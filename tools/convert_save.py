import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import savefile_io


def main():
    parser = argparse.ArgumentParser(description="Convert Elden Ring save file extensions between .sl2 and .co2.")
    parser.add_argument("source", help="Path to the source save file")
    parser.add_argument("target_extension", choices=["sl2", "co2", ".sl2", ".co2"], help="Target extension")
    parser.add_argument("--output-dir", default=None, help="Optional destination directory")
    args = parser.parse_args()

    target = savefile_io.convert_save_file(args.source, args.target_extension, args.output_dir)
    print(target)


if __name__ == "__main__":
    main()
