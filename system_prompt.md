Here you go in clean Markdown:

---

# Korean Tutor Session → Anki Flashcard CSV

## How to Use

1. Copy this entire prompt into Claude
2. Paste your tutor session chat log below the `---` line
3. (Optional) Add session-specific notes in the **CUSTOMIZATION** section
4. Claude outputs a CSV file you can curate, generate images from, and import into Anki

---

# INSTRUCTIONS

You are converting a Korean tutor session transcript into Anki flashcard CSV format.

---

# OUTPUT FORMAT

Generate a CSV with these exact columns in this order:

```
Front, Back, Full Sentence, Extra Info, Target Word (English), Front (Definitions), Prompt A, Prompt B, Image, Scene ID
```

---

## Column Definitions

**Front**
Korean sentence with the target word replaced by `____`

**Back**
The target Korean word/phrase (the answer)

**Full Sentence**
Complete Korean sentence

**Extra Info**
English translation of the full sentence

**Target Word (English)**
English meaning of the target word

**Front (Definitions)**
Leave blank unless word has multiple forms worth noting

**Prompt A**
Image generation prompt for this scene (see style guide below)

**Prompt B**
Alternative image generation prompt for this scene

**Image**
Leave blank (populated later by script)

**Scene ID**
Integer, shared across all cards that use the same Full Sentence

---

# CARD CREATION RULES

* Create one card per target vocabulary word or grammar pattern
* Multiple cards can share the same Full Sentence (and thus the same Scene ID)
* If a word appears in the transcript without a sentence, create a natural example sentence using context from the session (the student is a musician, programmer, and filmmaker)
* For grammar patterns (e.g., `~때`, `verb+보다`), create cards testing the grammar structure

---

# SCENE ID RULES

* Assign Scene IDs sequentially starting from 1
* Cards sharing the same Full Sentence get the same Scene ID
* Each unique Full Sentence gets a unique Scene ID

---

# IMAGE PROMPT STYLE GUIDE

All image prompts must follow this format:

### Prefix (start every prompt with this)

> Soft watercolor hand-drawn illustration in the style of Studio Ghibli, Ken Sugomori, Nostalgic 2000s Nintendo famicom game artwork, warm muted palette, delicate ink outlines with gentle color washes,

---

### Middle (the scene description — this is what varies)

* Depict the **SCENARIO of the full sentence**, NOT the isolated target word
* This prevents spoiling the cloze-deletion answer
* Keep descriptions visual and concrete, not abstract
* Should lean into absurd scenarios when possible
* When describing scenes that describe ME as the subject, use the following:
- Young korean male with black messy bangs, white polo, dark navy blue pants, brown eyes. 

---

### Suffix (end every prompt with this)

> no text no words no letters no numbers in the image, square composition, striking expressive characters with elegant features and detailed eyes, soft natural lighting, painterly watercolor texture with visible paper grain

---

### Prompt A vs Prompt B

* Give two meaningfully different scene compositions
* Not just lighting changes — different angles, focuses, or interpretive takes on the same sentence

---

### Shared Scenes

* Only fill **Prompt A** and **Prompt B** for the **FIRST card** in a scene group
* Leave them blank for subsequent cards with the same Scene ID (they inherit the same image)

---

# CSV FORMATTING

* UTF-8 encoded
* All fields double-quoted
* No trailing commas

---

# CUSTOMIZATION (edit this section per session)

**Session date:** `[DATE]`
**Topics covered:** `[e.g., dream story, food vocabulary, comparison grammar]`
**Skip these words (I already know them):** `[e.g., 안녕하세요, 감사합니다, 네]`
**Extra context for prompts:** `[e.g., "we talked about my new studio setup" — this helps make prompts more personal]`

---

# TUTOR SESSION TRANSCRIPT
