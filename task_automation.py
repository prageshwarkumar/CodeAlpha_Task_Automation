
import argparse
import logging
import shutil
import sys
from pathlib import Path

JPG_EXTENSIONS = {".jpg", ".jpeg"}

# ---------------------------------------------------------------- logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("automation.log", encoding="utf-8"),
    ],
)
log = logging.getLogger("jpg-mover")


def unique_path(path: Path) -> Path:
    """If a file already exists, return photo_1.jpg, photo_2.jpg ... instead of overwriting."""
    if not path.exists():
        return path
    counter = 1
    while True:
        candidate = path.with_name(f"{path.stem}_{counter}{path.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def find_jpg_files(src: Path, dest: Path, recursive: bool) -> list[Path]:
    pattern = "**/*" if recursive else "*"
    return [
        f for f in src.glob(pattern)
        if f.is_file()
        and f.suffix.lower() in JPG_EXTENSIONS
        and dest not in f.parents          # skip files already inside destination
    ]


def move_jpg_files(src: str, dest: str, recursive: bool = False, dry_run: bool = False) -> dict:
    src_path = Path(src).expanduser().resolve()
    dest_path = Path(dest).expanduser().resolve()
    report = {"found": 0, "moved": 0, "failed": 0, "size_mb": 0.0}

    if not src_path.is_dir():
        log.error("Source folder not found: %s", src_path)
        return report

    if src_path == dest_path:
        log.error("Source and destination cannot be the same folder.")
        return report

    files = find_jpg_files(src_path, dest_path, recursive)
    report["found"] = len(files)

    if not files:
        log.warning("No .jpg files found in %s", src_path)
        return report

    if not dry_run:
        dest_path.mkdir(parents=True, exist_ok=True)

    for f in files:
        target = unique_path(dest_path / f.name)
        try:
            size = f.stat().st_size
            if dry_run:
                log.info("[DRY RUN] %s -> %s", f, target)
            else:
                shutil.move(str(f), str(target))
                log.info("Moved: %s -> %s", f.name, target.name)
            report["moved"] += 1
            report["size_mb"] += size / (1024 * 1024)
        except (PermissionError, OSError) as err:
            report["failed"] += 1
            log.error("Could not move %s: %s", f.name, err)

    # ---- summary
    action = "Would move" if dry_run else "Moved"
    print("\n" + "=" * 40)
    print(f" Files found : {report['found']}")
    print(f" {action:<12}: {report['moved']}")
    print(f" Failed      : {report['failed']}")
    print(f" Total size  : {report['size_mb']:.2f} MB")
    print("=" * 40)
    return report


def main():
    parser = argparse.ArgumentParser(description="CodeAlpha Task 3 - Move .jpg files to a new folder")
    parser.add_argument("--src", help="Source folder containing the images")
    parser.add_argument("--dest", help="Destination folder (created if missing)")
    parser.add_argument("--recursive", action="store_true", help="Include sub-folders")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, do not move files")
    args = parser.parse_args()

    # interactive mode if folders were not given
    src = args.src or input("Source folder path: ").strip().strip('"')
    dest = args.dest or input("Destination folder path: ").strip().strip('"')
    dry_run = args.dry_run

    if not args.src and not dry_run:
        dry_run = input("Do a dry run first? (y/n): ").strip().lower() == "y"

    move_jpg_files(src, dest, args.recursive, dry_run)


if __name__ == "__main__":
    main()