#!/usr/bin/env python3
"""
Parallel image generation for Korean flashcard images.

Usage:
    pip install fal-client openpyxl aiohttp
    export FAL_KEY="your-fal-api-key"

    # Generate from prompt spreadsheet (primary workflow)
    python generate_images.py --xlsx korean_anki_image_prompts_v2.xlsx

    # Or from a text file (one prompt per line)
    python generate_images.py -f prompts.txt

    # Options
    --images-per-scene 2    (default: 2)
    --output flashcard_images
    --concurrency 10
    --dry-run               (preview prompts without generating)
"""

import asyncio
import json
import argparse
import string
from pathlib import Path

try:
    import fal_client
except ImportError:
    print("Run: pip install fal-client")
    exit(1)


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
MODEL = "fal-ai/flux-pro/v1.1"
IMAGE_SIZE = "square"
OUTPUT_DIR = Path("flashcard_images")
MAX_CONCURRENT = 10
IMAGES_PER_SCENE = 2


# ---------------------------------------------------------------------------
# Prompt loading
# ---------------------------------------------------------------------------
def load_prompts_from_xlsx(path: str) -> list[tuple[int, str]]:
    """Load prompts from the image prompt spreadsheet.
    Returns [(scene_id, prompt), ...].
    Reads column H (Selected Prompt), falls back to column E (Prompt A)."""
    from openpyxl import load_workbook

    wb = load_workbook(path, read_only=True)
    ws = wb["Image Prompts"]

    scenes = []
    skipped = []

    for row in ws.iter_rows(min_row=2, values_only=True):
        scene_id = row[0]
        if scene_id is None:
            continue
        selected = (row[7] or "").strip()  # Column H
        fallback = (row[4] or "").strip()  # Column E
        prompt = selected or fallback

        if not prompt:
            skipped.append(scene_id)
            continue

        scenes.append((int(scene_id), prompt))

    wb.close()

    if skipped:
        print(f"WARNING: {len(skipped)} scenes have no prompt: {skipped}")

    return scenes


def load_prompts_from_file(path: str) -> list[tuple[int, str]]:
    """Load from text file. Scene IDs assigned sequentially."""
    lines = [
        l.strip() for l in Path(path).read_text().splitlines()
        if l.strip() and not l.startswith("#")
    ]
    return [(i + 1, line) for i, line in enumerate(lines)]


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------
async def generate_one(
    scene_id: int,
    letter: str,
    prompt: str,
    semaphore: asyncio.Semaphore,
    output_dir: Path,
) -> dict:
    """Generate a single image and return result metadata."""
    filename = f"{scene_id:03d}_{letter}.png"
    async with semaphore:
        print(f"  [{filename}] Generating: {prompt[:60]}...")
        try:
            result = await asyncio.to_thread(
                fal_client.subscribe,
                MODEL,
                arguments={
                    "prompt": prompt,
                    "image_size": IMAGE_SIZE,
                    "num_images": 1,
                },
            )
            image_url = result["images"][0]["url"]
            print(f"  [{filename}] ✓ Done")
            return {
                "scene_id": scene_id,
                "letter": letter,
                "filename": filename,
                "prompt": prompt,
                "url": image_url,
                "error": None,
            }
        except Exception as e:
            print(f"  [{filename}] ✗ Failed: {e}")
            return {
                "scene_id": scene_id,
                "letter": letter,
                "filename": filename,
                "prompt": prompt,
                "url": None,
                "error": str(e),
            }


async def generate_batch(
    scenes: list[tuple[int, str]],
    images_per_scene: int,
    output_dir: Path,
) -> list[dict]:
    """Fire off all prompts in parallel (bounded by semaphore)."""
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    letters = string.ascii_lowercase[:images_per_scene]

    tasks = []
    for scene_id, prompt in scenes:
        for letter in letters:
            tasks.append(
                generate_one(scene_id, letter, prompt, semaphore, output_dir)
            )

    return await asyncio.gather(*tasks)


# ---------------------------------------------------------------------------
# Download
# ---------------------------------------------------------------------------
async def download_images(results: list[dict], output_dir: Path):
    """Download generated images to local disk with scene_id naming."""
    import aiohttp

    output_dir.mkdir(parents=True, exist_ok=True)

    async with aiohttp.ClientSession() as session:
        for r in results:
            if not r["url"]:
                continue
            filepath = output_dir / r["filename"]
            async with session.get(r["url"]) as resp:
                with open(filepath, "wb") as f:
                    f.write(await resp.read())
            print(f"  Saved {filepath}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
async def main():
    global MAX_CONCURRENT, MODEL

    parser = argparse.ArgumentParser(description="Generate flashcard images from prompt sheet")
    parser.add_argument("--xlsx", help="Path to image prompts spreadsheet (.xlsx)")
    parser.add_argument("-f", "--file", help="Path to prompts text file (one per line)")
    parser.add_argument("-o", "--output", default="flashcard_images", help="Output directory")
    parser.add_argument("-n", "--concurrency", type=int, default=MAX_CONCURRENT)
    parser.add_argument("--images-per-scene", type=int, default=IMAGES_PER_SCENE)
    parser.add_argument("--model", default=MODEL, help=f"FAL model (default: {MODEL})")
    parser.add_argument("--no-download", action="store_true", help="Skip downloading, just print URLs")
    parser.add_argument("--dry-run", action="store_true", help="Preview prompts without generating")
    args = parser.parse_args()

    MAX_CONCURRENT = args.concurrency
    MODEL = args.model
    output_dir = Path(args.output)

    # Load prompts
    if args.xlsx:
        scenes = load_prompts_from_xlsx(args.xlsx)
    elif args.file:
        scenes = load_prompts_from_file(args.file)
    else:
        print("Provide --xlsx <spreadsheet> or -f <prompts.txt>")
        return

    total_images = len(scenes) * args.images_per_scene

    print(f"\n🎴 {len(scenes)} scenes × {args.images_per_scene} = {total_images} images")
    print(f"   Model: {MODEL}")
    print(f"   Concurrency: {args.concurrency}")
    print(f"   Output: {output_dir}\n")

    if args.dry_run:
        for scene_id, prompt in scenes[:5]:
            print(f"  Scene {scene_id:03d}: {prompt[:80]}...")
        if len(scenes) > 5:
            print(f"  ... ({len(scenes) - 5} more)")
        print(f"\nDry run complete. {total_images} images would be generated.")
        return

    # Generate
    results = await generate_batch(scenes, args.images_per_scene, output_dir)

    # Summary
    succeeded = [r for r in results if r["url"]]
    failed = [r for r in results if r["error"]]
    print(f"\n✓ {len(succeeded)} succeeded, ✗ {len(failed)} failed\n")

    # Save manifest
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"Manifest saved to {manifest_path}")

    # Download
    if not args.no_download and succeeded:
        print("\nDownloading images...")
        await download_images(results, output_dir)

    if failed:
        print(f"\nFailed scenes:")
        for r in failed:
            print(f"  {r['filename']}: {r['error']}")

    print("\nDone! 🎉")


if __name__ == "__main__":
    asyncio.run(main())