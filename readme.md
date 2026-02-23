Korean Flashcard Pipeline
Turn Korean tutor session chat logs into Anki flashcards with AI-generated watercolor images.
What it does

You paste your tutor session transcript into Claude
Claude outputs a CSV with vocabulary cards and image prompts
Scripts generate images via FAL API and wire everything into Anki

Setup
bashpip install fal-client openpyxl aiohttp
export FAL_KEY="your-fal-api-key"  # https://fal.ai/dashboard/keys
Workflow
1. Generate the CSV
Paste your tutor chat log into Claude with the prompt template (korean_session_prompt_template.md). Claude outputs a CSV like:
FrontBackFull SentenceExtra Info...Prompt APrompt BImageScene ID____ 다 했어요.거의거의 다 했어요.I'm almost done....Soft watercolor...Soft watercolor...1
2. Curate
Open the CSV in Excel or Google Sheets. Delete words you don't need. Pick which prompt you prefer per scene.
3. Generate images + import to Anki
bash# Generate images (reads Prompt A from the CSV)
python generate_images.py --csv session.csv

# Map images to cards + copy to Anki media folder
python map_images_to_anki.py --csv session.csv --images flashcard_images

# Import korean_anki_final_{job_id}.csv into Anki
Scripts
ScriptWhat it doesgenerate_images.pyReads prompts from CSV, generates images via FAL in parallel, saves to flashcard_images/{job_id}/map_images_to_anki.pyMatches images to cards by Scene ID, adds <img> tags, strips prompt columns, copies images to Anki media, outputs final CSV
File naming
Images follow this pattern:
{scene_id}_{letter}_{korean_word}_{job_id}.png
001_a_거의_20260223_143052.png
001_b_거의_20260223_143052.png
The job ID is shared across filenames, the output folder, and the final CSV so you can trace any image back to the run that created it.
Options
bash# Preview what would be generated (no API calls)
python generate_images.py --csv session.csv --dry-run

# Only generate first 5 scenes (for testing)
python generate_images.py --csv session.csv --limit 5

# Use a different model
python generate_images.py --csv session.csv --model fal-ai/flux-2-pro

# Keep prompt columns in the Anki CSV
python map_images_to_anki.py --csv session.csv --images flashcard_images --keep-prompts

# Specify Anki media folder manually
python map_images_to_anki.py --csv session.csv --images flashcard_images \
    --anki-media "~/Library/Application Support/Anki2/User 1/collection.media"
Image style
All prompts use a consistent Ghibli-adjacent watercolor style:

Soft watercolor hand-drawn illustration in the style of Studio Ghibli, warm muted palette, delicate ink outlines with gentle color washes, [scene], no text no words no letters no numbers, square composition, striking expressive characters with elegant features and detailed eyes

Images depict the sentence scenario, not the target word — so they don't spoil the cloze deletion answer.
Requirements

Python 3.10+
FAL API key
Anki (for import)