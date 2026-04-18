import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "data" / "config.json"
ITEM_DATA_DIR = BASE_DIR / "data" / "items"
CATALOG_FILES = ("base_game.json", "shadow_of_the_erdtree.json")


def _normalize_item_ids(value):
    if isinstance(value, list) and len(value) == 2 and all(isinstance(i, int) for i in value):
        return value

    if isinstance(value, dict):
        ids = value.get("ids")
        if isinstance(ids, list) and len(ids) == 2 and all(isinstance(i, int) for i in ids):
            return ids

    return None


def _normalize_item_entry(value):
    ids = _normalize_item_ids(value)
    if ids is None:
        return None

    if isinstance(value, list):
        return ids

    normalized = {"ids": ids}
    if "goods_id" in value and isinstance(value["goods_id"], int):
        normalized["goods_id"] = value["goods_id"]
    if "raw_item" in value and isinstance(value["raw_item"], int):
        normalized["raw_item"] = value["raw_item"]
    if "source" in value and isinstance(value["source"], str):
        normalized["source"] = value["source"]

    return normalized


def _load_catalog_file(path):
    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8") as handle:
        raw_data = json.load(handle)

    normalized = {}
    for category, items in raw_data.items():
        if category.startswith("_") or not isinstance(items, dict):
            continue

        normalized[category] = {}
        for item_name, item_value in items.items():
            entry = _normalize_item_entry(item_value)
            if entry is not None:
                normalized[category][item_name] = entry

    return normalized


def load_item_database(config_path=CONFIG_PATH):
    database = {}

    for file_name in CATALOG_FILES:
        catalog = _load_catalog_file(ITEM_DATA_DIR / file_name)
        for category, items in catalog.items():
            database.setdefault(category, {}).update(items)

    if config_path.exists():
        with config_path.open("r", encoding="utf-8") as handle:
            config = json.load(handle)

        custom_items = config.get("custom_ids", {})
        normalized_custom_items = {}
        for item_name, item_value in custom_items.items():
            entry = _normalize_item_entry(item_value)
            if entry is not None:
                normalized_custom_items[item_name] = entry

        if normalized_custom_items:
            database["Custom Items"] = normalized_custom_items

    return database


class Items:
    def __init__(self):
        self.db = load_item_database()
        self.categories = list(self.db.keys())

    def get_item_ls(self, cat):
        return list(self.db.get(cat, {}))
