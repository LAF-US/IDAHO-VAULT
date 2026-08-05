from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib import error, request


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LOG_PATH = REPO_ROOT / "!" / "MONITORING" / "health-log.md"
USER_AGENT = "IDAHO-VAULT/health-monitor"


@dataclass(frozen=True)
class ServiceSpec:
    name: str
    url: str


@dataclass(frozen=True)
class ServiceResult:
    name: str
    url: str
    ok: bool
    status_code: int | None
    detail: str


DEFAULT_SERVICES: tuple[ServiceSpec, ...] = (
    ServiceSpec(name="GitHub API", url="https://api.github.com"),
    ServiceSpec(name="Linear API", url="https://linear.app/api"),
    ServiceSpec(name="Slack Webhook Host", url="https://hooks.slack.com/"),
    ServiceSpec(name="OpenRouter API", url="https://openrouter.ai/api/v1"),
)


def check_service(service: ServiceSpec, timeout: float = 5.0) -> ServiceResult:
    req = request.Request(
        service.url,
        method="HEAD",
        headers={"User-Agent": USER_AGENT},
    )
    try:
        with request.urlopen(req, timeout=timeout) as response:
            status_code = getattr(response, "status", None)
            detail = f"reachable (HTTP {status_code})" if status_code is not None else "reachable"
            return ServiceResult(
                name=service.name,
                url=service.url,
                ok=True,
                status_code=status_code,
                detail=detail,
            )
    except error.HTTPError as exc:
        ok = exc.code < 500
        detail = f"reachable but returned HTTP {exc.code}"
        return ServiceResult(
            name=service.name,
            url=service.url,
            ok=ok,
            status_code=exc.code,
            detail=detail,
        )
    except error.URLError as exc:
        reason = getattr(exc, "reason", exc)
        return ServiceResult(
            name=service.name,
            url=service.url,
            ok=False,
            status_code=None,
            detail=f"unreachable: {reason}",
        )


def run_health_check(
    services: Iterable[ServiceSpec] = DEFAULT_SERVICES,
    *,
    timeout: float = 5.0,
) -> list[ServiceResult]:
    return [check_service(service, timeout=timeout) for service in services]


def _captured_at() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")


def render_markdown(results: Iterable[ServiceResult], *, captured_at: str | None = None) -> str:
    timestamp = captured_at or _captured_at()
    lines = [
        "# Runtime Health Snapshot",
        "",
        f"- Captured: `{timestamp}`",
        "",
        "| Service | Status | Detail |",
        "| --- | --- | --- |",
    ]
    for result in results:
        status = "OK" if result.ok else "FAIL"
        lines.append(f"| {result.name} | `{status}` | {result.detail} |")
    return "\n".join(lines)


def write_markdown_log(markdown: str, path: Path = DEFAULT_LOG_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    content = markdown if not existing.strip() else f"{existing.rstrip()}\n\n---\n\n{markdown}"
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check the reachability of runtime provider surfaces.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument(
        "--write-log",
        action="store_true",
        help="Append the markdown snapshot to !/MONITORING/health-log.md.",
    )
    args = parser.parse_args()

    results = run_health_check(timeout=args.timeout)
    captured_at = _captured_at()

    if args.format == "json":
        print(
            json.dumps(
                {
                    "captured_at": captured_at,
                    "results": [asdict(result) for result in results],
                },
                indent=2,
            )
        )
    else:
        markdown = render_markdown(results, captured_at=captured_at)
        print(markdown)
        if args.write_log:
            write_markdown_log(markdown)

    return 0 if all(result.ok for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
