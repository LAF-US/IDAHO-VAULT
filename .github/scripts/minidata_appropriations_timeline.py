import argparse
import csv
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


TRACKED_BILLS = [
    "S1361",
    "S1363",
    "S1375",
    "S1373",
    "H0847",
    "H0848",
    "S1331",
    "S1380",
    "S1381",
    "S1382",
    "S1384",
    "S1385",
    "S1383",
    "S1362",
]

MAIL_GLOB = "MiniData File for *_ 2026.msg"
ATTACH_STREAM = "__attach_version1.0_#00000000\\__substg1.0_37010102"
ATTACH_NAME_STREAM = "__attach_version1.0_#00000000\\__substg1.0_3704001F"

CSV_FALLBACKS = [
    ("downloads-original", "2026-03-20", Path(r"C:\Users\loganf\Downloads\minidata.csv")),
    ("downloads-1", "2026-03-23", Path(r"C:\Users\loganf\Downloads\minidata (1).csv")),
    ("downloads-2", "2026-03-24", Path(r"C:\Users\loganf\Downloads\minidata (2).csv")),
    ("vault-apr01", "2026-04-01", Path(r"C:\Users\loganf\Documents\IDAHO-VAULT\minidata-2026-04-01.csv")),
]


@dataclass(frozen=True)
class Snapshot:
    label: str
    date: str
    path: Path
    source: str
    attachment_name: str | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build an appropriations-bill status timeline from dated minidata snapshots. "
            "Defaults to the vault's dated .msg originals and falls back to local CSVs."
        )
    )
    parser.add_argument(
        "--source",
        choices=("auto", "msg", "csv"),
        default="auto",
        help="Choose whether to read vault .msg originals, CSV fallbacks, or auto-detect.",
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path.cwd(),
        help="Workspace root that contains the dated MiniData .msg files.",
    )
    parser.add_argument(
        "--extract-dir",
        type=Path,
        default=Path("tmp-minidata-msg"),
        help="Directory for extracted attachment streams when using .msg sources.",
    )
    return parser.parse_args()


def load_csv_rows(path: Path) -> dict[str, tuple[str, str, str]]:
    data: dict[str, tuple[str, str, str]] = {}
    with path.open("r", encoding="cp1252", newline="") as handle:
        for row in csv.reader(handle):
            if not row or len(row) < 3:
                continue
            bill_id = row[0].strip().upper()
            title = row[1].strip()
            status = row[2].strip()
            vote = row[3].strip() if len(row) > 3 else ""
            data[bill_id] = (title, status, vote)
    return data


def build_csv_fallback_snapshots() -> list[Snapshot]:
    snapshots: list[Snapshot] = []
    for label, date, path in CSV_FALLBACKS:
        if path.exists():
            snapshots.append(Snapshot(label=label, date=date, path=path, source="csv"))
    return snapshots


def decode_utf16le_text(path: Path) -> str:
    return path.read_bytes().decode("utf-16le").rstrip("\x00")


def extract_msg_attachment(msg_path: Path, extract_root: Path) -> tuple[Path, str]:
    target = extract_root / msg_path.stem
    target.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [
            "7z",
            "x",
            "-y",
            f"-o{target}",
            str(msg_path),
            ATTACH_STREAM,
            ATTACH_NAME_STREAM,
        ],
        check=True,
        capture_output=True,
    )

    attachment_dir = target / "__attach_version1.0_#00000000"
    data_path = attachment_dir / "__substg1.0_37010102"
    name_path = attachment_dir / "__substg1.0_3704001F"
    try:
        attachment_name = decode_utf16le_text(name_path)
    except OSError:
        # The data stream is the real source of truth. If Windows briefly balks
        # at the name sidecar stream, keep the timeline usable and carry on.
        attachment_name = "minidata.csv"
    return data_path, attachment_name


def parse_msg_date(msg_path: Path) -> tuple[str, str]:
    raw = msg_path.stem.replace("MiniData File for ", "").replace("_ ", ", ")
    date_obj = datetime.strptime(raw, "%B %d, %Y")
    return raw, date_obj.strftime("%Y-%m-%d")


def build_msg_snapshots(workspace: Path, extract_root: Path) -> list[Snapshot]:
    msg_files = sorted(workspace.glob(MAIL_GLOB))
    snapshots: list[Snapshot] = []
    for msg_path in msg_files:
        label, date = parse_msg_date(msg_path)
        data_path, attachment_name = extract_msg_attachment(msg_path, extract_root)
        snapshots.append(
            Snapshot(
                label=label,
                date=date,
                path=data_path,
                source="msg",
                attachment_name=attachment_name,
            )
        )
    return sorted(snapshots, key=lambda snap: snap.date)


def resolve_snapshots(args: argparse.Namespace) -> list[Snapshot]:
    extract_root = args.extract_dir
    if not extract_root.is_absolute():
        extract_root = args.workspace / extract_root

    msg_snapshots = build_msg_snapshots(args.workspace, extract_root)
    csv_snapshots = build_csv_fallback_snapshots()

    if args.source == "msg":
        return msg_snapshots
    if args.source == "csv":
        return csv_snapshots
    return msg_snapshots or csv_snapshots


def print_source_header(snapshots: list[Snapshot]) -> None:
    print("Sources")
    for snap in snapshots:
        detail = f"attachment={snap.attachment_name}" if snap.attachment_name else snap.path.name
        print(f"{snap.date}\t{snap.source}\t{snap.label}\t{detail}")
    print()


def print_detail_table(snapshots: list[Snapshot], rows_by_snapshot: dict[str, dict[str, tuple[str, str, str]]]) -> None:
    print("Bill\tSnapshotDate\tSnapshotLabel\tStatus\tChangedFromPrior\tTitle")
    for bill_id in TRACKED_BILLS:
        previous_status = None
        for snap in snapshots:
            row = rows_by_snapshot[snap.date].get(bill_id)
            if row is None:
                status = "(missing)"
                title = ""
            else:
                title, status, _vote = row
            changed = "yes" if previous_status is not None and status != previous_status else ""
            print(f"{bill_id}\t{snap.date}\t{snap.label}\t{status}\t{changed}\t{title}")
            previous_status = status
        print()


def print_summary(snapshots: list[Snapshot], rows_by_snapshot: dict[str, dict[str, tuple[str, str, str]]]) -> None:
    print("ActivitySummary")
    print("Bill\tActivityDates\tFinalStatus")
    for bill_id in TRACKED_BILLS:
        activity_dates: list[str] = []
        previous_status = None
        final_status = "(missing)"
        for snap in snapshots:
            row = rows_by_snapshot[snap.date].get(bill_id)
            status = row[1] if row else "(missing)"
            final_status = status
            if previous_status is not None and status != previous_status:
                activity_dates.append(snap.date)
            previous_status = status
        joined = ", ".join(activity_dates) if activity_dates else "(no snapshot change)"
        print(f"{bill_id}\t{joined}\t{final_status}")


def main() -> int:
    args = parse_args()
    snapshots = resolve_snapshots(args)
    if not snapshots:
        raise FileNotFoundError("No dated minidata snapshots found in .msg or CSV form.")

    rows_by_snapshot = {snap.date: load_csv_rows(snap.path) for snap in snapshots}
    print_source_header(snapshots)
    print_detail_table(snapshots, rows_by_snapshot)
    print_summary(snapshots, rows_by_snapshot)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
