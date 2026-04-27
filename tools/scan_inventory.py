import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import hexedit

REPORT_DIR = REPO_ROOT / "data" / "reports"
SEARCH_START = 30000
SEARCH_END = 90000
ENTRY_SIZE = 12
ENTRY_COUNT = 2048
SAMPLE_ENTRIES = 192


def _build_known_maps():
    known_by_id = {}
    duplicate_ids = Counter()
    for raw_item, item_name in hexedit.KNOWN_INVENTORY_ITEMS.items():
        item_key = tuple(hexedit.normalize_item_descriptor(raw_item)["item_id"])
        duplicate_ids[item_key] += 1
        known_by_id.setdefault(item_key, item_name)
    return known_by_id, duplicate_ids


KNOWN_BY_ID, DUPLICATE_IDS = _build_known_maps()


def _read_entry(slot_data, index):
    raw_item = int.from_bytes(slot_data[index : index + 4], "little")
    item_id = tuple(hexedit.normalize_item_descriptor(raw_item)["item_id"])
    quantity = int.from_bytes(slot_data[index + 4 : index + 8], "little")
    unique_id = int.from_bytes(slot_data[index + 8 : index + 12], "little")
    return item_id, quantity, unique_id


def discover_inventory_start(slot_data):
    best = None

    max_start = min(len(slot_data) - (ENTRY_SIZE * SAMPLE_ENTRIES), SEARCH_END)
    for start in range(SEARCH_START, max_start, 4):
        valid_uid_count = 0
        nonzero_qty_count = 0
        known_match_count = 0

        for offset in range(start, start + (ENTRY_SIZE * SAMPLE_ENTRIES), ENTRY_SIZE):
            item_id, quantity, unique_id = _read_entry(slot_data, offset)
            if unique_id != 0:
                valid_uid_count += 1
            if quantity > 0:
                nonzero_qty_count += 1
            if item_id in KNOWN_BY_ID:
                known_match_count += 1

        score = (known_match_count * 5) + (valid_uid_count * 2) + nonzero_qty_count
        candidate = {
            "start": start,
            "score": score,
            "known_match_count": known_match_count,
            "valid_uid_count": valid_uid_count,
            "nonzero_qty_count": nonzero_qty_count,
        }

        if best is None or candidate["score"] > best["score"]:
            best = candidate

    return best


def scan_slot(slot_data, slot_index, slot_name):
    anchor = discover_inventory_start(slot_data)
    entries = []
    unknown_entries = []
    known_entries = []

    start = anchor["start"]
    for i in range(ENTRY_COUNT):
        index = start + (i * ENTRY_SIZE)
        item_id, quantity, unique_id = _read_entry(slot_data, index)
        if quantity <= 0 or unique_id == 0:
            continue

        entry = {
            "slot": slot_index,
            "character": slot_name,
            "index": index,
            "item_id": list(item_id),
            "unique_id": unique_id,
            "quantity": quantity,
        }

        item_name = KNOWN_BY_ID.get(item_id)
        if item_name is not None:
            entry["name"] = item_name
            known_entries.append(entry)
        else:
            unknown_entries.append(entry)

        entries.append(entry)

    return {
        "slot": slot_index,
        "character": slot_name,
        "inventory_start": start,
        "anchor_score": anchor,
        "known_entries": known_entries,
        "unknown_entries": unknown_entries,
        "total_entries": len(entries),
    }


def scan_save(save_path):
    save_path = Path(save_path)
    names = hexedit.get_names(str(save_path))
    slots = hexedit.get_slot_ls(str(save_path))
    slot_reports = []

    for slot_index, (slot_name, slot_data) in enumerate(zip(names, slots), start=1):
        if slot_name is None:
            continue
        slot_reports.append(scan_slot(slot_data, slot_index, slot_name))

    unknown_counter = Counter()
    for slot_report in slot_reports:
        for entry in slot_report["unknown_entries"]:
            unknown_counter[tuple(entry["item_id"])] += 1

    return {
        "save_path": str(save_path),
        "slots": slot_reports,
        "unknown_item_frequency": [
            {"item_id": list(item_id), "count": count}
            for item_id, count in unknown_counter.most_common()
        ],
    }


def build_markdown_report(scan_reports):
    lines = []
    lines.append("# Inventory Scan Report")
    lines.append("")
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
    lines.append("")

    for report in scan_reports:
        save_name = Path(report["save_path"]).name
        lines.append(f"## {save_name}")
        lines.append("")

        for slot_report in report["slots"]:
            lines.append(
                f"- Slot {slot_report['slot']} `{slot_report['character']}`: "
                f"{len(slot_report['known_entries'])} known, "
                f"{len(slot_report['unknown_entries'])} unknown, "
                f"start={slot_report['inventory_start']}, "
                f"score={slot_report['anchor_score']['score']}"
            )

        lines.append("")
        lines.append("Top unknown IDs:")
        top_unknown = report["unknown_item_frequency"][:25]
        if not top_unknown:
            lines.append("- None")
        else:
            for item in top_unknown:
                lines.append(f"- `{item['item_id']}` seen {item['count']} times")
        lines.append("")

    return "\n".join(lines)


def main():
    save_candidates = [
        REPO_ROOT.parent / "ER0000.sl2",
        REPO_ROOT.parent / "ER0000.co2",
        REPO_ROOT / "data" / "save-files" / "Shogun" / "ER0000.co2",
    ]
    save_paths = [path for path in save_candidates if path.exists()]
    if not save_paths:
        raise SystemExit("No save files found to scan.")

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    reports = [scan_save(path) for path in save_paths]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = REPORT_DIR / f"inventory_scan_{timestamp}.json"
    md_path = REPORT_DIR / f"inventory_scan_{timestamp}.md"

    json_path.write_text(json.dumps(reports, indent=2), encoding="utf-8")
    md_path.write_text(build_markdown_report(reports), encoding="utf-8")

    print(f"JSON report: {json_path}")
    print(f"Markdown report: {md_path}")
    for report in reports:
        print(Path(report['save_path']).name)
        for slot_report in report["slots"]:
            print(
                f"  Slot {slot_report['slot']} {slot_report['character']}: "
                f"{len(slot_report['known_entries'])} known / "
                f"{len(slot_report['unknown_entries'])} unknown"
            )


if __name__ == "__main__":
    main()
