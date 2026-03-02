
INSTRUCTIONS
You are converting a Korean tutor session transcript into Anki flashcard CSV format.
OUTPUT FORMAT
Generate a CSV with these exact columns in this order:
Front, Back, Full Sentence, Extra Info, Target Word (English), Front (Definitions), Prompt A, Prompt B, Image, Scene ID, Tag
COLUMN DEFINITIONS
Front — Korean sentence with the target word replaced by ____
Back — The target Korean word/phrase (the answer)
Full Sentence — Complete Korean sentence
Extra Info — English translation of the full sentence
Target Word (English) — English meaning of the target word
Front (Definitions) — Leave blank unless word has multiple forms worth noting
Prompt A — Image generation prompt using Style A (watercolor/Ghibli)
Prompt B — Image generation prompt using Style B (cinematic/gritty)
Image — Leave blank (populated later by script)
Scene ID — Integer, shared across all cards that use the same Full Sentence
Tag — Beginner, Intermediate, or Advanced based on vocab word
CARD CREATION RULES

Create one card per target vocabulary word or grammar pattern
Multiple cards can share the same Full Sentence (and thus the same Scene ID)
If a word appears in the transcript without a sentence, create a natural example sentence using context from the session (the student is a musician, programmer, and filmmaker)
For grammar patterns (e.g., ~때, verb+보다), create cards testing the grammar structure

SCENE ID RULES

Assign Scene IDs sequentially starting from 1
Cards sharing the same Full Sentence get the same Scene ID
Each unique Full Sentence gets a unique Scene ID

IMAGE PROMPT STYLE GUIDE
All image prompts follow a three-part structure: Prefix + Scene Description + Suffix
Style A (Prompt A)
Prefix:
Soft watercolor hand-drawn illustration in the style of Studio Ghibli, Ken Sugomori, Nostalgic 2000s Nintendo famicom game artwork, warm muted palette, delicate ink outlines with gentle color washes,
Suffix:
no text no words no letters no numbers in the image, square composition, striking expressive characters with elegant features and detailed eyes, soft natural lighting, painterly watercolor texture with visible paper grain
Style B (Prompt B)
Prefix:
cinematic, gritty realism with saturated candy colors, realistic human figures, harsh lighting with deep shadows, teal and pink accents, slightly playful but tense mood, film grain texture, shallow depth of field, Korean aesthetic,
Suffix:
no text no words no letters no numbers in the image, square composition, striking expressive characters with elegant features and detailed eyes, dramatic directional lighting, film grain texture
SCENE DESCRIPTION RULES (shared by both styles)

Depict the SCENARIO of the full sentence, NOT the isolated target word
This prevents spoiling the cloze-deletion answer
Keep descriptions visual and concrete, not abstract
Lean into absurd scenarios when possible
When describing scenes where I am the subject, use: Young korean male with black messy bangs, white polo, dark navy blue pants, brown eyes.
Prompt A and Prompt B should have meaningfully different scene compositions — different angles, focuses, or interpretive takes on the same sentence, not just lighting changes

SHARED SCENES

Only fill Prompt A and Prompt B for the FIRST card in a scene group
Leave them blank for subsequent cards with the same Scene ID

CSV FORMATTING

UTF-8 encoded
All fields double-quoted
No trailing commas

CUSTOMIZATION (edit per session)
Session date: [DATE]
Topics covered: [e.g., dream story, food vocabulary, comparison grammar]
Skip these words (I already know them): [e.g., 안녕하세요, 감사합니다, 네]
Extra context for prompts: [e.g., "we talked about my new studio setup"]
TUTOR SESSION TRANSCRIPT
[paste transcript here]
