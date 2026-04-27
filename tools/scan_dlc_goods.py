import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import hexedit


ERDT_ROOT = Path(r"D:\ELDEN RING\tools\erdt\app\Elden Ring Debug Tool 0.8.6.2")
GOODS_DIR = ERDT_ROOT / "Resources" / "Items" / "Goods"
DLC_GOODS_DIR = ERDT_ROOT / "Resources" / "Items" / "DLC" / "DLCGoods"
REPORT_DIR = REPO_ROOT / "data" / "reports"
ENTRY_SIZE = 12
ENTRY_COUNT = 2048
SEARCH_START = 30000
SEARCH_END = 90000
SAMPLE_ENTRIES = 192
GOODS_FLAG = 0xB0000000


def load_goods_map(*directories):
    goods = {}
    for directory in directories:
        for path in sorted(directory.glob("*.txt")):
            with path.open("r", encoding="utf-8-sig") as handle:
                for raw_line in handle:
                    line = raw_line.strip()
                    if not line:
                        continue
                    item_id_str, item_name = line.split(" ", 1)
                    goods_id = int(item_id_str)
                    save_value = goods_id | GOODS_FLAG
                    goods[save_value] = {
                        "goods_id": goods_id,
                        "save_value": save_value,
                        "name": item_name,
                        "source_file": path.name,
                        "is_dlc": "DLC" in str(path.parent) or path.name.startswith("DLC"),
                    }
    return goods


GOODS_MAP = load_goods_map(GOODS_DIR, DLC_GOODS_DIR)


def read_entry(slot_data, index):
    raw_item = int.from_bytes(slot_data[index : index + 4], "little")
    quantity = int.from_bytes(slot_data[index + 4 : index + 8], "little")
    unique_id = int.from_bytes(slot_data[index + 8 : index + 12], "little")
    return raw_item, quantity, unique_id


def discover_inventory_start(slot_data):
    best = None
    max_start = min(len(slot_data) - (ENTRY_SIZE * SAMPLE_ENTRIES), SEARCH_END)

    for start in range(SEARCH_START, max_start, 4):
        known_count = 0
        plausible_count = 0

        for offset in range(start, start + (ENTRY_SIZE * SAMPLE_ENTRIES), ENTRY_SIZE):
            raw_item, quantity, unique_id = read_entry(slot_data, offset)
            if quantity > 0:
                plausible_count += 1
            if raw_item in GOODS_MAP:
                known_count += 1

        score = (known_count * 8) + plausible_count
        candidate = {"start": start, "score": score, "known_count": known_count}
        if best is None or candidate["score"] > best["score"]:
            best = candidate

    return best


def scan_save(save_path):
    save_path = Path(save_path)
    names = hexedit.get_names(str(save_path))
    slots = hexedit.get_slot_ls(str(save_path))
    scan_report = {"save_path": str(save_path), "slots": []}

    for slot_index, (slot_name, slot_data) in enumerate(zip(names, slots), start=1):
        if slot_name is None:
            continue

        anchor = discover_inventory_start(slot_data)
        start = anchor["start"]
        entries = []

        for i in range(ENTRY_COUNT):
            index = start + (i * ENTRY_SIZE)
            raw_item, quantity, unique_id = read_entry(slot_data, index)
            if quantity <= 0:
                continue

            item_info = GOODS_MAP.get(raw_item)
            if item_info is None:
                continue

            entries.append(
                {
                    "index": index,
                    "raw_item": raw_item,
                    "goods_id": item_info["goods_id"],
                    "name": item_info["name"],
                    "quantity": quantity,
                    "unique_id": unique_id,
                    "source_file": item_info["source_file"],
                    "is_dlc": item_info["is_dlc"],
                }
            )

        scan_report["slots"].append(
            {
                "slot": slot_index,
                "character": slot_name,
                "inventory_start": start,
                "anchor_score": anchor["score"],
                "matched_entries": entries,
                "dlc_entries": [entry for entry in entries if entry["is_dlc"]],
            }
        )

    return scan_report


def build_markdown_report(reports):
    lines = ["# DLC Goods Scan Report", ""]
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
    lines.append("")

    for report in reports:
        lines.append(f"## {Path(report['save_path']).name}")
        lines.append("")
        for slot in report["slots"]:
            lines.append(
                f"### Slot {slot['slot']} `{slot['character']}`"
            )
            lines.append("")
            lines.append(
                f"- Inventory start: `{slot['inventory_start']}`"
            )
            lines.append(
                f"- Matched goods entries: `{len(slot['matched_entries'])}`"
            )
            lines.append(
                f"- Matched DLC goods entries: `{len(slot['dlc_entries'])}`"
            )
            lines.append("")

            if slot["dlc_entries"]:
                for entry in slot["dlc_entries"]:
                    lines.append(
                        f"- `{entry['name']}` goodsId=`{entry['goods_id']}` qty=`{entry['quantity']}` raw=`0x{entry['raw_item']:08X}`"
                    )
            else:
                lines.append("- No DLC goods matched in this slot")
            lines.append("")

    return "\n".join(lines)


def main():
    save_candidates = [
        REPO_ROOT.parent / "ER0000.sl2",
        REPO_ROOT.parent / "ER0000.co2",
    ]
    save_paths = [path for path in save_candidates if path.exists()]
    if not save_paths:
        raise SystemExit("No save files found to scan.")

    reports = [scan_save(path) for path in save_paths]
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = REPORT_DIR / f"dlc_goods_scan_{timestamp}.json"
    md_path = REPORT_DIR / f"dlc_goods_scan_{timestamp}.md"

    json_path.write_text(json.dumps(reports, indent=2), encoding="utf-8")
    md_path.write_text(build_markdown_report(reports), encoding="utf-8")

    print(f"JSON report: {json_path}")
    print(f"Markdown report: {md_path}")
    for report in reports:
        print(Path(report["save_path"]).name)
        for slot in report["slots"]:
            print(
                f"  Slot {slot['slot']} {slot['character']}: "
                f"{len(slot['matched_entries'])} goods matched / "
                f"{len(slot['dlc_entries'])} dlc goods matched"
            )


if __name__ == "__main__":
    main()
