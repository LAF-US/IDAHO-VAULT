#!/usr/bin/env python3
"""Validate LAF-USB external-object manifests.

The Universal Sync Bus manifest connector is intentionally credential-free. It
does not transfer, delete, or sync payloads. It validates the small durable
records that let Git reference objects carried by external storage lanes.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import PurePosixPath, PureWindowsPath
from typing import Any


REQUIRED_OBJECT_FIELDS = {
    "id",
    "original_filename",
    "git_policy",
    "carrier_lane",
    "topology_role",
    "runtime_scope",
    "storage_key",
    "size_bytes",
    "checksum",
    "verification_state",
    "sensitivity",
    "related",
}

VALID_GIT_POLICIES = {"external-over-lfs-limit", "external-operational", "lfs-pointer", "git-native"}
VALID_CARRIER_LANES = {"rclone", "rsync", "gcloud-storage-rsync", "provider-manual", "local-manual", "disabled"}
VALID_TOPOLOGY_ROLES = {"hot", "cold", "immutable", "local-cache", "staging-mirror", "disabled", "unknown"}
VALID_RUNTIME_SCOPES = {"local", "cloud", "ci", "unavailable", "unknown"}
VALID_VERIFICATION_STATES = {"pending", "size-verified", "checksum-verified", "missing", "failed", "not-required"}
VALID_SENSITIVITY = {"publishable", "private", "sensitive", "secret", "draft", "unknown"}

SECRET_PATTERNS = [
    re.compile(r"(?i)(token|secret|password|credential|private[_-]?key)\s*[:=]"),
    re.compile(r"(?i)(signed|presigned)[_-]?url"),
    re.compile(r"(?i)aws_access_key_id|aws_secret_access_key"),
    re.compile(r"(?i)-----BEGIN [A-Z ]*PRIVATE KEY-----"),
]


def is_absolute_path(value: str) -> bool:
    if PureWindowsPath(value).is_absolute():
        return True
    return PurePosixPath(value).is_absolute()


def load_manifest(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("manifest root must be a JSON object")
    return data


def flatten_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        strings: list[str] = []
        for key, nested in value.items():
            strings.extend(flatten_strings(key))
            strings.extend(flatten_strings(nested))
        return strings
    if isinstance(value, list):
        strings: list[str] = []
        for nested in value:
            strings.extend(flatten_strings(nested))
        return strings
    return []


def validate_object(index: int, obj: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(obj, dict):
        return [f"object[{index}] must be an object"]

    missing = sorted(REQUIRED_OBJECT_FIELDS - set(obj))
    if missing:
        errors.append(f"object[{index}] missing required fields: {', '.join(missing)}")

    object_id = obj.get("id", f"object[{index}]")
    prefix = f"{object_id}"

    if obj.get("git_policy") not in VALID_GIT_POLICIES:
        errors.append(f"{prefix}: invalid git_policy {obj.get('git_policy')!r}")
    if obj.get("carrier_lane") not in VALID_CARRIER_LANES:
        errors.append(f"{prefix}: invalid carrier_lane {obj.get('carrier_lane')!r}")
    if obj.get("topology_role") not in VALID_TOPOLOGY_ROLES:
        errors.append(f"{prefix}: invalid topology_role {obj.get('topology_role')!r}")
    if obj.get("runtime_scope") not in VALID_RUNTIME_SCOPES:
        errors.append(f"{prefix}: invalid runtime_scope {obj.get('runtime_scope')!r}")
    if obj.get("verification_state") not in VALID_VERIFICATION_STATES:
        errors.append(f"{prefix}: invalid verification_state {obj.get('verification_state')!r}")
    if obj.get("sensitivity") not in VALID_SENSITIVITY:
        errors.append(f"{prefix}: invalid sensitivity {obj.get('sensitivity')!r}")

    size_bytes = obj.get("size_bytes")
    if not isinstance(size_bytes, int) or size_bytes < 0:
        errors.append(f"{prefix}: size_bytes must be a non-negative integer")

    checksum = obj.get("checksum")
    if not isinstance(checksum, dict):
        errors.append(f"{prefix}: checksum must be an object")
    else:
        algorithm = checksum.get("algorithm")
        value = checksum.get("value")
        if algorithm not in {"sha256", "sha512", "none", None}:
            errors.append(f"{prefix}: unsupported checksum algorithm {algorithm!r}")
        if value is not None and not isinstance(value, str):
            errors.append(f"{prefix}: checksum.value must be string or null")

    related = obj.get("related")
    if not isinstance(related, list):
        errors.append(f"{prefix}: related must be a list")

    for field in ("original_filename", "storage_key"):
        value = obj.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{prefix}: {field} must be a non-empty string")
        elif is_absolute_path(value):
            errors.append(f"{prefix}: {field} must not be an absolute local path")

    for text in flatten_strings(obj):
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"{prefix}: possible credential material in manifest text")
                break

    return errors


def validate_manifest(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != "laf-usb-object-manifest/v1":
        errors.append("schema must be laf-usb-object-manifest/v1")

    objects = data.get("laf_usb_objects")
    if not isinstance(objects, list):
        errors.append("laf_usb_objects must be a list")
        return errors

    seen_ids: set[str] = set()
    for index, obj in enumerate(objects):
        errors.extend(validate_object(index, obj))
        if isinstance(obj, dict):
            object_id = obj.get("id")
            if isinstance(object_id, str):
                if object_id in seen_ids:
                    errors.append(f"{object_id}: duplicate id")
                seen_ids.add(object_id)

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", nargs="+", help="JSON manifest file(s) to validate")
    args = parser.parse_args()

    failed = False
    for manifest in args.manifest:
        try:
            errors = validate_manifest(load_manifest(manifest))
        except Exception as exc:  # noqa: BLE001 - CLI should report bad files plainly.
            print(f"{manifest}: {exc}", file=sys.stderr)
            failed = True
            continue

        if errors:
            failed = True
            print(f"{manifest}: invalid", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)
        else:
            print(f"{manifest}: OK")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
