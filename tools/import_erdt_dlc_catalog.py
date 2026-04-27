import json
from collections import OrderedDict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
ERDT_ROOT = Path(r"D:\ELDEN RING\tools\erdt\app\Elden Ring Debug Tool 0.8.6.2")
DLC_ROOT = ERDT_ROOT / "Resources" / "Items" / "DLC"
OUTPUT_PATH = REPO_ROOT / "data" / "items" / "shadow_of_the_erdtree.json"
GOODS_FLAG = 0xB0000000


CATEGORY_MAP = OrderedDict(
    [
        ("DLCArmor.txt", "Armor"),
        ("DLCGems.txt", "Ashes of War"),
        ("DLCMagic.txt", "Magic"),
        ("DLCTalismans.txt", "Talismans"),
        ("DLCAshes.txt", "Spirit Ashes"),
        ("DLCConsumables.txt", "Consumables"),
        ("DLCCookbooks.txt", "Cookbooks"),
        ("DLCCraftingMaterials.txt", "Crafting Materials"),
        ("DLCCrystalTears.txt", "Crystal Tears"),
        ("DLCGestures.txt", "Gestures"),
        ("DLCKeyItems.txt", "Key Items"),
        ("DLCMerchantItems.txt", "Merchant Items"),
        ("DLCNotesPaintings.txt", "Notes & Paintings"),
        ("DLCTools.txt", "Tools"),
        ("DLCUpgradeMaterials.txt", "Upgrade Materials"),
        ("DLCAmmo.txt", "Ammo"),
        ("DLCMeleeWeapons.txt", "Melee Weapons"),
        ("DLCRangedWeapons.txt", "Ranged Weapons"),
        ("DLCShields.txt", "Shields"),
        ("DLCSpellTools.txt", "Spell Tools"),
    ]
)


def load_entries(path):
    entries = OrderedDict()
    with path.open("r", encoding="utf-8-sig") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            item_id_str, item_name = line.split(" ", 1)
            item_id = int(item_id_str)
            entries[item_name] = {
                "ids": [item_id & 0xFF, (item_id >> 8) & 0xFF],
                "goods_id": item_id,
                "raw_item": GOODS_FLAG | item_id,
                "source": "Shadow of the Erdtree",
                "source_file": path.name,
            }
    return entries


def build_catalog():
    catalog = OrderedDict()
    catalog["_meta"] = {
        "source": "Generated from Elden Ring Debug Tool resources",
        "tool_root": str(ERDT_ROOT),
        "notes": [
            "This file is generated automatically from the DLC resource text files bundled with Elden Ring Debug Tool.",
            "raw_item is the 32-bit inventory value currently used by the save editor."
        ],
    }

    for file_name, category_name in CATEGORY_MAP.items():
        matches = list(DLC_ROOT.rglob(file_name))
        if not matches:
            catalog[category_name] = {}
            continue
        catalog[category_name] = load_entries(matches[0])

    return catalog


def main():
    catalog = build_catalog()
    OUTPUT_PATH.write_text(json.dumps(catalog, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")
    for category, entries in catalog.items():
        if category == "_meta":
            continue
        print(f"{category}: {len(entries)}")


if __name__ == "__main__":
    main()
