"""Tests for the supply-chain pin guard (check_action_pins).

Every case here is a hole that was open at some point, not a hypothetical.
The guard's failure mode is silent: it prints "OK" and exits 0 while a mutable
container or floating tag goes unread, so a regression looks exactly like
success. That is what these tests exist to catch, and why each one names the
form that slipped through rather than only asserting a tidy invariant.

The fixtures build a whole throwaway repository and run the script inside it.
`REPO_ROOT` is derived from the script's own location (`parents[2]`), so
copying the script into `<tmp>/.github/scripts/` makes `<tmp>` the repository
under test — no monkeypatching of module state, and `main()` is exercised end
to end, including discovery, the worklist, and the exit code.
"""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("check_action_pins.py")

# Run in a subprocess whose argv[1] is the guard's directory, so the guard
# computes REPO_ROOT from its own location and reports the fixture repository's
# targets. Kept whole here rather than assembled from adjacent literals inside
# the call: a program spelled as fragments in an argument list reads like a
# list of arguments with a comma missing.
LIST_TARGETS = """
import sys
sys.path.insert(0, sys.argv[1])
import check_action_pins as m
for target in m.scan_targets():
    print(target.relative_to(m.REPO_ROOT))
"""


# Validate a regular file, repoint the name at a file outside the repository,
# then read — the exact sequence main() performs, with the window forced wide
# open. Prints the read's verdict, or a marker if outside content came back.
SWAP_PROBE = """
import pathlib
import sys

sys.path.insert(0, sys.argv[1])
import check_action_pins as guard

action = pathlib.Path(sys.argv[2])
outside = pathlib.Path(sys.argv[3])

readable, reason = guard._readable(action)
if readable is None:
    print("NOT-VALIDATED", reason)
    raise SystemExit(0)

action.unlink()
action.symlink_to(outside)

text, reason = guard._read(readable)
if text is not None and "actions/checkout@latest" in text:
    print("READ-OUTSIDE-CONTENT")
else:
    print(reason or "read something, but not the outside file")
"""


# The same sequence, but the thing repointed is the action's PARENT DIRECTORY
# rather than the file. O_NOFOLLOW on the final open is satisfied either way --
# `action.yml` under the substituted directory really is a regular file -- so
# this is only refused by a guard that checks the components above it too.
# Make the walk's own bookkeeping fail. `os.close` releasing a descriptor the
# walk has finished with is the one syscall here whose failure means nothing
# about the file being read — so it must not be the one that takes the run
# down. Patched in this child process only.
CLOSE_FAILURE_PROBE = """
import errno
import os
import pathlib
import sys

sys.path.insert(0, sys.argv[1])
import check_action_pins as guard

real_close, seen = os.close, []


def flaky(descriptor):
    seen.append(descriptor)
    if len(seen) == 1:
        raise OSError(errno.EBADF, "Bad file descriptor")
    return real_close(descriptor)


os.close = flaky

try:
    text, reason = guard._read(pathlib.Path(sys.argv[2]))
except BaseException as exc:
    print(f"RAISED {type(exc).__name__}: {exc}")
else:
    print("RETURNED", "text" if text is not None else f"({reason})")
"""


# `relative_to()` compares spellings, so `<root>/.github/../../outside.yml` is
# lexically inside the repository. Nothing here is a symlink, so O_NOFOLLOW has
# no opinion: the walk simply climbs. Prints what the read actually returned.
TRAVERSAL_PROBE = """
import pathlib
import sys

sys.path.insert(0, sys.argv[1])
import check_action_pins as guard

sneaky = pathlib.Path(guard.REPO_ROOT, ".github", "..", "..", sys.argv[2])
try:
    sneaky.relative_to(guard.REPO_ROOT)
except ValueError:
    print("NOT-LEXICALLY-INSIDE")
    raise SystemExit(0)

text, reason = guard._read(sneaky)
if text is not None and "actions/checkout@latest" in text:
    print("READ-OUTSIDE-CONTENT")
else:
    print(reason or "read something, but not the outside file")
"""


ANCESTOR_SWAP_PROBE = """
import pathlib
import shutil
import sys

sys.path.insert(0, sys.argv[1])
import check_action_pins as guard

action = pathlib.Path(sys.argv[2])
outside = pathlib.Path(sys.argv[3])

readable, reason = guard._readable(action)
if readable is None:
    print("NOT-VALIDATED", reason)
    raise SystemExit(0)

parent = action.parent
shutil.rmtree(parent)
parent.symlink_to(outside, target_is_directory=True)

text, reason = guard._read(readable)
if text is not None and "actions/checkout@latest" in text:
    print("READ-OUTSIDE-CONTENT")
else:
    print(reason or "read something, but not the outside file")
"""


class GuardFixture(unittest.TestCase):
    """A temporary repository containing a copy of the guard."""

    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="pinguard-"))
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        for directory in ("scripts", "workflows", "actions"):
            (self.root / ".github" / directory).mkdir(parents=True)
        shutil.copy(SCRIPT, self.root / ".github" / "scripts" / SCRIPT.name)

    def write(self, rel: str, text: str) -> Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def workflow(self, text: str, name: str = "ci.yml") -> Path:
        return self.write(f".github/workflows/{name}", text)

    def action(self, where: str, text: str) -> Path:
        return self.write(f".github/actions/{where}/action.yml", text)

    def run_guard(self) -> tuple[int, list[str], str]:
        """(exit code, findings, the whole stderr).

        The raw stderr is carried alongside the parsed findings and never
        thrown away. Selecting indented lines and discarding the rest would
        make this harness commit the guard's own sin: a traceback, or a
        finding printed in some future shape without leading spaces, would
        register as "no findings" -- output silently reclassified as safe
        because a pattern did not match it. The assertions below check what
        was dropped instead of trusting it, and quote all of stderr when they
        fail, so a broken guard says why rather than showing an empty list.
        """
        result = subprocess.run(
            [sys.executable, str(self.root / ".github" / "scripts" / SCRIPT.name)],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=self.root,
            check=False,
        )
        findings = [
            line.strip() for line in result.stderr.splitlines() if line.startswith("  ")
        ]
        return result.returncode, findings, result.stderr

    def scan_targets(self) -> list[str]:
        """The guard's own discovery list, as repo-relative strings."""
        listing = subprocess.run(
            [
                sys.executable,
                "-c",
                LIST_TARGETS,
                str(self.root / ".github" / "scripts"),
            ],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=self.root,
            check=False,
        )
        self.assertEqual(listing.returncode, 0, listing.stderr)
        return listing.stdout.splitlines()

    def assertClean(self) -> None:
        """Exit 0 and a silent stderr — no findings, and nothing else either."""
        code, findings, stderr = self.run_guard()
        self.assertEqual(code, 0, stderr)
        self.assertEqual(findings, [], stderr)
        # A clean run says "OK" on stdout and nothing at all on stderr, so any
        # stderr here is something this harness was not looking at: a warning,
        # a deprecation, a partial traceback that did not change the exit code.
        self.assertEqual(stderr, "", "clean run wrote to stderr")

    def assertFlags(self, *fragments: str) -> list[str]:
        """Exit 1, every stderr line accounted for, and each fragment reported."""
        code, findings, stderr = self.run_guard()
        self.assertEqual(code, 1, f"expected a finding; stderr was:\n{stderr}")
        unaccounted = [
            line
            for line in stderr.splitlines()
            if line.strip()
            and not line.startswith("  ")
            and "action-pin guard:" not in line
        ]
        self.assertEqual(unaccounted, [], f"unrecognised stderr:\n{stderr}")
        for fragment in fragments:
            self.assertTrue(
                any(fragment in finding for finding in findings),
                f"{fragment!r} not reported; stderr was:\n{stderr}",
            )
        return findings


PINNED = "a" * 40
DIGEST = "sha256:" + "b" * 64
CLEAN_WORKFLOW = (
    f"on: push\njobs:\n  j:\n    steps:\n      - uses: actions/checkout@{PINNED}\n"
)


class UsesTest(GuardFixture):
    """`uses:` refs must name a full 40-character commit SHA."""

    def test_full_sha_is_clean(self):
        self.workflow(CLEAN_WORKFLOW)
        self.assertClean()

    def test_floating_tag_is_flagged(self):
        self.workflow(
            "on: push\njobs:\n  j:\n    steps:\n      - uses: actions/checkout@v4\n"
        )
        self.assertFlags("actions/checkout@v4")

    def test_short_sha_is_flagged(self):
        self.workflow("on: push\nsteps:\n  - uses: actions/checkout@abc1234\n")
        self.assertFlags("actions/checkout@abc1234")

    def test_ref_without_at_is_flagged(self):
        self.workflow("on: push\nsteps:\n  - uses: actions/checkout\n")
        self.assertFlags("actions/checkout")

    def test_expression_cannot_be_resolved(self):
        # `\S+` never matched a value containing spaces, and an unmatched line
        # was treated as safe -- so the one ref that is unknowable at read time
        # was the one waved through.
        self.workflow("on: push\nsteps:\n  - uses: ${{ matrix.action }}\n")
        self.assertFlags("expression")

    def test_flow_mapping_fails_closed(self):
        # Valid YAML, valid Actions, invisible to a line-anchored pattern.
        self.workflow("on: push\nsteps: [{uses: actions/checkout@v4}]\n")
        self.assertFlags("flow mapping")

    def test_quoted_key_in_flow_mapping_fails_closed(self):
        # Stripping every quoted span also deleted quoted KEYS, which removed
        # the very token the flow check looks for.
        self.workflow("on: push\nsteps:\n  - {'uses': actions/checkout@v4}\n")
        self.assertFlags("flow mapping")

    def test_comma_inside_a_quoted_name_is_not_a_flow_mapping(self):
        # `- name: "step, uses: something"` contains `, uses:` and failed CI on
        # a step whose name merely held a comma.
        self.workflow(
            "on: push\nsteps:\n"
            '  - name: "check every workflow, uses: a full SHA"\n'
            f"    uses: actions/checkout@{PINNED}\n"
        )
        self.assertClean()

    def test_flow_form_inside_a_comment_is_not_a_finding(self):
        self.workflow(CLEAN_WORKFLOW + "# note: the {uses: x} form is rejected\n")
        self.assertClean()

    def test_docker_uses_needs_a_digest(self):
        # Skipped as a pin target, but still a container.
        self.workflow("on: push\nsteps:\n  - uses: docker://alpine:latest\n")
        self.assertFlags("docker ref needs")

    def test_digest_pinned_docker_uses_is_clean(self):
        self.workflow(f"on: push\nsteps:\n  - uses: docker://alpine@{DIGEST}\n")
        self.assertClean()


class LocalActionTest(GuardFixture):
    """`uses: ./…` is followed, because the action it names can be mutable."""

    def test_local_action_is_followed(self):
        self.workflow("on: push\nsteps:\n  - uses: ./tools/builder\n")
        self.write(
            "tools/builder/action.yml",
            "name: builder\nruns:\n  using: docker\n  image: 'docker://alpine:latest'\n",
        )
        # Outside .github/actions entirely -- reachable only by following.
        self.assertFlags("tools/builder/action.yml")

    def test_quoted_local_ref_is_followed(self):
        # `_scalar()` in one function and the raw value in the other made
        # `uses: "./x"` local to one and not the other.
        self.workflow('on: push\nsteps:\n  - uses: "./tools/builder"  # note\n')
        self.write(
            "tools/builder/action.yml",
            "name: builder\nruns:\n  using: docker\n  image: 'docker://alpine:latest'\n",
        )
        self.assertFlags("tools/builder/action.yml")

    def test_reference_cycle_terminates(self):
        self.workflow("on: push\nsteps:\n  - uses: ./a\n")
        self.write(
            "a/action.yml",
            "name: a\nruns:\n  using: composite\n  steps:\n    - uses: ./b\n",
        )
        self.write(
            "b/action.yml",
            "name: b\nruns:\n  using: composite\n  steps:\n    - uses: ./a\n",
        )
        self.assertClean()


class ContainerActionTest(GuardFixture):
    """A repository SHA pins the repository, never the container it builds."""

    def test_mutable_image_is_flagged(self):
        self.action(
            "app",
            "name: app\nruns:\n  using: docker\n  image: 'docker://alpine:latest'\n",
        )
        self.assertFlags("image needs")

    def test_digest_pinned_image_is_clean(self):
        self.action(
            "app",
            f"name: app\nruns:\n  using: docker\n  image: 'docker://alpine@{DIGEST}'\n",
        )
        self.assertClean()

    def test_composite_action_names_no_image(self):
        self.action("app", "name: app\nruns:\n  using: composite\n  steps: []\n")
        self.assertClean()

    def test_indented_top_level_runs_is_still_top_level(self):
        # Indentation is not a security boundary: a block mapping may carry a
        # uniform indent, and anchored at column 0 the guard never saw this.
        self.action(
            "app",
            "  name: app\n  runs: {using: docker, image: 'docker://alpine:latest'}\n",
        )
        self.assertFlags("image unverified")

    def test_indented_top_level_runs_with_digest_is_clean(self):
        self.action(
            "app",
            "  name: app\n  runs:\n    using: docker\n"
            f"    image: 'docker://alpine@{DIGEST}'\n",
        )
        self.assertClean()

    def test_whole_document_flow_mapping_fails_closed(self):
        self.action(
            "app",
            "{name: app, runs: {using: docker, image: 'docker://alpine:latest'}}\n",
        )
        self.assertFlags("flow mapping")

    def test_nested_runs_is_not_the_entry_point(self):
        # A `runs:` under `inputs:` is not the action's entry point, and
        # reporting it would invent a finding. The description deliberately
        # contains the words `using: docker`: without root-indent scoping the
        # guard treats this nested key as an entry point, finds that text in
        # its block and no `image:` under it, and fails the repository over a
        # sentence in a help string.
        self.action(
            "app",
            "name: app\ninputs:\n  runs:\n"
            "    description: 'set using: docker to build a container'\n"
            "runs:\n  using: composite\n  steps: []\n",
        )
        self.assertClean()

    def test_a_decoy_image_elsewhere_does_not_vouch_for_the_container(self):
        # Asking whether the FILE contains any `image:` let a digest-pinned
        # decoy under `inputs:` satisfy the test for a flow-form `runs:`.
        self.action(
            "app",
            "name: app\ninputs:\n  base:\n"
            f"    image: 'docker://alpine@{DIGEST}'\n"
            "runs: {using: docker, image: 'docker://alpine:latest'}\n",
        )
        self.assertFlags("flow mapping")

    def test_every_runs_candidate_is_judged(self):
        # Returning on the first match let a composite `runs:` seen first
        # excuse a docker one seen second.
        self.action(
            "app",
            "runs:\n  using: composite\n  steps: []\n"
            "runs: {using: docker, image: 'docker://alpine:latest'}\n",
        )
        self.assertFlags("flow mapping")

    def test_workflows_are_not_searched_for_runs_using(self):
        self.workflow(CLEAN_WORKFLOW + "  runs:\n    using: docker\n")
        self.assertClean()


class DockerfileTest(GuardFixture):
    """`image:` may name a build context, and its FROM lines are mutable."""

    def _action_with(self, dockerfile: str) -> None:
        self.action("app", "name: app\nruns:\n  using: docker\n  image: Dockerfile\n")
        self.write(".github/actions/app/Dockerfile", dockerfile)

    def test_mutable_from_is_flagged(self):
        # The original hole: a repository SHA freezes the Dockerfile TEXT, and
        # that text resolves its tag at build time.
        self._action_with("FROM alpine:latest\n")
        self.assertFlags("FROM alpine:latest")

    def test_digest_pinned_from_is_clean(self):
        self._action_with(f"FROM alpine@{DIGEST}\n")
        self.assertClean()

    def test_scratch_is_exempt(self):
        self._action_with("FROM scratch\n")
        self.assertClean()

    def test_earlier_stage_alias_is_exempt(self):
        self._action_with(f"FROM alpine@{DIGEST} AS build\nFROM build\n")
        self.assertClean()

    def test_a_stage_cannot_exempt_itself(self):
        # `FROM alpine AS alpine` matched `base in stages` when the alias was
        # registered before the base was classified.
        self._action_with("FROM alpine AS alpine\n")
        self.assertFlags("FROM alpine")

    def test_line_continuation_is_one_instruction(self):
        # Two physical lines to a regex, one instruction to Docker -- so
        # matching physical lines skipped the base entirely.
        self._action_with("FROM alpine:latest \\\n    AS build\n")
        self.assertFlags("FROM alpine:latest")

    def test_escape_directive_is_honoured(self):
        self._action_with("# escape=`\nFROM alpine:latest `\n    AS build\n")
        self.assertFlags("FROM alpine:latest")

    def test_escape_directive_after_an_ordinary_comment_is_ignored(self):
        # Docker stops looking for parser directives at the first ordinary
        # comment; honouring a later one joined continuations with the wrong
        # character and missed the FROM.
        self._action_with("# a note\n# escape=`\nFROM alpine:latest\n")
        self.assertFlags("FROM alpine:latest")

    def test_flag_tokens_before_the_base_are_skipped(self):
        self._action_with(f"FROM --platform=linux/amd64 alpine@{DIGEST}\n")
        self.assertClean()

    def test_unreadable_dockerfile_fails_closed(self):
        self.action("app", "name: app\nruns:\n  using: docker\n  image: Dockerfile\n")
        self.assertFlags("not a regular file")

    def test_path_outside_the_repository_is_refused(self):
        self.action(
            "app",
            "name: app\nruns:\n  using: docker\n  image: ../../../../etc/passwd\n",
        )
        self.assertFlags("outside the repository")


class WorkflowImageTest(GuardFixture):
    """Job containers and services are registry refs and need digests."""

    def test_mutable_container_is_flagged(self):
        self.workflow("on: push\njobs:\n  j:\n    container:\n      image: node:20\n")
        self.assertFlags("image needs")

    def test_inline_container_mapping_fails_closed(self):
        self.workflow("on: push\njobs:\n  j:\n    container: {image: node:20}\n")
        self.assertFlags("inline container mapping")

    def test_inline_services_mapping_fails_closed(self):
        self.workflow(
            "on: push\njobs:\n  j:\n    services: {redis: {image: redis:7}}\n"
        )
        self.assertFlags("inline services mapping")

    def test_empty_services_is_clean(self):
        self.workflow(CLEAN_WORKFLOW + "    services: {}\n")
        self.assertClean()

    def test_a_tag_containing_Dockerfile_is_a_registry_ref(self):
        # Docker tags may contain uppercase, so the build-context heuristic
        # read a legal registry ref as a path and called it unreadable. Only
        # action metadata can name a Dockerfile.
        self.workflow(
            "on: push\njobs:\n  j:\n    container:\n      image: myorg/app:Dockerfile-base\n"
        )
        self.assertFlags("image needs")


class DiscoveryTest(GuardFixture):
    """Discovery walks without following links, and reports what it skipped."""

    def test_nested_action_is_discovered(self):
        self.action(
            "vendor/pr-agent",
            "name: v\nruns:\n  using: docker\n  image: 'docker://alpine:latest'\n",
        )
        self.assertFlags("vendor/pr-agent/action.yml")

    def test_symlinked_action_file_is_not_read(self):
        self.action("real", "name: r\nruns:\n  using: composite\n  steps: []\n")
        link = self.root / ".github" / "actions" / "linked"
        link.mkdir()
        (link / "action.yml").symlink_to(self.root / ".github/actions/real/action.yml")
        self.assertFlags("symlink; not read")

    def test_symlinked_directory_is_reported_not_traversed(self):
        # A recursive glob over PR-controlled content can be pointed at an
        # arbitrary subtree. The walk refuses the link and says so.
        outside = self.root.parent / f"{self.root.name}-outside"
        outside.mkdir()
        self.addCleanup(shutil.rmtree, outside, ignore_errors=True)
        (outside / "action.yml").write_text("name: x\n", encoding="utf-8")
        (self.root / ".github" / "actions" / "evil").symlink_to(
            outside, target_is_directory=True
        )
        findings = self.assertFlags("symlink; not read")
        self.assertFalse([f for f in findings if "evil/action.yml" in f])

    def test_symlink_loop_terminates(self):
        loop = self.root / ".github" / "actions" / "loop"
        loop.mkdir(parents=True)
        (loop / "self").symlink_to(loop, target_is_directory=True)
        self.assertFlags("symlink; not read")

    def test_a_directory_symlink_named_action_yml_is_listed_once(self):
        # It satisfies both the directory pass and the filename pass. main()
        # would absorb the repeat -- its `seen` set is written before any
        # finding is -- so this asserts against scan_targets() itself, where
        # the duplicate actually lives, rather than against output that hides
        # it. Reported once either way, and the list is honest for any other
        # caller.
        weird = self.root / ".github" / "actions" / "weird"
        weird.mkdir(parents=True)
        (weird / "action.yml").symlink_to(
            self.root / ".github" / "actions", target_is_directory=True
        )
        targets = self.scan_targets()
        self.assertEqual(len(targets), len(set(targets)), targets)
        findings = self.assertFlags("weird/action.yml")
        self.assertEqual(len([f for f in findings if "weird/action.yml" in f]), 1)

    def test_a_byte_order_mark_does_not_hide_a_mutable_image(self):
        # This vault runs on Windows, where a round-trip through PowerShell's
        # default UTF-8 writer prepends a BOM. A BOM does NOT raise on a plain
        # utf-8 read -- it is valid UTF-8 -- it decodes to a U+FEFF glued to
        # the front of line 1, and every pattern here is anchored with `^\s*`,
        # which U+FEFF is not. So the guard reads the file, matches nothing on
        # that line, and reports OK. The container below is named on line 1 in
        # the flow form precisely because that is the arrangement where the
        # stray character is the difference between a finding and silence.
        path = self.root / ".github" / "actions" / "bom" / "action.yml"
        path.parent.mkdir(parents=True)
        path.write_bytes(
            "runs: {using: docker, image: 'docker://alpine:latest'}\nname: bom\n".encode(
                "utf-8-sig"
            )
        )
        self.assertFlags("image unverified")

    def test_a_file_swapped_for_a_symlink_after_the_check_is_not_read(self):
        # `_readable()` checks a PATH and `_read()` opens one: two operations on
        # a name, with a window between them. Verify a regular file, replace it
        # with a symlink pointing out of the repository, and a read by name
        # follows the link — outside content in the findings, from a guard whose
        # docstring said that window was closed. Opening with O_NOFOLLOW makes
        # the open itself refuse, so the check and the read can no longer
        # disagree about which object they mean.
        #
        # Run in the fixture repository, not this one: the guard derives
        # REPO_ROOT from its own location, and the containment check has to see
        # the planted file as inside the repository for the race to be the thing
        # under test rather than containment.
        action = self.root / ".github" / "actions" / "swapped" / "action.yml"
        action.parent.mkdir(parents=True)
        action.write_text("name: ok\nruns:\n  using: composite\n  steps: []\n")
        outside = self.root.parent / f"{self.root.name}-swap-target.yml"
        outside.write_text("on: push\nsteps:\n  - uses: actions/checkout@latest\n")
        self.addCleanup(outside.unlink, True)

        probe = subprocess.run(
            [
                sys.executable,
                "-c",
                SWAP_PROBE,
                str(self.root / ".github" / "scripts"),
                str(action),
                str(outside),
            ],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=self.root,
            check=False,
        )
        self.assertEqual(probe.returncode, 0, probe.stderr)
        verdict = probe.stdout.strip()
        self.assertNotIn(
            "READ-OUTSIDE-CONTENT", verdict, "a swapped-in symlink was followed"
        )
        self.assertIn("symlink", verdict)

    @unittest.skipUnless(
        os.open in os.supports_dir_fd,
        "descending by descriptor needs dir_fd; the ancestor half of the race "
        "is documented as open where it is missing, so asserting it here would "
        "fail on the platform the guard already says it cannot protect",
    )
    def test_an_ancestor_swapped_for_a_symlink_after_the_check_is_not_read(self):
        # The file-swap test above passes against a guard that closes only the
        # LAST component, which is what O_NOFOLLOW on a single open does. It
        # therefore proves less than it looks like it proves, and the gap was
        # real: with that version in place, replacing the action's parent
        # DIRECTORY with a link to somewhere outside the repository returned the
        # outside file's content, O_NOFOLLOW raising nothing because the final
        # component under the substituted directory is an ordinary file.
        #
        # Same fixture-repository reasoning as above: the guard derives
        # REPO_ROOT from its own location, so the planted path has to be inside
        # the copy for containment not to be what is actually under test.
        action = self.root / ".github" / "actions" / "ancestor" / "action.yml"
        action.parent.mkdir(parents=True)
        action.write_text("name: ok\nruns:\n  using: composite\n  steps: []\n")
        outside = self.root.parent / f"{self.root.name}-ancestor-target"
        outside.mkdir()
        self.addCleanup(shutil.rmtree, outside, ignore_errors=True)
        (outside / "action.yml").write_text(
            "on: push\nsteps:\n  - uses: actions/checkout@latest\n"
        )

        probe = subprocess.run(
            [
                sys.executable,
                "-c",
                ANCESTOR_SWAP_PROBE,
                str(self.root / ".github" / "scripts"),
                str(action),
                str(outside),
            ],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=self.root,
            check=False,
        )
        self.assertEqual(probe.returncode, 0, probe.stderr)
        verdict = probe.stdout.strip()
        self.assertNotIn(
            "READ-OUTSIDE-CONTENT", verdict, "a swapped-in ancestor was followed"
        )
        self.assertIn("symlink", verdict)

    def test_a_parent_reference_does_not_walk_out_of_the_repository(self):
        # No swap and no symlink in this one: `..` is an ordinary component,
        # and `Path.relative_to()` is a comparison of SPELLINGS, so
        # `<root>/.github/../../outside.yml` is "inside the repository" as far
        # as the containment check can tell. The walk then opened `.github`,
        # climbed back through two `..` components and read the outside file —
        # O_NOFOLLOW silent throughout, because nothing it was pointed at was a
        # link. The containment check has to be about where the path GOES, not
        # how it is written.
        outside = self.root.parent / f"{self.root.name}-traversal-target.yml"
        outside.write_text("on: push\nsteps:\n  - uses: actions/checkout@latest\n")
        self.addCleanup(outside.unlink, True)

        probe = subprocess.run(
            [
                sys.executable,
                "-c",
                TRAVERSAL_PROBE,
                str(self.root / ".github" / "scripts"),
                outside.name,
            ],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=self.root,
            check=False,
        )
        self.assertEqual(probe.returncode, 0, probe.stderr)
        verdict = probe.stdout.strip()
        self.assertNotIn(
            "READ-OUTSIDE-CONTENT", verdict, "a `..` component escaped the repository"
        )
        self.assertIn("outside the repository", verdict)

    @unittest.skipUnless(
        os.open in os.supports_dir_fd,
        "the descriptor walk is what holds the intermediate descriptors; "
        "without dir_fd there is no second close to fail",
    )
    def test_a_failed_close_reports_instead_of_raising(self):
        # The walk holds a directory descriptor, opens the next component from
        # it, and releases the previous one. That release is the one syscall in
        # here whose failure says NOTHING about the file being read — and it
        # was the only one outside a try. Forced to fail, `_read()` raised
        # OSError straight through its callers, so a guard whose whole subject
        # is "do not die where you could report" died. Every other case in this
        # file checks that a bad FILE produces a finding; this one checks that
        # a bad SYSCALL does too.
        action = self.root / ".github" / "actions" / "closefail" / "action.yml"
        action.parent.mkdir(parents=True)
        action.write_text("name: ok\nruns:\n  using: composite\n  steps: []\n")

        probe = subprocess.run(
            [
                sys.executable,
                "-c",
                CLOSE_FAILURE_PROBE,
                str(self.root / ".github" / "scripts"),
                str(action),
            ],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=self.root,
            check=False,
        )
        self.assertEqual(probe.returncode, 0, probe.stderr)
        self.assertIn("RETURNED", probe.stdout.strip(), probe.stdout)

    def test_non_utf8_metadata_is_a_finding_not_a_traceback(self):
        # A guard that dies still turns the job red, but it names a Python
        # error rather than the file.
        path = self.root / ".github" / "actions" / "bin" / "action.yml"
        path.parent.mkdir(parents=True)
        path.write_bytes(b"name: \xff\xfe not utf-8\n")
        self.assertFlags("not valid UTF-8")

    def test_empty_repository_is_an_error_not_a_pass(self):
        # Exit 2, distinct from both 0 (checked, clean) and 1 (checked, found
        # something): a run that discovered nothing verified nothing, and must
        # not be mistaken for a pass.
        code, findings, stderr = self.run_guard()
        self.assertEqual(code, 2, stderr)
        self.assertEqual(findings, [], stderr)
        self.assertIn("no workflow or action files found", stderr)


if __name__ == "__main__":
    unittest.main()
