# Wordly Wise 3000 — Book 6 Quiz Collection

A self-contained vocabulary quiz application for Wordly Wise 3000 Book 6, covering all 14 lessons, 210 words, and 2,726 questions. No server required — open any HTML file directly in a browser.

---

## Quick Start

1. Open `quiz/index.html` in any modern browser
2. Click a lesson card to begin
3. Use **Flashcard Mode** to study, then switch to **Quiz Mode** to test yourself
4. Use `master.html` to quiz across all lessons at once

---

## File Structure

```
quiz/
├── index.html          # Hub — lesson navigation grid
├── master.html         # Master quiz — all 2,726 questions, filterable by lesson & type
├── questions.json      # Structured export of all questions (developer use)
├── README.md           # This file
├── lesson_1/index.html
├── lesson_2/index.html
│   ...
└── lesson_14/index.html
```

---

## Lessons

| # | Story | Words |
|---|-------|-------|
| 1 | Lady Liberty | affection, appeal, clasp, conspicuous, contribute, declare, eloquent, exhibit, ferry, immigrant, lofty, pedestal, persecute, poverty, unveil |
| 2 | Rosa Parks | arrogant, boycott, campaign, ceremony, custody, degrade, detain, extend, integrate, segregate, supreme, triumph, vacate, verdict, violate |
| 3 | Land of Contrasts | abundant, arid, distinct, graze, hectic, horde, humid, incredible, inhabit, peninsula, rural, sanctuary, splendor, squalor, terrain |
| 4 | A Different Way to Fly | aloft, attain, buffet, elude, flammable, hover, inflate, jeopardy, moor, plummet, pollute, propel, stationary, superb, swivel |
| 5 | A Born Artist | antic, attire, captivate, deft, diligent, eclipse, evolve, innate, inscribe, posture, shroud, stifle, tentative, tranquil, versatile |
| 6 | The Story of Silk | apparel, appreciate, continuous, dissolve, domesticate, emerge, fiber, function, hatch, inhibit, minute, motion, sheathe, shed, transfer |
| 7 | Home on the Range | brawl, casual, constant, excel, exhaust, hardy, mediocre, monotonous, originate, punctuate, ravenous, realistic, soothe, stampede, veteran |
| 8 | Sacagawea's Great Adventure | accompany, beneficial, captive, convenient, ecstasy, expanse, expedition, inept, interpret, invaluable, linger, retrieve, skirmish, supplement, territory |
| 9 | Water, Water, Everywhere | accumulate, aggravate, conserve, contaminate, diminish, drastic, extravagant, frugal, impurity, peril, perpetual, resource, substitute, sustain, vital |
| 10 | Fun and Games | anticipate, bankrupt, brief, brisk, budget, compete, complicate, effect, err, factor, fad, gripe, knack, leisure, unique |
| 11 | Elizabeth Blackwell, M.D. | abbreviate, appropriate, exclude, fanciful, futile, grudge, inspire, majority, persevere, possess, prejudice, resolute, sneer, unanimous, unruly |
| 12 | The Trojan Horse | abandon, adversary, baffle, blunder, colossal, detect, haul, overpower, rejoice, scoff, sentinel, siege, sinister, victor, woe |
| 13 | The Ship of the Desert | adapt, deplete, efficient, fatigue, gait, glare, habitat, oblivious, outmoded, prominent, quench, rigor, sear, transport, wend |
| 14 | The Silk Road | benevolent, consent, discreet, engross, esteem, exaggerate, extensive, fantastic, intrigue, marvel, mission, opportunity, relinquish, tyrant, vanquish |

---

## Features

### Individual Lesson Pages (`lesson_N/index.html`)

**Flashcard Mode**
- Flip cards to reveal definitions, parts of speech, and example sentences
- Keyboard shortcut: Space to flip, ← → to navigate
- Progress indicator shows card position

**Quiz Mode**
- 20 questions drawn randomly from a pool of ~195 per lesson
- 4-choice multiple choice; one correct answer
- Hint button reveals a clue (counts against score)
- Streak counter tracks consecutive correct answers
- Results screen shows score, accuracy, and a themed message
- Wrong answers listed for review

**Question Types** (color-coded)
| Type | Color | Description |
|------|-------|-------------|
| Synonym | Blue | Find the word closest in meaning |
| Antonym | Pink | Find the word opposite in meaning |
- Analogy | Amber | Complete the word relationship (A : B :: C : ?) |
| Simile | Green | Choose the simile that uses the word correctly |
| Metaphor | Purple | Choose the metaphor that uses the word correctly |

### Master Quiz (`master.html`)

- All 2,726 questions in one place
- **Lesson filter**: Toggle individual lessons on/off; "All" / "None" buttons
- **Type filter**: Toggle question types independently
- Pool size updates live as filters change
- 20 questions per round drawn from the filtered pool
- Results include a breakdown by type and by lesson
- Wrong answer review panel

---

## questions.json Schema

```json
{
  "lessons": [
    {
      "lesson": 1,
      "story": "Lady Liberty",
      "color": "#f0c040",
      "words": ["affection", "appeal", "..."],
      "questions": [
        {
          "type": "synonym",
          "word": "eloquent",
          "q": "Which word is closest in meaning to eloquent?",
          "a": "expressive",
          "ch": ["expressive", "awkward", "silent", "vague"],
          "hint": "Think: speaking powerfully and clearly"
        }
      ]
    }
  ]
}
```

**Question fields:**
| Field | Type | Description |
|-------|------|-------------|
| `type` | string | `synonym`, `antonym`, `analogy`, `simile`, or `metaphor` |
| `word` | string | The vocabulary word being tested |
| `q` | string | Question prompt text |
| `a` | string | Correct answer |
| `ch` | string[] | All four choices (correct answer is one of them) |
| `hint` | string | Hint text shown when the hint button is clicked |

---

## Technical Notes

- **No dependencies**: All lesson pages are fully self-contained HTML files. The master quiz embeds all questions inline. No build step, no npm, no server.
- **canvas-confetti**: Loaded from CDN (`cdn.jsdelivr.net`) on result screens. Pages work offline without it (confetti simply won't fire).
- **Animated background**: HTML5 Canvas starfield, unique color palette per lesson.
- **Question counts**: 195 questions per lesson (lessons 1, 8, and 13 have 193–194 due to source material constraints). Total: 2,726.
- **Browser support**: Any modern browser (Chrome, Firefox, Safari, Edge). No IE support.
