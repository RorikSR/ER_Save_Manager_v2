from __future__ import annotations

import json
from collections import Counter
from datetime import datetime
from pathlib import Path

import hexedit
import itemdata
from logic import checksum as checksum_logic
from app_paths import DATA_DIR, ensure_runtime_data


ensure_runtime_data()
REPORT_DIR = DATA_DIR / "reports"


def _entry_source(category, entry):
    if category == "Custom Items":
        return "Custom"
    if isinstance(entry, dict):
        return entry.get("source", "Base Game")
    return "Base Game"


def _game_label(source):
    return "DLC" if "Shadow of the Erdtree" in source else source


def catalog_rows():
    rows = []
    database = itemdata.load_item_database()
    for category, items in database.items():
        for name, entry in items.items():
            descriptor = hexedit.normalize_item_descriptor(entry)
            source = _entry_source(category, entry)
            rows.append(
                {
                    "name": name,
                    "category": category,
                    "source": source,
                    "game": _game_label(source),
                    "ids": descriptor["item_id"],
                    "goods_id": descriptor["goods_id"],
                    "raw_item": descriptor["raw_item"],
                }
            )

    return sorted(rows, key=lambda row: (row["category"].lower(), row["name"].lower()))


def catalog_lookup_by_raw():
    lookup = {}
    for row in catalog_rows():
        lookup.setdefault(row["raw_item"], row)
    return lookup


def inventory_rows_for_slot(save_path, slot):
    lookup = catalog_lookup_by_raw()
    rows = []
    for entry in hexedit.get_inventory(str(save_path), slot):
        metadata = lookup.get(entry["raw_item"])
        rows.append(
            {
                "name": metadata["name"] if metadata else entry.get("name", "?"),
                "category": metadata["category"] if metadata else "Unknown",
                "source": metadata["source"] if metadata else "Unknown",
                "game": metadata["game"] if metadata else "Unknown",
                "raw_item": entry["raw_item"],
                "goods_id": entry["goods_id"],
                "item_id": entry["item_id"],
                "quantity": entry["quantity"],
                "index": entry["index"],
                "known": metadata is not None or entry.get("name") != "?",
            }
        )

    return sorted(rows, key=lambda row: (row["name"].lower(), row["raw_item"]))


def set_inventory_quantity(save_path, slot, raw_item, quantity, index=None):
    quantity = max(0, int(quantity))
    if index is None:
        result = hexedit.additem(str(save_path), int(slot), int(raw_item), quantity)
    else:
        result = hexedit.set_item_quantity_at_index(
            str(save_path),
            int(slot),
            int(raw_item),
            int(index),
            quantity,
        )
    if result is None:
        return {"updated": False, "checksum": None}

    checksum = checksum_logic.verify_data(Path(save_path).read_bytes())
    return {"updated": True, "checksum": checksum}


def scan_save_inventory(save_path):
    save_path = Path(save_path)
    lookup = catalog_lookup_by_raw()
    names = hexedit.get_names(str(save_path))
    report = {
        "save_path": str(save_path),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "slots": [],
        "summary": {
            "known": 0,
            "unknown": 0,
            "dlc": 0,
            "duplicates": 0,
            "rare": 0,
        },
        "unknown_item_frequency": [],
        "duplicate_raw_items": [],
        "rare_entries": [],
    }

    raw_counter = Counter()
    unknown_counter = Counter()

    for slot_index, slot_name in enumerate(names, start=1):
        if not slot_name:
            continue

        inventory_entries = hexedit.get_inventory(str(save_path), slot_index)
        slot_entries = []
        for entry in inventory_entries:
            raw_item = entry["raw_item"]
            raw_counter[raw_item] += 1
            metadata = lookup.get(raw_item)
            known = metadata is not None or entry.get("name") != "?"
            source = metadata["source"] if metadata else "Unknown"
            category = metadata["category"] if metadata else "Unknown"
            game = metadata["game"] if metadata else "Unknown"

            if known:
                report["summary"]["known"] += 1
            else:
                report["summary"]["unknown"] += 1
                unknown_counter[raw_item] += 1

            if game == "DLC":
                report["summary"]["dlc"] += 1

            rare_reasons = []
            if not known:
                rare_reasons.append("unknown")
            if entry["quantity"] > 999999:
                rare_reasons.append("very_high_quantity")
            if entry["raw_item"] & hexedit.GOODS_FLAG != hexedit.GOODS_FLAG:
                rare_reasons.append("non_goods_raw_prefix")

            normalized_entry = {
                "slot": slot_index,
                "character": slot_name,
                "name": metadata["name"] if metadata else entry.get("name", "?"),
                "category": category,
                "source": source,
                "game": game,
                "raw_item": raw_item,
                "goods_id": entry["goods_id"],
                "item_id": entry["item_id"],
                "quantity": entry["quantity"],
                "index": entry["index"],
                "known": known,
                "rare_reasons": rare_reasons,
            }

            if rare_reasons:
                report["summary"]["rare"] += 1
                report["rare_entries"].append(normalized_entry)

            slot_entries.append(normalized_entry)

        report["slots"].append(
            {
                "slot": slot_index,
                "character": slot_name,
                "total_entries": len(slot_entries),
                "entries": slot_entries,
            }
        )

    duplicate_raw_items = [
        {"raw_item": raw_item, "count": count, "metadata": lookup.get(raw_item)}
        for raw_item, count in raw_counter.most_common()
        if count > 1
    ]
    report["duplicate_raw_items"] = duplicate_raw_items
    report["summary"]["duplicates"] = len(duplicate_raw_items)
    report["unknown_item_frequency"] = [
        {"raw_item": raw_item, "count": count}
        for raw_item, count in unknown_counter.most_common()
    ]
    return report


def write_inventory_scan_report(report):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = REPORT_DIR / f"inventory_pro_scan_{timestamp}.json"
    md_path = REPORT_DIR / f"inventory_pro_scan_{timestamp}.md"

    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    md_path.write_text(build_markdown_report(report), encoding="utf-8")
    return json_path, md_path


def build_markdown_report(report):
    summary = report["summary"]
    lines = [
        "# Inventory Pro Scan",
        "",
        f"Generated: {report['generated_at']}",
        f"Save: `{report['save_path']}`",
        "",
        "## Summary",
        "",
        f"- Known entries: {summary['known']}",
        f"- Unknown entries: {summary['unknown']}",
        f"- DLC entries: {summary['dlc']}",
        f"- Duplicate raw item groups: {summary['duplicates']}",
        f"- Rare entries: {summary['rare']}",
        "",
    ]

    for slot in report["slots"]:
        lines.extend(
            [
                f"## Slot {slot['slot']}: {slot['character']}",
                "",
                f"Total entries: {slot['total_entries']}",
                "",
            ]
        )
        unknown = [entry for entry in slot["entries"] if not entry["known"]]
        if unknown:
            lines.append("Unknown entries:")
            for entry in unknown[:30]:
                lines.append(
                    f"- raw={entry['raw_item']} goods={entry['goods_id']} qty={entry['quantity']} index={entry['index']}"
                )
            lines.append("")

    lines.append("## Top Unknown Raw Items")
    lines.append("")
    for item in report["unknown_item_frequency"][:50]:
        lines.append(f"- raw={item['raw_item']} seen {item['count']} time(s)")
    if not report["unknown_item_frequency"]:
        lines.append("- None")

    return "\n".join(lines)
