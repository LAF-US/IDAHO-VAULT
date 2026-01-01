#!/usr/bin/env node
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import {
  copyFileSync,
  existsSync,
  lstatSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  realpathSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import { dirname, isAbsolute, join, relative, resolve, sep } from "node:path";
import { isDeepStrictEqual, parseArgs } from "node:util";
import { fileURLToPath, pathToFileURL } from "node:url";
import { assertPrebuiltProject, readPrebuiltArtifact, readPrebuiltManifest } from "../../../scripts/data-app-runtime.mjs";
import { buildPrebuiltDataApp } from "../../../scripts/data-app-build.mjs";
import { encodeDataAssetFragment } from "../../../scripts/data-url.mjs";
import { digestProtectedFile } from "../../../templates/data-app/base/scripts/protected-file-digest.mjs";
import { normalizeOwnerEmail } from "../../../templates/data-app/base/src/owner-email.js";

const { values } = parseArgs({
  options: {
    "project-dir": { type: "string" },
    "project-id": { type: "string" },
    "owner-email": { type: "string" },
    "read-only": { type: "boolean" },
    "migrate-packaging-manifest": { type: "boolean" },
    "presentation-file": { type: "string" },
    source: { type: "boolean", default: false },
  },
  strict: true,
});

for (const option of ["project-dir", "project-id"]) {
  if (!values[option]?.trim()) throw new Error(`Missing required --${option}.`);
}

if (values["migrate-packaging-manifest"] && !values.source) {
  throw new Error(
    "Legacy packaging manifest migration requires explicit --source --migrate-packaging-manifest with already-installed project Vite. Restore or upgrade the canonical starter to use prebuilt packaging.",
  );
}

const hasOwnerEmail = values["owner-email"] !== undefined;
if (hasOwnerEmail === Boolean(values["read-only"])) {
  throw new Error("Choose exactly one of --owner-email or --read-only.");
}
const ownerEmail = normalizeOwnerEmail(values["owner-email"]);
if (hasOwnerEmail && !ownerEmail) {
  throw new Error("A valid Site owner email is required to enable editing.");
}

const projectRoot = realpathSync(values["project-dir"]);
const projectId = values["project-id"].trim();
if (!/^[A-Za-z0-9][A-Za-z0-9_-]*$/u.test(projectId)) {
  throw new Error(
    "The Sites project ID must begin with a letter or digit and contain only letters, digits, underscores, or hyphens.",
  );
}

const pluginRoot = resolve(dirname(fileURLToPath(import.meta.url)), "../../..");

function jsonExpression(value) {
  // Parse a quoted JSON document instead of embedding an object literal. This
  // preserves own "__proto__" keys and keeps every authored byte inside a string.
  const document = JSON.stringify(JSON.stringify(value))
    .replaceAll("\u2028", "\\u2028")
    .replaceAll("\u2029", "\\u2029");
  return `JSON.parse(${document})`;
}

function ownerSeedModule(source, { migration = false } = {}) {
  const invalidShape = () =>
    new Error(
      migration
        ? "Packaging manifest migration requires an unmodified Data app owner module shape."
        : "The Data app owner module must contain only its expected owner exports and comments.",
    );
  const skipTrivia = (start) => {
    let offset = start;
    while (offset < source.length) {
      if (/\s/u.test(source[offset])) offset += 1;
      else if (source.startsWith("//", offset)) {
        const end = source.slice(offset + 2).search(/[\r\n\u2028\u2029]/u);
        offset = end < 0 ? source.length : offset + 2 + end;
      } else if (source.startsWith("/*", offset)) {
        const end = source.indexOf("*/", offset + 2);
        if (end < 0) throw invalidShape();
        offset = end + 2;
      } else break;
    }
    return offset;
  };
  const seeds = [];
  let offset = skipTrivia(0);
  while (offset < source.length) {
    const declaration = /^export const (dataAppOwner(?:UserId|Email)Sha256) = "/u.exec(source.slice(offset));
    if (!declaration) throw invalidShape();
    const name = declaration[1];
    const start = offset + declaration[0].length;
    const end = source.indexOf('"', start);
    if (end < 0 || !source.startsWith('";', end)) throw invalidShape();
    const value = source.slice(start, end);
    if (value && !/^[a-f\d]{64}$/iu.test(value)) {
      throw new Error("The existing Data app owner seed is invalid.");
    }
    seeds.push({ name, start, end, value });
    offset = skipTrivia(end + 2);
  }
  // Old static exports are accepted only to clear or migrate an existing seed.
  const shape = seeds.map(({ name }) => name).join(",");
  if (![
    "dataAppOwnerEmailSha256",
    "dataAppOwnerUserIdSha256",
    "dataAppOwnerUserIdSha256,dataAppOwnerEmailSha256",
  ].includes(shape)) {
    throw invalidShape();
  }
  if (seeds.filter(({ value }) => value).length > 1) {
    throw new Error("The Data app owner module must not contain multiple active owner authorization seeds.");
  }
  return seeds;
}

async function importVerifiedModule(code) {
  // Import the bytes that were verified, not a path that can change between the
  // integrity check and module loading. Release Worker assets are self-contained.
  try {
    return await import(`data:text/javascript;base64,${Buffer.from(code).toString("base64")}`);
  } catch {
    // A data-URL exception can echo the complete reviewed HTML and snapshot.
    throw new Error("The verified Data Worker module could not be loaded.");
  }
}

function escapeAttribute(value) {
  return value.replaceAll("&", "&amp;").replaceAll('"', "&quot;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");
}

function localReferenceVariants(paths) {
  const variants = new Set(
    paths.flatMap((path) => [path, escapeAttribute(path), encodeURI(path), encodeURIComponent(path)]),
  );
  for (let depth = 0; depth < 3; depth += 1) {
    for (const value of [...variants]) variants.add(JSON.stringify(value).slice(1, -1));
  }
  return [...variants];
}

const GENERATED_DATA_URL = /data:([a-z\d!#$%&'*+.^_`|~-]+\/[a-z\d!#$%&'*+.^_`|~-]+)(;charset=utf-8)?;base64,/giu;
const MAX_EMBEDDED_DATA_BYTES = 64 * 1024 * 1024;
const MAX_TOTAL_EMBEDDED_DATA_BYTES = 128 * 1024 * 1024;
const MAX_EMBEDDED_DATA_URLS = 256;
const MAX_EMBEDDED_DATA_DEPTH = 8;
const dataLimitError = () => new Error("The Data app exceeds the supported embedded-data privacy inspection limits.");
const malformedDataUrl = () => new Error("The Data app contains a malformed embedded data URL.");

function precedingBackslashes(text, index) {
  let count = 0;
  while (index > 0 && text[--index] === "\\") count += 1;
  return count;
}

function dynamicTemplate(text) {
  for (const match of text.matchAll(/\$\{/gu)) {
    if (precedingBackslashes(text, match.index) % 2 === 0) return true;
  }
  return false;
}

function htmlDataUrlContext(text) {
  const attributes = new Map();
  const styles = [];
  // Only markup attributes are strict HTML URLs. Skip raw-text element bodies
  // so an authored JavaScript template that constructs markup is still source.
  const tags = /<!--[\s\S]*?(?:-->|$)|<\/?([a-z][a-z\d:-]*)(?=[\t\n\f\r />])(?:[^"'<>]|"[^"]*"|'[^']*')*>/giu;
  for (let tag; (tag = tags.exec(text)); ) {
    if (!tag[1] || tag[0].startsWith("</")) continue;
    const name = tag[1].toLowerCase();
    const attributePattern =
      /[\t\n\f\r ](?:src|href)[\t\n\f\r ]*=[\t\n\f\r ]*(?:"([^"]*)"|'([^']*)'|([^\t\n\f\r "'=<>`]+))/giu;
    for (const attribute of tag[0].matchAll(attributePattern)) {
      const value = attribute[1] ?? attribute[2] ?? attribute[3];
      const prefix = value.matchAll(GENERATED_DATA_URL).next().value;
      if (!prefix || prefix.index !== 0) continue;
      const quoted = attribute[3] === undefined;
      const offset = tag.index + attribute.index + attribute[0].length - value.length - Number(quoted);
      attributes.set(offset, { value: value.slice(prefix[0].length), strict: true });
    }
    if (name === "plaintext") break;
    if (!/^(?:script|style|title|textarea|xmp|iframe|noembed|noframes|noscript)$/u.test(name)) continue;
    const close = new RegExp(`</${name}(?=[\\t\\n\\f\\r />])[^>]*>`, "giu");
    close.lastIndex = tags.lastIndex;
    const end = close.exec(text);
    if (name === "style") styles.push(text.slice(tags.lastIndex, end?.index));
    tags.lastIndex = end ? close.lastIndex : text.length;
  }
  return { attributes, styles };
}

function dataUrlCandidate(text, match, wholeValue, context) {
  const start = match.index + match[0].length;
  if (wholeValue && !text.slice(0, match.index).trim()) {
    return { value: text.slice(start), strict: true };
  }
  const attribute = context.attributes?.get(match.index);
  if (attribute) return attribute;
  const before = text.slice(Math.max(0, match.index - 256), match.index);
  const quotedCssUrl = context.css && /\burl\(\s*\\*["']$/iu.test(before);
  const quote = text[match.index - 1];
  if (['"', "'", "`"].includes(quote)) {
    const escapes = precedingBackslashes(text, match.index - 1);
    let end = -1;
    for (let cursor = start; cursor < text.length; cursor += 1) {
      if (text[cursor] !== quote) continue;
      const closingEscapes = precedingBackslashes(text, cursor);
      if (escapes > closingEscapes) continue;
      if (!quotedCssUrl && !escapes && closingEscapes % 2) continue;
      end = cursor - escapes;
      break;
    }
    if (end < start) return quotedCssUrl ? { value: text.slice(start), strict: true } : null;
    const value = text.slice(start, end);
    if (!quotedCssUrl && quote === "`" && dynamicTemplate(value)) return null;
    return { value, strict: Boolean(quotedCssUrl) };
  }
  if (context.css && /\burl\(\s*$/iu.test(before)) {
    const end = text.indexOf(")", start);
    return {
      value: text.slice(start, end < 0 ? undefined : end).replace(/[\t\n\f\r ]+$/u, ""),
      strict: true,
    };
  }
  const value = /^[^\s"'`\\<>()\[\]{}]*/u.exec(text.slice(start))[0];
  return { value, strict: false };
}

function asciiFold(bytes) {
  const folded = Buffer.from(bytes);
  for (let index = 0; index < folded.length; index += 1) {
    if (folded[index] >= 65 && folded[index] <= 90) folded[index] += 32;
  }
  return folded;
}

function textualMime(mime, charset) {
  return (
    Boolean(charset) ||
    mime.startsWith("text/") ||
    mime === "image/svg+xml" ||
    /^application\/(?:json|javascript|ecmascript|xml|[^/]+\+(?:json|xml))$/u.test(mime)
  );
}

function embeddedTextKind(mime) {
  if (mime === "text/css") return "css";
  if (mime === "text/html" || mime === "application/xhtml+xml" || mime === "image/svg+xml") return "html";
  return "source";
}

function assertPublicationPrivacy(
  source,
  localTaskIds,
  localReferencePaths,
  worker = false,
  { structured = false, kind = "source" } = {},
) {
  const taskValues = localTaskIds.map((value) => value.toLowerCase());
  const referenceValues = localReferenceVariants(localReferencePaths);
  const referenceText = referenceValues.map((value) => value.toLowerCase());
  const taskBytes = taskValues.map((value) => asciiFold(Buffer.from(value)));
  const referenceBytes = referenceValues.map((value) => asciiFold(Buffer.from(value)));
  const pending = [{ value: source, depth: 0, structured, kind }];
  const objects = new WeakSet();
  const visitedUrls = new Set();
  let count = 0;
  let totalBytes = 0;
  const rejectTask = () => {
    throw new Error(
      worker
        ? "The published Sites Worker must not contain a local task identifier."
        : "The reviewed Data app contains a local task identifier outside its preview metadata.",
    );
  };
  const rejectReference = () => {
    throw new Error(
      worker
        ? "The published Sites Worker must not contain a local filesystem reference."
        : "The reviewed Data app contains a local filesystem reference outside its preview metadata.",
    );
  };
  const checkText = (text) => {
    const lower = text.toLowerCase();
    if (taskValues.some((value) => lower.includes(value))) rejectTask();
    if (referenceText.some((value) => lower.includes(value))) rejectReference();
  };
  const checkBytes = (bytes) => {
    const folded = asciiFold(bytes);
    if (taskBytes.some((value) => folded.includes(value))) rejectTask();
    if (referenceBytes.some((value) => folded.includes(value))) rejectReference();
  };
  while (pending.length) {
    const { value, depth, structured: wholeValue, kind: textKind } = pending.pop();
    if (wholeValue && value && typeof value === "object") {
      if (objects.has(value)) continue;
      objects.add(value);
      for (const [key, child] of Object.entries(value)) {
        pending.push(
          { value: key, depth, structured: true, kind: "source" },
          { value: child, depth, structured: true, kind: "source" },
        );
      }
      continue;
    }
    if (typeof value !== "string") continue;
    checkText(value);
    const context = textKind === "html" ? htmlDataUrlContext(value) : { css: textKind === "css" };
    for (const style of context.styles ?? []) {
      pending.push({ value: style, depth, structured: false, kind: "css" });
    }
    // The generator emits MIME/base64 URLs, not remote fetches. Strictly check
    // complete HTML/CSS URL values and parsed configuration strings. Elsewhere
    // in source, inspect canonical literal candidates without mistaking a
    // dynamic JavaScript prefix or documentation for a malformed emitted URL.
    for (const match of value.matchAll(GENERATED_DATA_URL)) {
      const candidate = dataUrlCandidate(value, match, wholeValue, context);
      if (!candidate) continue;
      const fragmentOffset = candidate.value.indexOf("#");
      const encoded = fragmentOffset < 0 ? candidate.value : candidate.value.slice(0, fragmentOffset);
      const fragment = fragmentOffset < 0 ? "" : candidate.value.slice(fragmentOffset + 1);
      const invalid = () => {
        if (candidate.strict) throw malformedDataUrl();
        return true;
      };
      if (encoded.length % 4 !== 0 || !/^[a-z\d+/]*={0,2}$/iu.test(encoded)) {
        invalid();
        continue;
      }
      if (encoded.length > Math.ceil(MAX_EMBEDDED_DATA_BYTES / 3) * 4 || fragment.length > MAX_EMBEDDED_DATA_BYTES * 3)
        throw dataLimitError();
      let decodedFragment;
      try {
        decodedFragment = decodeURIComponent(fragment);
        if (encodeDataAssetFragment(decodedFragment) !== fragment) {
          invalid();
          continue;
        }
      } catch {
        invalid();
        continue;
      }
      const mime = match[1].toLowerCase();
      const key = `${mime}${match[2] ? ";charset=utf-8" : ""},${candidate.value}`;
      if (visitedUrls.has(key)) continue;
      const bytes = Buffer.from(encoded, "base64");
      if (bytes.toString("base64") !== encoded) {
        invalid();
        continue;
      }
      if (++count > MAX_EMBEDDED_DATA_URLS || depth >= MAX_EMBEDDED_DATA_DEPTH) throw dataLimitError();
      visitedUrls.add(key);
      totalBytes += bytes.length + Buffer.byteLength(decodedFragment);
      if (bytes.length > MAX_EMBEDDED_DATA_BYTES || totalBytes > MAX_TOTAL_EMBEDDED_DATA_BYTES) throw dataLimitError();
      checkBytes(bytes);
      if (decodedFragment) {
        pending.push({ value: decodedFragment, depth: depth + 1, structured: true, kind: "source" });
      }
      let decoded;
      try {
        decoded = new TextDecoder("utf-8", { fatal: true }).decode(bytes);
      } catch {
        if (textualMime(mime, match[2])) {
          throw new Error("The Data app contains a non-UTF-8 embedded text data URL.");
        }
      }
      if (decoded) {
        pending.push({ value: decoded, depth: depth + 1, structured: false, kind: embeddedTextKind(mime) });
        if (mime === "application/json" || mime.endsWith("+json")) {
          try {
            pending.push({ value: JSON.parse(decoded), depth: depth + 1, structured: true, kind: "source" });
          } catch {
            // A ?url asset need not itself be valid JSON; its exact text was
            // still inspected. Do not impose a new asset-format requirement.
          }
        }
      }
    }
  }
}

function projectPath(path) {
  const realPath = realpathSync(path);
  const nested = relative(projectRoot, realPath);
  if (isAbsolute(nested) || nested === ".." || nested.startsWith(`..${sep}`) || resolve(projectRoot, nested) !== realPath) {
    throw new Error("Every Sites packaging input must stay inside the Data app project.");
  }
  return realPath;
}

function projectOutput(path) {
  const absolutePath = resolve(path);
  const nested = relative(projectRoot, absolutePath);
  if (isAbsolute(nested) || nested === ".." || nested.startsWith(`..${sep}`)) {
    throw new Error("Every Sites packaging output must stay inside the Data app project.");
  }
  let container = existsSync(absolutePath) ? absolutePath : dirname(absolutePath);
  while (!existsSync(container)) container = dirname(container);
  projectPath(container);
  return absolutePath;
}

function assertPrebuiltServerDirectory(directory) {
  let metadata;
  try {
    metadata = lstatSync(directory);
  } catch (error) {
    if (error.code === "ENOENT") return;
    throw error;
  }
  if (
    !metadata.isDirectory() ||
    metadata.isSymbolicLink() ||
    readdirSync(directory, { withFileTypes: true }).some(
      (entry) => entry.name !== "index.js" || !entry.isFile() || entry.isSymbolicLink(),
    )
  ) {
    throw new Error(
      "Prebuilt Sites packaging requires dist/server to contain only a regular index.js. " +
        "Review and remove stale source-build outputs, or use explicit --source.",
    );
  }
}

const sensitiveMetadataKey = /authorization|authentication|authheaders?|session|cookie|csrf|xsrf|bearer|tokens?|pass(?:word|wd)|secrets?|credentials?|(?:api|access|private)keys?|connectionstrings?|signedurls?|signatures?|xamz|xgoog|sharedaccesssignature/iu;
const credentialValue = /(?:\bbearer\s+[a-z\d._~+/-]+=*|\beyj[a-z\d_-]+\.eyj[a-z\d_-]+\.[a-z\d_-]+\b|\b(?:access[_-]?token|tokens?|api[_-]?key|session(?:[_-]?id)?|(?:j|php)?sess(?:ion)?id|password|passwd|secret|signature|sig|x-amz-signature|x-goog-signature)\s*[=:]\s*[^\s&,;]+)/iu;
const credentialPath = /(?:^|\/)(?:bearer|tokens?|access[_-]?tokens?|api[_-]?keys?|password|passwd|secrets?|credentials?|signatures?|sig|signed(?:url)?|x[_-]?(?:amz|goog)[_-]?signature)(?:\/|[=:_-]|$)/iu;
const credentialJwtPath = /(?:^|\/)eyj[a-z\d_-]+\.eyj[a-z\d_-]+\.[a-z\d_-]+(?:\/|$)/iu;
const embeddedSession = /(?:^|[;/])(?:j|php)?sess(?:ion)?id\s*=/iu;
const encodedUrlDelimiter = /%(?:25)*(?:3f|23)/iu;
const embeddedUrl = /(?:[a-z][a-z\d+.-]*:\/\/|\/\/|(?<![\w/])\/|(?<![\w/])(?:[a-z\d._~%-]+(?:\/[a-z\d._~%-]+)*)?(?=[?#][^\s<>"'`]*=))[^\s<>"'`]+/giu;

function isCalendarEventSourceLocator(rawUrl, sourceValue) {
  // Calendar htmlLink's eid locates an event; it is not an access credential.
  // Require the exact raw URL so normalization cannot hide additional parameters.
  return (
    /^https:\/\/www\.google\.com(?::443)?\/calendar\/event\?eid=[A-Za-z0-9_-]{1,2048}$/u.test(rawUrl) &&
    (!sourceValue.trimStart().startsWith(rawUrl) || sourceValue === rawUrl) &&
    !/[\0-\x1f\x7f]/u.test(sourceValue)
  );
}

function rejectCredentials(value, location = "snapshot", path = []) {
  if (typeof value === "string") {
    if (credentialValue.test(value) || encodedUrlDelimiter.test(value)) {
      throw new Error(`The Data app snapshot contains embedded credentials at ${location}.`);
    }

    for (const match of value.matchAll(embeddedUrl)) {
      let url;
      try {
        url = new URL(match[0], "https://data-app.invalid");
      } catch {
        throw new Error(`The Data app snapshot contains an invalid source URL at ${location}.`);
      }
      let pathname;
      try {
        pathname = url.pathname;
        for (let depth = 0; depth < 8; depth += 1) {
          pathname = decodeURIComponent(pathname);
          if (!/%[a-f\d]{2}/iu.test(pathname)) break;
          if (depth === 7) throw new Error("Source URL encoding exceeds the supported depth.");
        }
      } catch {
        throw new Error(`The Data app snapshot contains an invalid source URL at ${location}.`);
      }
      if (url.username || url.password || (url.search && !isCalendarEventSourceLocator(match[0], value))
        || url.hash || /[?#]/u.test(pathname)
        || credentialPath.test(pathname) || credentialJwtPath.test(pathname)
        || embeddedSession.test(pathname) || credentialValue.test(pathname)) {
        throw new Error(`The Data app snapshot contains a credential-bearing source URL at ${location}.`);
      }
    }
    return;
  }

  if (Array.isArray(value)) {
    for (const [index, entry] of value.entries()) {
      rejectCredentials(entry, `${location}[${index}]`, [...path, index]);
    }
    return;
  }
  if (!value || typeof value !== "object") return;

  for (const [key, entry] of Object.entries(value)) {
    const normalizedKey = key.toLowerCase().replace(/[^a-z\d]/gu, "");
    if (normalizedKey === "rows" && Array.isArray(entry)
      && path.length === 2 && path[0] === "queries") continue;
    const queryId = path.length === 1 && path[0] === "queries";
    const harmlessMetric = typeof entry === "boolean" || (
      typeof entry === "number"
      && /(?:counts?|total|rate|ratio|duration|usage|score|percent(?:age)?)$/iu.test(normalizedKey)
    );
    if (!queryId && entry !== null && !harmlessMetric && sensitiveMetadataKey.test(normalizedKey)) {
      throw new Error(`The Data app snapshot contains credential metadata at ${location}.${key}.`);
    }
    rejectCredentials(entry, `${location}.${key}`, [...path, key]);
  }
}

const hostingPath = projectPath(join(projectRoot, ".openai/hosting.json"));
const hostingSource = readFileSync(hostingPath, "utf8");
const hosting = JSON.parse(hostingSource);
if (hosting?.project_id && hosting.project_id !== projectId) {
  throw new Error("The Data app does not belong to the requested Sites project.");
}
if (
  !values.source &&
  (!hosting || hosting.d1 !== "DB" || hosting.r2 !== null ||
    Object.keys(hosting).some((key) => !["project_id", "d1", "r2"].includes(key)))
) {
  throw new Error("Prebuilt Data hosting must use only project_id, d1: DB, and r2: null; preserve existing bindings.");
}

let prebuiltManifest;
if (!values.source) {
  assertPrebuiltServerDirectory(join(projectRoot, "dist/server"));
  prebuiltManifest = await readPrebuiltManifest(pluginRoot);
  const existingHtmlPath = join(projectRoot, "dist/index.html");
  const html = existsSync(existingHtmlPath) ? readFileSync(projectPath(existingHtmlPath), "utf8") : "";
  const head = /<head(?:\s[^>]*)?>([\s\S]*?)<\/head\s*>/iu.exec(html)?.[1] ?? "";
  const markers = [...head.matchAll(/<meta name="data-app-runtime-sha256" content="([a-f\d]{64})">/gu)];
  if (markers.length !== 1 || markers[0][1] !== prebuiltManifest.artifacts.app.sha256) {
    // Rebuild old/missing clients without changing any copied runtime source.
    // A failed build preserves the old output, so the same retry needs no state file.
    await buildPrebuiltDataApp({ projectDir: projectRoot, pluginRoot, onProgress: (message) => console.error(message) });
  }
}

const htmlPath = projectPath(join(projectRoot, "dist/index.html"));
const snapshotPath = projectPath(join(projectRoot, "src/data.json"));
const ownerPath = projectPath(join(projectRoot, "src/data-app-owner.js"));
const workerPath = values.source ? projectPath(join(projectRoot, "src/worker.js")) : join(projectRoot, "src/worker.js");
const protectedManifestPath = projectPath(join(projectRoot, "protected-runtime.json"));
if (!values.source) assertPrebuiltServerDirectory(join(projectRoot, "dist/server"));
const serverDirectory = projectOutput(join(projectRoot, "dist/server"));
const serverOutputPath = projectOutput(join(serverDirectory, "index.js"));
const distHostingPath = projectOutput(join(projectRoot, "dist/.openai/hosting.json"));

const protectedManifestSource = readFileSync(protectedManifestPath, "utf8");
const protectedManifest = JSON.parse(protectedManifestSource);
const packagingOwnedPaths = new Set([".openai/hosting.json", "src/data-app-owner.js"]);
const approvedEditablePaths = ["src/content/", "src/theme.css", "src/data.json"];
if (
  protectedManifest.version !== 1 ||
  JSON.stringify(protectedManifest.editablePaths) !== JSON.stringify(approvedEditablePaths) ||
  !protectedManifest.files ||
  typeof protectedManifest.files !== "object" ||
  Array.isArray(protectedManifest.files)
) {
  throw new Error("The Data app protected runtime manifest is invalid.");
}
for (const requiredPath of values.source
  ? [...packagingOwnedPaths, "src/worker.js", "scripts/verify-protected-runtime.mjs"]
  : []) {
  if (!Object.hasOwn(protectedManifest.files, requiredPath)) {
    throw new Error(`The Data app protected runtime manifest does not protect ${requiredPath}.`);
  }
}
const digestHelperName = "scripts/protected-file-digest.mjs";
const protectsDigestHelper = Object.hasOwn(protectedManifest.files, digestHelperName);
let digestHelperExists = false;
if (values.source) {
  try {
    lstatSync(join(projectRoot, digestHelperName));
    digestHelperExists = true;
  } catch (error) {
    if (error.code !== "ENOENT") throw error;
  }
}
if (values.source && !protectsDigestHelper && digestHelperExists) {
  throw new Error(
    "The Data app protected runtime manifest must protect its existing digest helper before any source verification.",
  );
}
const legacySourceManifest = !protectsDigestHelper;
const packagingDigest = (path, contents) =>
  legacySourceManifest ? createHash("sha256").update(contents).digest("hex") : digestProtectedFile(path, contents);
const protectedMismatches = [];
// Copied runtime source is only consumed by an explicitly selected source build.
for (const [protectedPath, expectedHash] of values.source ? Object.entries(protectedManifest.files) : []) {
  if (typeof expectedHash !== "string" || !/^[a-f\d]{64}$/u.test(expectedHash)) {
    throw new Error(`The Data app protected runtime hash is invalid: ${protectedPath}.`);
  }
  const actualPath = projectPath(join(projectRoot, protectedPath));
  const actualHash = packagingDigest(protectedPath, readFileSync(actualPath));
  if (actualHash !== expectedHash) protectedMismatches.push(protectedPath);
}
const unrelatedProtectedMismatches = protectedMismatches.filter((path) => !packagingOwnedPaths.has(path));
if (unrelatedProtectedMismatches.length) {
  throw new Error(
    `Protected Data app runtime files were modified outside packaging ownership: ${unrelatedProtectedMismatches.join(
      ", ",
    )}. Restore the canonical starter, or explicitly authorize the source change before using --source.`,
  );
}
if (protectedMismatches.length && !values["migrate-packaging-manifest"]) {
  throw new Error(
    "Protected Data app packaging metadata is out of sync. Use --source --migrate-packaging-manifest only " +
      "to repair a verified existing Site's hosting and owner manifest entries.",
  );
}
if (values["migrate-packaging-manifest"] && !protectedMismatches.length) {
  throw new Error("Packaging manifest migration requires existing legacy hosting or owner hash mismatches.");
}

const reviewedHtml = readFileSync(htmlPath);
const reviewedHtmlSource = reviewedHtml.toString("utf8");
const localThreadMarkers = [
  ...reviewedHtmlSource.matchAll(/<meta\b[^>]*\bname\s*=\s*["']?data-app-local-thread(?=["'\s/>]|$)[^>]*(?:>|$)/giu),
];
if (localThreadMarkers.length > 1) {
  throw new Error("The reviewed Data app contains duplicate local task metadata.");
}
const localThreadMarker = localThreadMarkers[0];
const localThreadMatch = localThreadMarker?.[0].match(
  /^<meta\s+name="data-app-local-thread"\s+content="([\da-f]{8}-[\da-f]{4}-[\da-f]{4}-[\da-f]{4}-[\da-f]{12})"\s*\/?>$/iu,
);
if (localThreadMarker && !localThreadMatch) {
  throw new Error("The reviewed Data app contains malformed local task metadata.");
}
const localThreadId = localThreadMatch?.[1] ?? null;
const localReferenceMarkers = [
  ...reviewedHtmlSource.matchAll(/<meta\b[^>]*\bname\s*=\s*["']?data-app-local-reference(?=["'\s/>]|$)[^>]*(?:>|$)/giu),
];
if (localReferenceMarkers.length > 1) {
  throw new Error("The reviewed Data app contains duplicate local-reference metadata.");
}
const localReferenceMarker = localReferenceMarkers[0];
const localReferencePaths = [projectRoot, htmlPath];
if (localReferenceMarker) {
  try {
    const content = /^<meta name="data-app-local-reference" content="([^"]*)">$/u.exec(localReferenceMarker[0])?.[1];
    if (content === undefined) throw new Error("Invalid marker.");
    const decoded = content
      .replaceAll("&quot;", '"')
      .replaceAll("&lt;", "<")
      .replaceAll("&gt;", ">")
      .replaceAll("&amp;", "&");
    const reference = JSON.parse(decoded);
    const canonical = JSON.stringify({ root: reference.root, htmlPath: reference.htmlPath });
    if (
      content !== escapeAttribute(canonical) ||
      [reference.root, reference.htmlPath].some(
        (path) => typeof path !== "string" || !isAbsolute(path) || /[\0-\x1f\x7f]/u.test(path),
      ) ||
      reference.root !== projectRoot ||
      reference.htmlPath !== htmlPath ||
      realpathSync(reference.root) !== reference.root ||
      projectPath(reference.htmlPath) !== reference.htmlPath ||
      !/<head(?:\s[^>]*)?>[\s\S]*?<\/head\s*>/iu.exec(reviewedHtmlSource)?.[0].includes(localReferenceMarker[0])
    ) {
      throw new Error("Invalid reference.");
    }
  } catch {
    throw new Error("The reviewed Data app contains malformed local-reference metadata.");
  }
}
const transientMarkers = [localThreadMarker, localReferenceMarker]
  .filter(Boolean)
  .sort((left, right) => left.index - right.index);
const htmlParts = [];
let htmlOffset = 0;
for (const marker of transientMarkers) {
  const markerOffset = Buffer.byteLength(reviewedHtmlSource.slice(0, marker.index), "utf8");
  if (markerOffset < htmlOffset) throw new Error("The reviewed Data app contains overlapping local metadata.");
  htmlParts.push(reviewedHtml.subarray(htmlOffset, markerOffset));
  htmlOffset = markerOffset + Buffer.byteLength(marker[0], "utf8");
}
htmlParts.push(reviewedHtml.subarray(htmlOffset));
const sourceHtml = transientMarkers.length ? Buffer.concat(htmlParts) : reviewedHtml;
const localTaskIds = [localThreadId, process.env.CODEX_SESSION_ID, process.env.CODEX_THREAD_ID].filter((value) =>
  /^[\da-f]{8}-[\da-f]{4}-[\da-f]{4}-[\da-f]{4}-[\da-f]{12}$/iu.test(value ?? ""),
);
assertPublicationPrivacy(sourceHtml.toString("utf8"), localTaskIds, localReferencePaths, false, { kind: "html" });

const sourceSnapshot = readFileSync(snapshotPath);
let decodedSnapshot;
try {
  decodedSnapshot = new TextDecoder("utf-8", { fatal: true }).decode(sourceSnapshot);
} catch {
  throw new Error("The reviewed Data app snapshot must be valid UTF-8.");
}
const snapshot = JSON.parse(decodedSnapshot);

if (!snapshot.queries || typeof snapshot.queries !== "object" || Array.isArray(snapshot.queries)) {
  throw new Error("The Data app must contain a reviewed query snapshot.");
}
rejectCredentials(snapshot);

const snapshotHash = createHash("sha256").update(sourceSnapshot).digest("hex");
const documentHead = /<head(?:\s[^>]*)?>([\s\S]*?)<\/head\s*>/iu.exec(sourceHtml.toString("utf8"))?.[1];
const snapshotMarkers = [...(documentHead ?? "").matchAll(
  /<meta\b[^>]*\bname\s*=\s*(["'])data-app-snapshot-sha256\1[^>]*>/giu,
)];
const snapshotMarkerHash = snapshotMarkers.length === 1
  ? /\bcontent\s*=\s*(["'])([a-f\d]{64})\1/u.exec(snapshotMarkers[0][0])?.[2]
  : null;
if (snapshotMarkerHash !== snapshotHash) {
  throw new Error("The built Data app HTML must contain exactly one matching reviewed snapshot integrity marker.");
}

const presentationPath = values["presentation-file"] ? projectPath(values["presentation-file"]) : null;
const requestedPresentation = presentationPath ? JSON.parse(readFileSync(presentationPath, "utf8")) : {};
let persistedPresentation = requestedPresentation;
if (
  requestedPresentation &&
  typeof requestedPresentation === "object" &&
  !Array.isArray(requestedPresentation) &&
  Object.hasOwn(requestedPresentation, "filterDefinitions")
) {
  const reviewedFilterDefinitions = snapshot.filters ?? [];
  if (
    !Array.isArray(reviewedFilterDefinitions) ||
    !Array.isArray(requestedPresentation.filterDefinitions) ||
    !isDeepStrictEqual(requestedPresentation.filterDefinitions, reviewedFilterDefinitions)
  ) {
    throw new Error("Presentation filter definitions must exactly match the reviewed Data app snapshot.");
  }
  persistedPresentation = { ...requestedPresentation };
  delete persistedPresentation.filterDefinitions;
}
function validatedInitialPresentation(validatePresentation) {
  const initialPresentation = { ...validatePresentation(persistedPresentation) };
  // Verification can only originate from an authenticated creator in the deployed Worker.
  delete initialPresentation.verification;
  return initialPresentation;
}

if (values["migrate-packaging-manifest"] && (hosting.project_id !== projectId || hosting.d1 !== "DB")) {
  throw new Error("Packaging manifest migration requires the existing exact Sites project identity and DB binding.");
}

const ownerBytes = readFileSync(ownerPath);
const ownerSource = ownerBytes.toString("utf8");
if (!Buffer.from(ownerSource, "utf8").equals(ownerBytes))
  throw new Error("The Data app owner module is not valid UTF-8.");
const ownerSeeds = ownerSeedModule(ownerSource, {
  migration: Boolean(values["migrate-packaging-manifest"]),
});
const persistedOwner = ownerSeeds.find(({ value }) => value);
const hasEmailOwnerExport = ownerSeeds.some(({ name }) => name === "dataAppOwnerEmailSha256");
const ownerEmailHash = ownerEmail ? createHash("sha256").update(ownerEmail).digest("hex") : "";
const ownerAuthorization = ownerEmailHash ? "email" : "none";
const ownerPreserved = Boolean(
  ownerEmailHash &&
  persistedOwner?.name === "dataAppOwnerEmailSha256" &&
  persistedOwner.value.toLowerCase() === ownerEmailHash,
);
const ownerTransferred = Boolean(persistedOwner && ownerEmailHash && !ownerPreserved);
const ownerRevoked = Boolean(persistedOwner && !ownerEmailHash);

const temporaryWorkerPath = join(dirname(workerPath), ".sites-worker-entry.mjs");
if (values.source && existsSync(temporaryWorkerPath)) throw new Error("A stale Sites Worker entry must be removed first.");
const workerEnvironment = { ...process.env, CODEX_SESSION_ID: "", CODEX_THREAD_ID: "" };
const workerConfiguration = (initialPresentation) => ({
  html: sourceHtml.toString("utf8"),
  projectId,
  seedSnapshot: snapshot,
  ownerEmailSha256: ownerEmailHash,
  initialPresentation,
});
let packagedWorker;
let vitePath;
let workerRuntimeSha256;
if (values.source) {
  const verifierPath = projectPath(join(projectRoot, "scripts/verify-protected-runtime.mjs"));
  // A legacy migration repairs only the two preflight-checked packaging hashes.
  // Run the project's verifier against that prospective repair, then restore
  // the original manifest even if verification fails before publication starts.
  const repairedCurrentManifest = values["migrate-packaging-manifest"]
    ? `${JSON.stringify(
        {
          ...protectedManifest,
          files: {
            ...protectedManifest.files,
            ".openai/hosting.json": packagingDigest(".openai/hosting.json", readFileSync(hostingPath)),
            "src/data-app-owner.js": packagingDigest("src/data-app-owner.js", readFileSync(ownerPath)),
          },
        },
        null,
        2,
      )}\n`
    : null;
  let verification;
  try {
    if (repairedCurrentManifest !== null) writeFileSync(protectedManifestPath, repairedCurrentManifest);
    verification = spawnSync(process.execPath, [verifierPath], {
      cwd: projectRoot,
      encoding: "utf8",
      env: workerEnvironment,
      stdio: ["ignore", "pipe", "pipe"],
    });
  } finally {
    if (repairedCurrentManifest !== null) writeFileSync(protectedManifestPath, protectedManifestSource);
  }
  if (verification.error) throw verification.error;
  if (verification.status !== 0) {
    throw new Error(`Protected Data app source verification failed with status ${verification.status}.`);
  }
  const localVite = join(projectRoot, "node_modules/vite/bin/vite.js");
  if (!existsSync(localVite)) {
    throw new Error(
      "Source-mode Sites packaging requires an already-installed project Vite. No dependencies will be downloaded.",
    );
  }
  vitePath = projectPath(localVite);
  const presentationModule = projectPath(join(projectRoot, "src/presentation-state.js"));
  const { validatePresentation } = await import(pathToFileURL(presentationModule).href);
  const initialPresentation = validatedInitialPresentation(validatePresentation);
  assertPublicationPrivacy(workerConfiguration(initialPresentation), localTaskIds, localReferencePaths, true, {
    structured: true,
  });
  const workerSource = readFileSync(workerPath, "utf8");
  const ownerImport = `import { ${ownerSeeds.map(({ name }) => name).join(", ")} } from "./data-app-owner.js";`;
  if (workerSource.split(ownerImport).length !== 2) {
    throw new Error("The Data app Worker does not contain its expected owner authorization.");
  }
  const ownerConstants = ownerSeeds
    .map(({ name }) => `const ${name} = ${JSON.stringify(name === "dataAppOwnerEmailSha256" ? ownerEmailHash : "")};`)
    .join("\n");
  const emailProperty = "ownerEmailSha256: dataAppOwnerEmailSha256,";
  const ownerProperty = hasEmailOwnerExport ? emailProperty : "ownerUserIdSha256: dataAppOwnerUserIdSha256,";
  const usesFactory = workerSource.includes("createDataAppWorker(");
  if (ownerEmailHash && (!usesFactory || !hasEmailOwnerExport || !workerSource.includes(emailProperty))) {
    throw new Error(
      "Owner-email authorization requires a confirmed, scoped protected runtime upgrade " +
        "of src/worker.js and src/data-app-owner.js, or use prebuilt packaging.",
    );
  }
  if (usesFactory) {
    const expectedOwnerProperties = ownerSeeds.map(({ name }) => `${name.replace("dataAppOwner", "owner")}: ${name},`);
    if (
      expectedOwnerProperties.some((property) => workerSource.split(property).length !== 2) ||
      [...workerSource.matchAll(/\bowner(?:UserId|Email)Sha256\s*:/gu)].length !== ownerSeeds.length ||
      /\binitialPresentation\s*:/u.test(workerSource)
    ) {
      throw new Error(
        "The source Data app Worker does not contain its expected owner authorization and presentation factory.",
      );
    }
    packagedWorker = workerSource
      .replace(ownerImport, ownerConstants)
      .replace(
        ownerProperty,
        `${ownerProperty}\n  projectId: ${JSON.stringify(projectId)},\n  initialPresentation: ${jsonExpression(initialPresentation)},`,
      );
  } else {
    // Existing monolithic Workers can still be republished read-only; the
    // packager does not silently replace their reviewed implementation.
    const seedPattern = ').bind(id, "{}", 0, new Date().toISOString()).run();';
    if (
      workerSource.split('const id = "current";').length !== 2 ||
      workerSource.split(seedPattern).length !== 2 ||
      /\bconst initialPresentation\b/u.test(workerSource)
    ) {
      throw new Error("The source Data app Worker does not contain its expected presentation seed.");
    }
    packagedWorker = workerSource
      .replace(ownerImport, ownerConstants)
      .replace(
        'const id = "current";',
        `const id = "current";\nconst initialPresentation = ${jsonExpression(initialPresentation)};`,
      )
      .replace(seedPattern, ").bind(id, JSON.stringify(initialPresentation), 0, new Date().toISOString()).run();");
  }
} else {
  const checked = await assertPrebuiltProject({ projectDir: projectRoot, pluginRoot, manifest: prebuiltManifest });
  const runtime = await readPrebuiltArtifact("worker", {
    pluginRoot: checked.pluginRoot,
    manifest: checked.manifest,
  });
  const { validatePresentation, createDataAppWorker } = await importVerifiedModule(runtime.code);
  if (typeof validatePresentation !== "function" || typeof createDataAppWorker !== "function") {
    throw new Error(
      "The verified Data Worker runtime does not provide its expected factory and presentation validator.",
    );
  }
  const initialPresentation = validatedInitialPresentation(validatePresentation);
  const configuration = workerConfiguration(initialPresentation);
  assertPublicationPrivacy(configuration, localTaskIds, localReferencePaths, true, { structured: true });
  packagedWorker = `${runtime.code}\nexport default createDataAppWorker(${jsonExpression(configuration)});\n`;
  const packagedModule = await importVerifiedModule(packagedWorker);
  if (typeof packagedModule.default?.fetch !== "function") {
    throw new Error("The verified Data Worker runtime did not produce a Sites Worker.");
  }
  workerRuntimeSha256 = runtime.sha256;
}

const existingDistHosting = existsSync(distHostingPath) ? readFileSync(distHostingPath) : null;
const existingServer = existsSync(serverOutputPath) ? readFileSync(projectPath(serverOutputPath)) : null;
const packagedOwnerSource = values.source || (ownerSeeds.length === 1 && hasEmailOwnerExport)
  ? ownerSeeds.reduceRight(
      (source, seed) =>
        source.slice(0, seed.start) +
        (seed.name === "dataAppOwnerEmailSha256" ? ownerEmailHash : "") +
        source.slice(seed.end),
      ownerSource,
    )
  : `export const dataAppOwnerEmailSha256 = "${ownerEmailHash}";\n`;
const packagedHostingSource = `${JSON.stringify({ ...hosting, project_id: projectId, d1: "DB" }, null, 2)}\n`;
const packagedProtectedManifestSource = `${JSON.stringify(
  {
    ...protectedManifest,
    files: {
      ...protectedManifest.files,
      ".openai/hosting.json": packagingDigest(".openai/hosting.json", packagedHostingSource),
      "src/data-app-owner.js": packagingDigest("src/data-app-owner.js", packagedOwnerSource),
    },
  },
  null,
  2,
)}\n`;
let htmlUpdated = false;
let ownerUpdated = false;
let hostingUpdated = false;
let distHostingUpdated = false;
let temporaryWorkerCreated = false;
let protectedManifestUpdated = false;
let serverPath;
try {
  if (transientMarkers.length) {
    htmlUpdated = true;
    writeFileSync(htmlPath, sourceHtml);
  }
  if (values.source) {
    temporaryWorkerCreated = true;
    writeFileSync(temporaryWorkerPath, packagedWorker);
    const result = spawnSync(
      process.execPath,
      [vitePath, "build", "--ssr", temporaryWorkerPath, "--outDir", serverDirectory, "--emptyOutDir"],
      { cwd: projectRoot, encoding: "utf8", env: workerEnvironment, stdio: "inherit" },
    );
    if (result.error) throw result.error;
    if (result.status !== 0) throw new Error(`Sites Worker packaging failed with status ${result.status}.`);
    rmSync(temporaryWorkerPath, { force: true });
    temporaryWorkerCreated = false;
  } else {
    mkdirSync(serverDirectory, { recursive: true });
    writeFileSync(serverOutputPath, packagedWorker);
  }

  serverPath = projectPath(join(projectRoot, "dist/server/index.js"));
  assertPublicationPrivacy(readFileSync(serverPath, "utf8"), localTaskIds, localReferencePaths, true);

  assert.deepEqual(
    readFileSync(htmlPath),
    sourceHtml,
    "Sites packaging must preserve the reviewed Data app HTML after removing local task metadata.",
  );
  assert.deepEqual(
    readFileSync(snapshotPath),
    sourceSnapshot,
    "Sites packaging must preserve the exact reviewed Data app snapshot.",
  );

  mkdirSync(dirname(distHostingPath), { recursive: true });
  hostingUpdated = true;
  writeFileSync(hostingPath, packagedHostingSource);
  distHostingUpdated = true;
  copyFileSync(hostingPath, distHostingPath);
  ownerUpdated = true;
  writeFileSync(ownerPath, packagedOwnerSource);
  protectedManifestUpdated = true;
  writeFileSync(protectedManifestPath, packagedProtectedManifestSource);
} catch (error) {
  const rollbackErrors = [];
  const restore = (action) => {
    try {
      action();
    } catch (rollbackError) {
      rollbackErrors.push(rollbackError);
    }
  };
  if (protectedManifestUpdated) restore(() => writeFileSync(protectedManifestPath, protectedManifestSource));
  restore(() => {
    if (existingServer) {
      mkdirSync(dirname(serverOutputPath), { recursive: true });
      writeFileSync(serverOutputPath, existingServer);
    } else {
      rmSync(serverOutputPath, { force: true });
    }
  });
  if (ownerUpdated) restore(() => writeFileSync(ownerPath, ownerSource));
  if (hostingUpdated) restore(() => writeFileSync(hostingPath, hostingSource));
  if (distHostingUpdated)
    restore(() => {
      if (existingDistHosting) writeFileSync(distHostingPath, existingDistHosting);
      else rmSync(distHostingPath, { force: true });
    });
  if (htmlUpdated) restore(() => writeFileSync(htmlPath, reviewedHtml));
  if (temporaryWorkerCreated) {
    restore(() => rmSync(temporaryWorkerPath, { force: true }));
    temporaryWorkerCreated = false;
  }
  if (rollbackErrors.length) {
    throw new AggregateError(
      [error, ...rollbackErrors],
      "Sites packaging failed and some prior artifacts could not be restored.",
    );
  }
  throw error;
} finally {
  if (temporaryWorkerCreated) rmSync(temporaryWorkerPath, { force: true });
}

console.log(
  JSON.stringify({
    projectRoot,
    projectId,
    htmlPath,
    serverPath,
    htmlSha256: createHash("sha256").update(sourceHtml).digest("hex"),
    snapshotSha256: snapshotHash,
    generatedAt: snapshot.generatedAt ?? null,
    queryIds: Object.keys(snapshot.queries),
    ownerAuthorization,
    ownerSeeded: Boolean(ownerEmailHash),
    ownerPreserved,
    ownerTransferred,
    ownerRevoked,
    presentationSeeded: true,
    databaseBinding: "DB",
    buildMode: values.source ? "source" : "prebuilt",
    ...(workerRuntimeSha256 ? { workerRuntimeSha256 } : {}),
  }),
);
