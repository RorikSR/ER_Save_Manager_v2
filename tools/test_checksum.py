import hashlib
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from logic import checksum


def file_md5(path):
    return hashlib.md5(Path(path).read_bytes()).hexdigest()


def run_case(source_path, output_dir):
    source_path = Path(source_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    test_path = output_dir / source_path.name
    test_path.write_bytes(source_path.read_bytes())

    original = test_path.read_bytes()
    before = checksum.verify_data(original)
    after_once = checksum.recalculate_data(original)
    after_once_verify = checksum.verify_data(after_once)
    after_twice = checksum.recalculate_data(after_once)
    after_twice_verify = checksum.verify_data(after_twice)
    test_path.write_bytes(after_twice)

    return {
        "file": str(source_path),
        "before_valid": before["valid"],
        "before_issue_count": len(before["issues"]),
        "after_once_valid": after_once_verify["valid"],
        "after_twice_valid": after_twice_verify["valid"],
        "idempotent": after_once == after_twice,
        "source_md5": hashlib.md5(original).hexdigest(),
        "recalculated_md5": file_md5(test_path),
    }


def main():
    sources = [
        Path(r"D:\ELDEN RING\ER0000.sl2"),
        Path(r"D:\ELDEN RING\ER0000.co2"),
    ]
    output_dir = REPO_ROOT / "data" / "reports" / "checksum-tests"
    results = [run_case(path, output_dir) for path in sources if path.exists()]
    report_path = REPO_ROOT / "data" / "reports" / "checksum_report.json"
    report_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(report_path)
    for result in results:
        print(result)


if __name__ == "__main__":
    main()
