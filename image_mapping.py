#!/usr/bin/env python3
"""
Map generated scene images to Anki cards and copy to Anki media folder.

Usage:
    python map_images_to_anki.py \
        --csv korean_anki_cloze_v2.csv \
        --images ./generated_images/ \
        --output korean_anki_final.csv \
        --anki-media "~/Library/Application Support/Anki2/User 1/collection.media"

What this script does:
    1. Reads the CSV (with Scene ID column)
    2. Scans the images folder for {scene_id}_a.png, {scene_id}_b.png, etc.
    3. Groups images by scene ID
    4. Adds an "Image" column with <img> tags for all images matching that scene
    5. Copies all matched images into the Anki media folder
    6. Writes the updated CSV ready for Anki import

Filename convention expected:
    001_a.png, 001_b.png, 001_c.png, 001_d.png
    002_a.png, 002_b.png, ...
    (zero-padded 3-digit scene ID + underscore + letter)
"""

import argparse
import csv
import shutil
import re
from pathlib import Path
from collections import defaultdict


def find_anki_media_folder() -> Path | None:
    """Try to auto-detect Anki media folder on common OS paths."""
    candidates = [
        Path.home() / "Library" / "Application Support" / "Anki2",  # macOS
        Path.home() / ".local" / "share" / "Anki2",                 # Linux
        Path.home() / "AppData" / "Roaming" / "Anki2",              # Windows
    ]
    for base in candidates:
        if base.exists():
            # Find first profile folder
            for profile in sorted(base.iterdir()):
                media = profile / "collection.media"
                if media.exists():
                    return media
    return None


def scan_images(images_dir: Path) -> dict[int, list[Path]]:
    """Scan directory for scene images. Returns {scene_id: [path, ...]} sorted by letter."""
    pattern = re.compile(r"^(\d+)_([a-z])\.(png|jpg|jpeg|webp)$", re.IGNORECASE)
    scene_images = defaultdict(list)

    for f in sorted(images_dir.iterdir()):
        match = pattern.match(f.name)
        if match:
            scene_id = int(match.group(1))
            scene_images[scene_id].append(f)

    return dict(scene_images)


def build_img_tags(filenames: list[str]) -> str:
    """Build HTML img tags for Anki field."""
    return " ".join(f'<img src="{name}">' for name in filenames)


def main():
    parser = argparse.ArgumentParser(description="Map scene images to Anki CSV cards")
    parser.add_argument("--csv", required=True, help="Input CSV with Scene ID column")
    parser.add_argument("--images", required=True, help="Directory with generated images")
    parser.add_argument("--output", required=True, help="Output CSV path")
    parser.add_argument("--anki-media", default=None,
                        help="Anki collection.media folder (auto-detected if omitted)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview what would happen without copying files")
    args = parser.parse_args()

    csv_path = Path(args.csv)
    images_dir = Path(args.images)
    output_path = Path(args.output)

    # Resolve Anki media folder
    if args.anki_media:
        anki_media = Path(args.anki_media)
    else:
        anki_media = find_anki_media_folder()
        if anki_media:
            print(f"Auto-detected Anki media: {anki_media}")
        else:
            print("ERROR: Could not auto-detect Anki media folder.")
            print("       Pass --anki-media /path/to/collection.media explicitly.")
            return

    if not anki_media.exists():
        print(f"ERROR: Anki media folder does not exist: {anki_media}")
        return

    # Scan images
    scene_images = scan_images(images_dir)
    total_images = sum(len(v) for v in scene_images.values())
    print(f"Found {total_images} images across {len(scene_images)} scenes")

    # Read CSV
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Track stats
    cards_with_images = 0
    cards_without_images = 0
    images_copied = 0
    files_to_copy = set()

    # Build output rows
    output_rows = []
    for row in rows:
        scene_id = int(row["Scene ID"])
        images = scene_images.get(scene_id, [])

        if images:
            filenames = [img.name for img in images]
            row["Image"] = build_img_tags(filenames)
            cards_with_images += 1
            files_to_copy.update(images)
        else:
            row["Image"] = ""
            cards_without_images += 1

        output_rows.append(row)

    # Copy images to Anki media
    if not args.dry_run:
        for img_path in sorted(files_to_copy):
            dest = anki_media / img_path.name
            shutil.copy2(img_path, dest)
            images_copied += 1
    else:
        images_copied = len(files_to_copy)

    # Write output CSV
    fieldnames = list(rows[0].keys()) + (["Image"] if "Image" not in rows[0] else [])
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(fieldnames)
        for row in output_rows:
            writer.writerow([row.get(field, "") for field in fieldnames])

    # Report
    prefix = "[DRY RUN] " if args.dry_run else ""
    print(f"\n{prefix}Results:")
    print(f"  Cards with images:    {cards_with_images}")
    print(f"  Cards without images: {cards_without_images}")
    print(f"  Unique images copied: {images_copied}")
    print(f"  Output CSV:           {output_path}")
    print(f"  Anki media folder:    {anki_media}")

    if cards_without_images > 0:
        missing = set()
        for row in output_rows:
            if not row.get("Image"):
                missing.add(int(row["Scene ID"]))
        print(f"\n  Missing scenes: {sorted(missing)}")


if __name__ == "__main__":
    main()