# Korean Flashcard Pipeline

Turn Korean tutor session chat logs into Anki flashcards with stylized images. 

---

## What It Does

1. You paste your tutor session transcript into Claude
2. Claude outputs a structured CSV with vocabulary cards + image prompts
3. Scripts generate images via the FAL API
4. Everything is wired into Anki for import
---

# Setup

## Install Dependencies

```bash
pip install fal-client openpyxl aiohttp
```

## Set Your FAL API Key

```bash
export FAL_KEY="your-fal-api-key"
# https://fal.ai/dashboard/keys
```

---

# Workflow

## 1️⃣ Generate the CSV

Paste your tutor chat log into Claude using:

```
korean_session_prompt_template.md
```

Claude outputs a CSV like:

```
Front,Back,Full Sentence,Extra Info,...,Prompt A,Prompt B,Image,Scene ID
____ 다 했어요.,거의,거의 다 했어요.,I'm almost done.,...,Soft watercolor...,Soft watercolor..., ,1
```

---

## 2️⃣ Curate the CSV

Open in Excel or Google Sheets:

* Delete words you don’t need
* Choose which prompt (A or B) you prefer per scene
* Save as `session.csv`

---

## 3️⃣ Generate Images + Import to Anki

### Generate Images

Reads **Prompt A** from the CSV and generates images via FAL in parallel:

```bash
python generate_images.py --csv session.csv
```

---

### Map Images to Cards + Prepare for Anki

```bash
python map_images_to_anki.py --csv session.csv --images flashcard_images
```

This:

* Matches images to cards by Scene ID
* Adds `<img>` tags
* Strips prompt columns
* Copies images to Anki media folder
* Outputs:

```
korean_anki_final_{job_id}.csv
```

Import that file into Anki.

---

# Scripts

| Script                  | What It Does                                                                                              |
| ----------------------- | --------------------------------------------------------------------------------------------------------- |
| `generate_images.py`    | Reads prompts from CSV, generates images via FAL in parallel, saves to `flashcard_images/{job_id}/`       |
| `map_images_to_anki.py` | Matches images to cards by Scene ID, inserts `<img>` tags, copies images to Anki media, outputs final CSV |

---

# File Naming

Images follow this pattern:

```
{scene_id}{letter}{korean_word}_{job_id}.png
```

Example:

```
001_a_거의_20260223_143052.png
001_b_거의_20260223_143052.png
```

The `job_id` is shared across:

* Image filenames
* Output folder
* Final CSV

This allows tracing any image back to its generation run.

---

# Options

## Preview Only (No API Calls)

```bash
python generate_images.py --csv session.csv --dry-run
```

---

## Limit to First 5 Scenes

```bash
python generate_images.py --csv session.csv --limit 5
```

---

## Use a Different Model

```bash
python generate_images.py --csv session.csv --model fal-ai/flux-2-pro
```

---

## Keep Prompt Columns in Final Anki CSV

```bash
python map_images_to_anki.py --csv session.csv --images flashcard_images --keep-prompts
```

---

## Specify Anki Media Folder Manually

```bash
python map_images_to_anki.py \
  --csv session.csv \
  --images flashcard_images \
  --anki-media "~/Library/Application Support/Anki2/User 1/collection.media"
```

---

# Image Style

All prompts use a consistent Ghibli-adjacent watercolor style:

> Soft watercolor hand-drawn illustration in the style of Studio Ghibli, warm muted palette, delicate ink outlines with gentle color washes, [scene], no text no words no letters no numbers, square composition, striking expressive characters with elegant features and detailed eyes

Images depict the **sentence scenario**, not the isolated target word, so they don’t spoil the cloze deletion answer.

---

# Requirements

* Python 3.10+
* FAL API key
* Anki (for import)

