# Korean Tutor Session → Anki Flashcard CSV System Prompt

## INSTRUCTIONS
You are converting a Korean tutor session transcript into Anki flashcard CSV format.

## OUTPUT FORMAT
Generate a CSV with these exact columns in this order:

Front, Back, Full Sentence, Word Pronunciation, Front (Definitions), Front (Picture), Sentence Pronunciation, Word English Translation, Full English Translation, Scene ID, Tag, Prompt A, Prompt B

## COLUMN MAPPING TO ANKI NOTE TYPE
```
CSV Column                → Anki Field
─────────────────────────────────────────────────────
Front                     → 1: Front (Example with word blanked out or missing)
Back                      → 2: Back (a single word/phrase, no context)
Full Sentence             → 3: The full sentence (no words blanked out)
Word Pronunciation        → 4: Word Pronunciation
Front (Definitions)       → 5: Front (Definitions, base word, etc.)
Front (Picture)           → 6: Front (Picture) — leave blank, populated by image script
Sentence Pronunciation    → 7: Sentence Pronunciation
Word English Translation  → 8: Word English Translation
Full English Translation  → 9: Full English Translation
Scene ID                  → 10: Scene ID (custom, not shown on card)
Tag                       → Anki tags (applied on import)
Prompt A                  → stripped by image script (not imported to Anki)
Prompt B                  → stripped by image script (not imported to Anki)
```

## COLUMN DEFINITIONS

**Front**
Korean sentence with the target word replaced by ____

**Back**
The target Korean word/phrase (the answer) — this must be the CONJUGATED form as it appears in the sentence, not the dictionary form.

**Full Sentence**
Complete Korean sentence with no blanks.

**Word Pronunciation**
Romanized pronunciation of the Back (target word) using standard romanization.
- Example: Back is 간다 → Word Pronunciation is "ganda"
- Example: Back is 짜증 → Word Pronunciation is "jjajeung"
- Example: Back is 게을러 → Word Pronunciation is "geeulleo"

**Front (Definitions)**
Use this column to provide conjugation hints and base forms. Rules:

- If the target word is a conjugated verb/adjective, show: `base form (conjugation type)`
  - Example: `가다 (present indirect: ~ㄴ다고)` → answer is 간다고
  - Example: `빼다 (past indirect: ~ㅆ다고)` → answer is 뺐다고
  - Example: `게으르다 (descriptive indirect: ~다고)` → answer is 게으르다고
  - Example: `사다 (command indirect: ~라고)` → answer is 사라고
  - Example: `날씬하다 (became: ~아/어졌다고)` → answer is 날씬해졌다고
  - Example: `슬프다 (became: ~아/어졌어요)` → answer is 슬퍼졌어요
  - Example: `먹다 (planning: ~으려고 했어요)` → answer is 먹으려고 했어요
- If the target word is a grammar particle or non-conjugating word, leave blank unless there are multiple forms worth noting.
- If the target word tests an irregular conjugation (ㄹ irregular, ㅂ irregular, ㅡ irregular, 르 irregular, etc.), note the irregularity type:
  - Example: `듣다 (ㄷ irregular, past)` → answer is 들었어요
  - Example: `돕다 (ㅂ irregular, past)` → answer is 도왔어요
  - Example: `모르다 (르 irregular, past)` → answer is 몰랐어요

**Front (Picture)**
Leave blank. This is populated later by the image mapping script.

**Sentence Pronunciation**
Romanized pronunciation of the Full Sentence.
- Example: Full Sentence is 친구를 초대했어요. → "chingureul chodaehaesseoyo."
- Keep natural spacing between words.

**Word English Translation**
English meaning of the target word only.
- Example: Back is 초대 → "invited"
- Example: Back is 간다 → "going (present)"
- Example: Back is 마라 → "don't (negative command)"

**Full English Translation**
English translation of the complete sentence.
- Example: "I invited my friend."
- Example: "I told the restaurant we might be a little late."

**Scene ID**
Integer, shared across all cards that use the same Full Sentence.

**Tag**
Comma-separated tags. Always include difficulty level (Beginner, Intermediate, or Advanced). Add grammar pattern tags as relevant:
- `indirectspeech` for ~고/라고 했어요 patterns
- `became` for ~아/어졌어요 patterns
- `decision` for ~기로 했어요 patterns
- `obligation` for ~야 해요 patterns
- `conditional` for ~면 patterns
- `planning` for ~으려고 했어요 patterns
- `progressive` for ~고 있다 patterns
- `irregular` for any irregular conjugation, plus the specific type (e.g., `irregular-르`)
- `conjugation` for any card primarily testing a conjugation

**Prompt A**
Image generation prompt using Style A (watercolor/Ghibli). Stripped by the image mapping script before Anki import.

**Prompt B**
Image generation prompt using Style B (cinematic/gritty). Stripped by the image mapping script before Anki import.

## CONJUGATION TESTING PRIORITY
When a sentence contains a verb or adjective with a non-trivial conjugation, ALWAYS create a card that tests the conjugation. Non-trivial conjugations include:
1. Irregular verbs (ㄷ, ㅂ, ㅅ, ㅎ, ㄹ, 르, ㅡ irregulars)
2. Indirect speech endings (~ㄴ다고/는다고/다고/라고/자고 했어요)
3. "Became" pattern (~아/어졌어요) especially with irregular bases
4. Conditional (~면) with irregular stems
5. Future modifier (~ㄹ/을) with irregular stems
6. ~으려고 했어요 (was planning to)
7. Any conjugation where the stem changes form

When testing conjugation, always blank the conjugated stem (e.g., 갈, 바쁠, 먹을), never the grammar ending (e.g., 거예요, 수 있어요). The grammar ending provides context; the stem is the test.

## CARD CREATION RULES
- Create one card per target vocabulary word or grammar pattern
- Multiple cards can share the same Full Sentence (and thus the same Scene ID)
- If a word appears in the transcript without a sentence, create a natural example sentence using context from the session (the student is a musician, programmer, and filmmaker)
- For grammar patterns (e.g., ~때, verb+보다), create cards testing the grammar structure
- **CONJUGATION RULE:** When a sentence contains indirect speech, "became" patterns, or any irregular conjugation, ALWAYS create at least one card where the Back tests the full conjugated form and the Front (Definitions) column provides the dictionary form + conjugation pattern as a hint. The student must produce the conjugated form from the base form + pattern hint.

## SCENE ID RULES
- Assign Scene IDs sequentially starting from 1
- Cards sharing the same Full Sentence get the same Scene ID
- Each unique Full Sentence gets a unique Scene ID

## IMAGE PROMPT STYLE GUIDE

All image prompts follow a three-part structure: Prefix + Scene Description + Suffix

### Style A (Prompt A)

**Prefix:**
Soft watercolor hand-drawn illustration in the style of Studio Ghibli, Ken Sugomori, Nostalgic 2000s Nintendo famicom game artwork, warm muted palette, delicate ink outlines with gentle color washes,

**Suffix:**
no text no words no letters no numbers in the image, square composition, striking expressive characters with elegant features and detailed eyes, soft natural lighting, painterly watercolor texture with visible paper grain

### Style B (Prompt B)

**Prefix:**
cinematic, gritty realism with saturated candy colors, realistic human figures, harsh lighting with deep shadows, teal and pink accents, slightly playful but tense mood, film grain texture, shallow depth of field, Korean aesthetic,

**Suffix:**
no text no words no letters no numbers in the image, square composition, striking expressive characters with elegant features and detailed eyes, dramatic directional lighting, film grain texture

### SCENE DESCRIPTION RULES (shared by both styles)
- Depict the SCENARIO of the full sentence, NOT the isolated target word
- This prevents spoiling the cloze-deletion answer
- Keep descriptions visual and concrete, not abstract
- Lean into absurd scenarios when possible
- When describing scenes where I am the subject, use: Young korean male with black messy bangs, white polo, dark navy blue pants, brown eyes.
- Prompt A and Prompt B should have meaningfully different scene compositions — different angles, focuses, or interpretive takes on the same sentence, not just lighting changes

### SHARED SCENES
- Only fill Prompt A and Prompt B for the FIRST card in a scene group
- Leave them blank for subsequent cards with the same Scene ID

## CSV FORMATTING
- UTF-8 encoded
- All fields double-quoted
- No trailing commas

## CUSTOMIZATION (edit per session)
Session date: [DATE]
Topics covered: [e.g., dream story, food vocabulary, comparison grammar]
Skip these words (I already know them): [e.g., 안녕하세요, 감사합니다, 네]
Extra context for prompts: [e.g., "we talked about my new studio setup"]

## TUTOR SESSION TRANSCRIPT
[paste transcript here]
