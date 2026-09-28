# -*- coding: utf-8 -*-
"""Build The Outsiders vocab lessons (e.g. lesson_17, lesson_18) using the
existing generate_lesson.py HTML template, with hand-curated word/question
data (no WordNet dependency — generate_lesson.py's WordNet-based generators
require nltk, which is broken in this environment; see CLAUDE.md), plus a
new 3-part "Test Practice" mode appended to each page (Synonym Match /
Fill-in-the-Blank / Answer the Question) matching the grade-7 test rubric
in `pdfs/grade 7/Vocab Test Prep - Strategies and Test Format.pdf`.

To add another chapter's worth of vocab (e.g. Ch. 6-8 -> lesson_19):
  1. Add a new LESSON_19 list to outsiders_lesson_data.py, same shape as
     LESSON_17/18 (word, pos, definition, ex, syns, ants, simile x2,
     metaphor, prompt).
  2. Add a build_lesson(...) call for it at the bottom of this file.
  3. Re-run: python3 build_outsiders_lesson.py
  4. Manually add its entry to LESSONS[] in quiz/index.html (update_index_html()
     in generate_lesson.py assumes 15 words/lesson and will miscount stats
     for these lessons — do it by hand instead).
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_lesson as gl  # noqa: E402  (pure-python helpers only; avoid nltk-dependent calls)
from outsiders_lesson_data import LESSON_17, LESSON_18  # noqa: E402
from outsiders_practice_block import build_practice_block  # noqa: E402

random.seed(1717)

GENERIC_DISTRACTORS = [
    'ordinary', 'typical', 'routine', 'casual', 'familiar', 'plain',
    'silent', 'loud', 'gradual', 'sudden', 'gentle', 'harsh',
]

_SYN_TEMPLATES = [
    "{W} most nearly means:",
    "Which word is a synonym for {W}?",
    "{W} is closest in meaning to:",
]
_ANT_TEMPLATES = [
    "Which word is the OPPOSITE of {W}?",
    "{W} is most nearly OPPOSITE in meaning to:",
]
_SIMILE_STEMS = [
    "Complete the simile: {WORD_CAP} — it was like ___",
    "Complete the simile: Being {WORD} felt like ___",
]


def _make_q(qtype, word, q, answer, wrong, hint):
    ch = [answer] + wrong[:3]
    while len(ch) < 4:
        ch.append('(none of these)')
    return {'type': qtype, 'word': word, 'q': q, 'a': answer, 'ch': ch, 'hint': hint}


def _pick(pool, n, avoid):
    pool = [x for x in pool if x not in avoid]
    random.shuffle(pool)
    return pool[:n]


def gen_synonym_qs(words):
    questions = []
    all_ants_pool = list({a for w in words for a in w['ants']}) or GENERIC_DISTRACTORS
    for w in words:
        word = w['word']
        wrong_pool = w['ants'] + all_ants_pool + GENERIC_DISTRACTORS
        for i, syn in enumerate(w['syns']):
            tmpl = _SYN_TEMPLATES[i % len(_SYN_TEMPLATES)]
            q = tmpl.format(W=word.upper())
            wrong = _pick(wrong_pool, 3, avoid=[syn, word])
            hint = f"'{word.capitalize()}' means {w['definition'][:70].rstrip('.')} — '{syn}' captures the same idea."
            questions.append(_make_q('synonym', word, q, syn, wrong, hint))
    return questions


def gen_antonym_qs(words):
    questions = []
    all_syns_pool = list({s for w in words for s in w['syns']}) or GENERIC_DISTRACTORS
    for w in words:
        word = w['word']
        wrong_pool = w['syns'] + all_syns_pool + GENERIC_DISTRACTORS
        for i, ant in enumerate(w['ants']):
            tmpl = _ANT_TEMPLATES[i % len(_ANT_TEMPLATES)]
            q = tmpl.format(W=word.upper())
            wrong = _pick(wrong_pool, 3, avoid=[ant, word])
            hint = f"'{word.capitalize()}' means {w['definition'][:60].rstrip('.')} — '{ant}' is the opposite idea."
            questions.append(_make_q('antonym', word, q, ant, wrong, hint))
    return questions


def gen_analogy_qs(words):
    questions = []
    n = len(words)
    for i, w in enumerate(words):
        partners = [words[(i + 1) % n], words[(i + 2) % n]]
        # relation 1: synonym pair
        other = partners[0]
        if w['syns'] and other['syns']:
            syn1 = random.choice(w['syns'])
            ans = random.choice(other['syns'])
            q = f"{w['word'].upper()} is to {syn1.upper()} as {other['word'].upper()} is to _____"
            wrong_pool = other['ants'] + GENERIC_DISTRACTORS + [x['word'] for x in words]
            wrong = _pick(wrong_pool, 3, avoid=[ans, other['word'], w['word']])
            hint = f"Both pairs are synonyms — {w['word']}/{syn1} and {other['word']}/{ans} share the same relationship."
            questions.append(_make_q('analogy', w['word'], q, ans, wrong, hint))
        # relation 2: antonym pair
        other2 = partners[1]
        if w['ants'] and other2['ants']:
            ant1 = random.choice(w['ants'])
            ans2 = random.choice(other2['ants'])
            q2 = f"{w['word'].upper()} is to {ant1.upper()} as {other2['word'].upper()} is to _____"
            wrong_pool2 = other2['syns'] + GENERIC_DISTRACTORS + [x['word'] for x in words]
            wrong2 = _pick(wrong_pool2, 3, avoid=[ans2, other2['word'], w['word']])
            hint2 = f"Both pairs are antonyms — {w['word']} opposes {ant1}, and {other2['word']} opposes {ans2}."
            questions.append(_make_q('analogy', w['word'], q2, ans2, wrong2, hint2))
    return questions


_WRONG_COMPLETIONS = [
    "a sunny afternoon with nothing unusual on the horizon",
    "a list completed ahead of schedule with every item checked",
    "a routine confirmed by everyone in the room before it began",
    "something expected and received exactly as advertised",
    "a familiar road taken so many times that nothing about it required attention",
    "a schedule that stayed exactly the same from morning to night",
]


def gen_simile_qs(words):
    questions = []
    for w in words:
        word = w['word']
        for i, completion in enumerate(w['simile']):
            stem = _SIMILE_STEMS[i % len(_SIMILE_STEMS)]
            q = stem.format(WORD=word, WORD_CAP=word.upper())
            wrong = random.sample(_WRONG_COMPLETIONS, 3)
            hint = f"Think about what '{word}' means: {w['definition'][:70].rstrip('.')} The best completion captures that feeling in a concrete image."
            questions.append(_make_q('simile', word, q, completion, wrong, hint))
    return questions


def gen_metaphor_qs(words):
    questions = []
    for w in words:
        word = w['word']
        word_cap = word[0].upper() + word[1:]
        metaphor = w['metaphor']
        literal = gl._make_literal_sentence(word, w['ex'])
        sim_completions = w['simile'][:2] if len(w['simile']) >= 2 else w['simile'] * 2
        sim1 = f"{word_cap} was like {sim_completions[0]}."
        sim2 = f"{word_cap} felt like {sim_completions[1]}."
        options = list(dict.fromkeys([literal, sim1, sim2]))
        while len(options) < 3:
            options.append(f"{word_cap} seemed like {sim_completions[0]}, in a way.")
        q = f"Which sentence is a metaphor using {word.upper()}?"
        hint = (f"A metaphor makes a direct equation without 'like' or 'as'. "
                f"The correct answer calls {word} something else directly, not comparing it to something.")
        questions.append(_make_q('metaphor', word, q, metaphor, options[:3], hint))
    return questions


def build_lesson(lesson_num, story, color, words, out_dir='/Users/dorsag01/Documents/Kyle/quiz'):
    syn_qs = gen_synonym_qs(words)
    ant_qs = gen_antonym_qs(words)
    ana_qs = gen_analogy_qs(words)
    sim_qs = gen_simile_qs(words)
    met_qs = gen_metaphor_qs(words)
    all_qs = syn_qs + ant_qs + ana_qs + sim_qs + met_qs
    random.shuffle(all_qs)

    errors = gl.validate_questions(all_qs)
    print(f"Lesson {lesson_num}: {len(all_qs)} questions "
          f"(syn={len(syn_qs)} ant={len(ant_qs)} analogy={len(ana_qs)} simile={len(sim_qs)} metaphor={len(met_qs)})")
    if errors:
        print("  VALIDATION ERRORS:")
        for e in errors[:20]:
            print("   ", e)

    words_for_template = [{'word': w['word'], 'pos': w['pos'], 'def': w['definition'], 'ex': w['ex']} for w in words]
    html = gl.build_html(lesson_num, story, color, words_for_template, all_qs)

    # rebrand away from "Wordly Wise" — these lessons are from a different vocab curriculum
    html = html.replace(f"Wordly Wise &mdash; Lesson {lesson_num}: {story}", story)
    html = html.replace(f"Wordly Wise &middot; Lesson {lesson_num}", f"S.E. Hinton&rsquo;s <em>The Outsiders</em> &middot; Lesson {lesson_num}")
    html = html.replace(
        f"Master {len(words)} key vocabulary words from this lesson. Test yourself with synonyms, antonyms, analogies, similes, and metaphors &mdash; then review with flashcards.",
        f"Master {len(words)} key vocabulary words from <em>The Outsiders</em>. Test yourself with synonyms, antonyms, analogies, similes, and metaphors, then try Test Practice &mdash; the same synonym-match, fill-in-the-blank, and short-answer format as your real quiz."
    )

    # inject the new 3-part Test Practice mode
    acc = color
    dark = gl.darken(acc)
    r, g, b = gl.hex_to_rgb(acc)
    rgba_star = f'rgba({r},{g},{b}'
    css, screens_html, start_btn_html, script_js = build_practice_block(acc, dark, rgba_star, words)

    marker_style_close = '</style>\n</head>'
    assert html.count(marker_style_close) == 1, 'style close marker not found/unique'
    html = html.replace(marker_style_close, css + marker_style_close)

    marker_flash_btn = '<div><button class="btn btn-secondary" id="btn-flash-start">&#x1F4DA; Study Flashcards</button></div>'
    assert html.count(marker_flash_btn) == 1, 'flash button marker not found/unique'
    html = html.replace(marker_flash_btn, marker_flash_btn + '\n    ' + start_btn_html)

    marker_script_open = '\n<script>\n(function(){'
    assert html.count(marker_script_open) == 1, 'script open marker not found/unique'
    html = html.replace(marker_script_open, screens_html + marker_script_open)

    marker_script_close = '\n})();\n</script>'
    assert html.count(marker_script_close) == 1, 'script close marker not found/unique'
    html = html.replace(marker_script_close, script_js + marker_script_close)

    out = Path(out_dir) / f'lesson_{lesson_num}'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'index.html').write_text(html, encoding='utf-8')
    print(f"  wrote {out / 'index.html'}")
    return out / 'index.html', len(all_qs)


if __name__ == '__main__':
    build_lesson(17, 'The Outsiders: Ch. 1–2', '#0ea5e9', LESSON_17)
    build_lesson(18, 'The Outsiders: Ch. 3–5', '#f97316', LESSON_18)
