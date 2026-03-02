#!/usr/bin/env python3
"""
Map generated scene images to Anki cards and copy to Anki media folder.

Usage:
    python map_images_to_anki.py \
        --csv session_2026-02-23.csv \
        --images flashcard_images

What this does:
    1. Reads the session CSV (with Scene ID, Tag, Prompt A, Prompt B)
    2. Scans the images folder for {scene_id}_{letter}_{korean}_{job_id}.png
    3. Populates the "Front (Picture)" column with <img> tags
    4. Strips Prompt A / Prompt B columns (not needed for Anki import)
    5. Copies matched images into Anki's collection.media folder
    6. Writes final CSV: korean_anki_final_{job_id}.csv

Input CSV columns (from system prompt):
    Front, Back, Full Sentence, Word Pronunciation, Front (Definitions),
    Front (Picture), Sentence Pronunciation, Word English Translation,
    Full English Translation, Scene ID, Tag, Prompt A, Prompt B

Output CSV columns (Anki-ready, matches note type field order):
    1: Front
    2: Back
    3: Full Sentence
    4: Word Pronunciation
    5: Front (Definitions)
    6: Front (Picture)
    7: Sentence Pronunciation
    8: Word English Translation
    9: Full English Translation
    10: Scene ID
    11: Tag
"""

import argparse
import csv
import re
import shutil
from pathlib import Path
from collections import defaultdict


def find_anki_media_folder() -> Path | None:
    """Auto-detect Anki media folder."""
    candidates = [
        Path.home() / "Library" / "Application Support" / "Anki2",  # macOS
        Path.home() / ".local" / "share" / "Anki2",                 # Linux
        Path.home() / "AppData" / "Roaming" / "Anki2",              # Windows
    ]
    for base in candidates:
        if base.exists():
            for profile in sorted(base.iterdir()):
                media = profile / "collection.media"
                if media.exists():
                    return media
    return None


def scan_images(images_dir: Path) -> dict[int, list[Path]]:
    """Scan directory for scene images. Returns {scene_id: [path, ...]}.
    Handles all filename formats:
        001_a.png
        001_a_20260223_143052.png
        001_a_거의_20260223_143052.png
    Scans subdirectories (for timestamped job folders)."""
    pattern = re.compile(
        r"^(\d+)_([a-z])(?:_[^.]+)?\.(png|jpg|jpeg|webp)$",
        re.IGNORECASE
    )
    scene_images = defaultdict(list)

    dirs_to_scan = [images_dir]
    if images_dir.exists():
        for child in images_dir.iterdir():
            if child.is_dir():
                dirs_to_scan.append(child)

    for scan_dir in dirs_to_scan:
        for f in sorted(scan_dir.iterdir()):
            if f.is_file():
                match = pattern.match(f.name)
                if match:
                    scene_id = int(match.group(1))
                    scene_images[scene_id].append(f)

    return dict(scene_images)


def build_img_tags(filenames: list[str]) -> str:
    return " ".join(f'<img src="{name}">' for name in filenames)


# Columns to output for Anki import (matches note type field order)
# Prompt A and Prompt B are stripped
ANKI_COLUMNS = [
    "Front",
    "Back",
    "Full Sentence",
    "Word Pronunciation",
    "Front (Definitions)",
    "Front (Picture)",
    "Sentence Pronunciation",
    "Word English Translation",
    "Full English Translation",
    "Scene ID",
    "Tag",
]

# Columns that exist in the input CSV but should be stripped for Anki
STRIP_COLUMNS = ["Prompt A", "Prompt B"]


def main():
    parser = argparse.ArgumentParser(description="Map scene images to Anki CSV cards")
    parser.add_argument("--csv", required=True, help="Input session CSV")
    parser.add_argument("--images", required=True, help="Directory with generated images")
    parser.add_argument("--output", default=None, help="Output CSV (default: korean_anki_final_{job_id}.csv)")
    parser.add_argument("--job-id", default=None, help="Job ID (auto-detected from images folder)")
    parser.add_argument("--anki-media", default=None, help="Anki collection.media folder")
    parser.add_argument("--keep-prompts", action="store_true", help="Keep Prompt A/B columns in output")
    parser.add_argument("--dry-run", action="store_true", help="Preview without copying files")
    args = parser.parse_args()

    csv_path = Path(args.csv)
    images_dir = Path(args.images)

    # Resolve job ID
    job_id = args.job_id
    if not job_id and images_dir.exists():
        subdirs = sorted([d.name for d in images_dir.iterdir() if d.is_dir()])
        if subdirs:
            job_id = subdirs[-1]
            print(f"Auto-detected job ID: {job_id}")

    if not job_id:
        from datetime import datetime
        job_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_path = Path(args.output) if args.output else Path(f"korean_anki_final_{job_id}.csv")

    # Resolve Anki media
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

    # Validate expected columns
    input_cols = set(rows[0].keys()) if rows else set()
    missing = set(ANKI_COLUMNS) - input_cols
    if missing:
        print(f"WARNING: Missing expected columns in input CSV: {missing}")
        print(f"         Available columns: {sorted(input_cols)}")

    # Determine output columns
    if args.keep_prompts:
        out_columns = ANKI_COLUMNS + STRIP_COLUMNS
    else:
        out_columns = ANKI_COLUMNS

    # Build output rows
    cards_with_images = 0
    cards_without_images = 0
    files_to_copy = set()
    output_rows = []

    for row in rows:
        scene_id = int(row.get("Scene ID", 0))
        images = scene_images.get(scene_id, [])

        if images:
            filenames = [img.name for img in images]
            row["Front (Picture)"] = build_img_tags(filenames)
            cards_with_images += 1
            files_to_copy.update(images)
        else:
            row["Front (Picture)"] = row.get("Front (Picture)", "")
            cards_without_images += 1

        output_rows.append(row)

    # Copy images to Anki media
    images_copied = 0
    if not args.dry_run:
        for img_path in sorted(files_to_copy):
            dest = anki_media / img_path.name
            shutil.copy2(img_path, dest)
            images_copied += 1
    else:
        images_copied = len(files_to_copy)

    # Write output CSV
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(out_columns)
        for row in output_rows:
            writer.writerow([row.get(col, "") for col in out_columns])

    # Report
    prefix = "[DRY RUN] " if args.dry_run else ""
    print(f"\n{prefix}Results:")
    print(f"  Job ID:               {job_id}")
    print(f"  Cards with images:    {cards_with_images}")
    print(f"  Cards without images: {cards_without_images}")
    print(f"  Unique images copied: {images_copied}")
    print(f"  Output CSV:           {output_path}")
    print(f"  Anki media folder:    {anki_media}")
    print(f"  Prompt columns:       {'kept' if args.keep_prompts else 'stripped'}")
    print(f"  Output columns:       {len(out_columns)}")

    # Tag summary
    tag_counts = defaultdict(int)
    for row in output_rows:
        tags = row.get("Tag", "")
        for tag in [t.strip() for t in tags.split(",") if t.strip()]:
            tag_counts[tag] += 1
    if tag_counts:
        print(f"\n  Tag distribution:")
        for tag, count in sorted(tag_counts.items(), key=lambda x: -x[1]):
            print(f"    {tag}: {count}")

    if cards_without_images > 0:
        missing_scenes = set()
        for row in output_rows:
            if not row.get("Front (Picture)"):
                missing_scenes.add(int(row.get("Scene ID", 0)))
        print(f"\n  Missing scenes: {sorted(missing_scenes)}")


if __name__ == "__main__":
    main()