"""Lint any draft for AI-slop tells and flat rhythm.

Usage: python slop_check.py draft.md [--form blog|article|email|chat|reply|post|summary|notes|any]
Exit 0 = no FAIL. WARN lines are judgement calls; read them, don't obey them blindly.
Quoted text ("..." or “...”) is ignored for style checks: it is someone else's voice.
"""
import argparse
import re
import statistics
import sys
from pathlib import Path

BANNED = {
    r"\bdelv(e|es|ing)\b": "delve",
    r"\btapestry\b": "tapestry",
    r"\btestament to\b": "testament to",
    r"\blandscape\b": "landscape",
    r"\bnavigat(e|ing) the\b": "navigate the",
    r"\bseamless(ly)?\b": "seamless",
    r"\brobust\b": "robust",
    r"\bcutting[- ]edge\b": "cutting-edge",
    r"\bgame[- ]?chang(er|ing)\b": "game-changer",
    r"\bleverag(e|es|ing)\b": "leverage",
    r"\butili[sz](e|es|ing)\b": "utilise",
    r"\belevat(e|es|ing)\b": "elevate",
    r"\bempower(s|ing)?\b": "empower",
    r"\bunlock(s|ing)? (the|your|new|their)\b": "unlock the",
    r"\brealm of\b": "realm of",
    r"\bjourney\b": "journey",
    r"\bin today'?s\b": "in today's…",
    r"\bfast[- ]paced\b": "fast-paced",
    r"\bit'?s (worth|important to) not(e|ing)\b": "it's important to note",
    r"\bin conclusion\b": "in conclusion",
    r"\blet'?s dive\b|\bdive (in|deep)\b": "dive in",
    r"\bbuckle up\b": "buckle up",
    r"\bhere'?s the (thing|kicker)\b": "here's the thing",
    r"\bgreat question\b": "great question",
    r"\bhope (this|that) (email |message )?finds you\b": "hope this finds you well",
    r"\b(i|we) wanted to reach out\b": "wanted to reach out",
    r"\bdon'?t hesitate to\b": "don't hesitate to",
    r"\b(thrilled|excited) to (announce|share)\b": "excited to announce",
    r"\bany inconvenience\b": "any inconvenience",
    r"\btake (this|it) (very )?seriously\b": "we take this seriously",
    r"\bunforeseen circumstances\b": "unforeseen circumstances",
    r"\bnot (just|only) [^.,;]{1,40},? but( also)?\b": "not just X but Y",
    r"\bit'?s not [^.;]{1,40}[,;—–-]+ it'?s\b": "it's not X, it's Y",
    r"\bmay potentially\b": "may potentially",
    r"\bresults[- ]driven\b|\bproven track record\b": "CV cliché",
    r"\blet me know (your thoughts|if you have any questions|if you'?d like to discuss)\b": "let me know your thoughts",
    r"\bgreat job\b|\breally solid\b": "empty praise",
}
# Tells from Wikipedia's "Signs of AI writing". One alone proves little, so a few hits WARN and many FAIL.
AI_TELLS = {
    r",\s+(highlighting|underscoring|emphasi[sz]ing|reflecting|symboli[sz]ing|showcasing|fostering|ensuring)\b": "-ing tail",
    r"\b(serves|stands) as\b|\bboasts\b": "copula avoidance (say 'is')",
    r"\b(pivotal|crucial|vital) role\b|\bstands? as a testament\b|\bunderscores? the importance\b": "significance puffery",
    r"\breflects? (a )?broader\b|\bsetting the stage\b|\bindelible mark\b|\bdeeply rooted\b|\bevolving\b": "significance puffery",
    r"\bvibrant\b|\bnestled\b|\bin the heart of\b|\brenowned\b|\bdiverse array\b|\bgroundbreaking\b": "promotional word",
    r"\b(experts|observers|critics|analysts) (argue|say|believe|have (noted|cited))\b|\bindustry reports\b": "vague attribution",
    r"\bchallenges and (future )?(prospects|opportunities)\b|\bvaluable insights?\b|\bresonates? with\b": "stock phrase",
}
AI_TELLS_FAIL = 3
# Style words with the biggest jump in 15M PubMed abstracts after 2023 (Kobak et al., Science Advances 2025).
STYLE_WORDS = (
    r"\b(delv\w*|intricat\w*|meticulous\w*|showcas\w*|underscor\w*|pivotal|realms?|tapestry|unveil\w*|"
    r"unravel\w*|multifaceted|commendable|unparalleled|transformative|seamless\w*|elucidat\w*|noteworthy|"
    r"embark\w*|bolster\w*|foster\w*|garner\w*|burgeoning|accentuat\w*|indispensab\w*|interplay|"
    r"groundbreaking|comprehensive|enhanc\w*|streamlin\w*|surpass\w*)\b"
)
STYLE_WORDS_MAX = 1
# Reading grade (Flesch-Kincaid): busy readers do better with plain text.
GRADE_FORMS = {"email", "chat", "reply", "post"}
GRADE_MAX = 11
# Models repeat their own pet phrases inside one piece (Antislop, Paech et al. 2025).
STOPWORDS = set("a an the and or but of to in on at for with by from is are was were be it its this that you your we our i".split())
REPEAT_MIN = 3
ASK_FORMS = {"email", "chat"}
ASKS_MAX = 2
CONTRAST = r"\b(isn'?t|is not|wasn'?t|aren'?t)\b[^.!?\n]{1,50}[.;,]\s+(it|they|that)('?s| is| was| are)\b"
CONTRAST_MAX = 1
INLINE_HEADER = r"(?m)^\s*[-*]\s+\*\*[^*\n]{1,40}[.:]?\*\*"
INLINE_HEADER_FORMS = {"notes", "summary", "any"}
INLINE_HEADER_MAX = 3
FILLER_OPENERS = r"(?m)(?:^|[.!?]\s+)(Moreover|Furthermore|Additionally|Overall|Ultimately|Notably|Importantly),"
HEDGES = r"\b(may|might|could potentially|perhaps|arguably|somewhat|relatively|fairly|quite)\b"
THROAT_CLEARING = r"^(in this (post|article|email|piece)|this (post|article) (will|explores)|have you ever wondered|let'?s (talk|explore))"
RECAP_CLOSE = r"^(in (summary|short|conclusion)|overall|to (sum|wrap) (up|it up)|all in all)\b"

FORMS = {  # (min words, max words, max bullets)
    "blog": (400, 1600, 12), "article": (500, 2500, 12), "email": (25, 250, 6), "chat": (1, 90, 4), "reply": (40, 200, 4),
    "post": (40, 280, 6), "summary": (60, 300, 7), "notes": (60, 350, 15), "any": (1, 100000, 20),
}
WORDS_PER_EM_DASH = 150
EXCLAIM_MAX = 1
TRIAD_MAX = 2
HEDGES_PER_100_MAX = 1.5
MIN_SENTENCES_FOR_RHYTHM = 6
RHYTHM_STDEV_MIN = 4.0
LONG_SENTENCE = 32
HASHTAG_MAX = 2
EXPOSITION = (r"\b(that'?s (what|why) |this is (why|what|where) |that is why|which is why|in other words|put simply|"
              r"here'?s (why|the (straight|short|honest|real))|the (straight|short|honest) answer|it'?s a fair question|"
              r"the reason is)")
EXPOSITION_MAX = 1
BUTTON_FORMS = {"blog", "article", "post", "any"}
BUTTON_WORDS = 9
BUTTON_MAX = 2


def strip_quotes(text: str) -> str:
    return re.sub(r"[\"“][^\"”\n]*[\"”]", "", text)


def sentences(text: str) -> list[str]:
    body = re.sub(r"^\s*([-*#>]|\d+\.)\s*", "", text, flags=re.M)
    body = body.replace("**", "")
    return [s for s in re.split(r"(?<=[.!?])\s+|\n{2,}", body) if re.search(r"\w", s)]


def syllables(word: str) -> int:
    groups = re.findall(r"[aeiouy]+", word.lower())
    silent_e = word.lower().endswith("e") and len(groups) > 1
    return max(1, len(groups) - silent_e)


def reading_grade(text: str) -> float:
    words = re.findall(r"[A-Za-z]+", text)
    sents = sentences(text)
    if not words or not sents:
        return 0.0
    syl = sum(syllables(w) for w in words)
    return 0.39 * len(words) / len(sents) + 11.8 * syl / len(words) - 15.59


def repeated_phrases(text: str) -> list[str]:
    words = re.findall(r"[a-z']+", text.lower())
    counts: dict[str, int] = {}
    for i in range(len(words) - 2):
        gram = words[i:i + 3]
        if sum(w not in STOPWORDS for w in gram) >= 2:
            key = " ".join(gram)
            counts[key] = counts.get(key, 0) + 1
    return sorted(k for k, n in counts.items() if n >= REPEAT_MIN)


def check(text: str, form: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    own = strip_quotes(text)
    words = len(re.findall(r"\w+", text))
    lo, hi, max_bullets = FORMS[form]
    if not lo <= words <= hi:
        out.append(("WARN", f"{words} words; usual range for {form} is {lo}-{hi}"))
    for pat, label in BANNED.items():
        if re.search(pat, own, re.I):
            out.append(("FAIL", f"slop phrase: {label}"))
    tells = [label for pat, label in AI_TELLS.items() for _ in re.finditer(pat, own, re.I)]
    if tells:
        level = "FAIL" if len(tells) >= AI_TELLS_FAIL else "WARN"
        out.append((level, f"{len(tells)} AI tell(s): {', '.join(sorted(set(tells)))}"))
    style = re.findall(STYLE_WORDS, own, re.I)
    if len(style) > STYLE_WORDS_MAX:
        out.append(("WARN", f"{len(style)} LLM style words ({', '.join(sorted({w.lower() for w in style}))}); use plain verbs"))
    grade = reading_grade(own)
    if form in GRADE_FORMS and grade > GRADE_MAX:
        out.append(("WARN", f"reading grade {grade:.0f}; aim for {GRADE_MAX} or under with shorter words and sentences"))
    repeats = repeated_phrases(own)
    if repeats:
        out.append(("WARN", f"repeated phrase(s): {', '.join(repeats)}; say it once, or vary it"))
    asks = own.count("?")
    if form in ASK_FORMS and asks > ASKS_MAX:
        out.append(("WARN", f"{asks} questions; make one ask stand out"))
    contrasts = len(re.findall(CONTRAST, own, re.I))
    if contrasts > CONTRAST_MAX:
        out.append(("WARN", f"{contrasts} 'isn't X, it's Y' contrasts; keep one at most"))
    headers = len(re.findall(INLINE_HEADER, text))
    if form not in INLINE_HEADER_FORMS and headers > INLINE_HEADER_MAX:
        out.append(("WARN", f"{headers} bold-label bullets; write sentences unless the reader scans by label"))
    fillers = re.findall(FILLER_OPENERS, own)
    if fillers:
        out.append(("FAIL", f"filler transition(s): {', '.join(sorted(set(fillers)))}"))
    dashes = own.count("—") + own.count(" – ")
    if dashes > max(1, words // WORDS_PER_EM_DASH):
        out.append(("FAIL", f"{dashes} em dashes in {words} words; use a colon, full stop or brackets"))
    if own.count("!") > EXCLAIM_MAX:
        out.append(("WARN", f"{own.count('!')} exclamation marks"))
    if len(re.findall(r"#\w+", own)) > HASHTAG_MAX:
        out.append(("FAIL", "hashtag soup"))
    if len(re.findall(r"[\U0001F300-\U0001FAFF☀-➿]", own)) > 1:
        out.append(("WARN", "emoji garnish"))
    triads = re.findall(r"\b\w+(?: \w+)?, \w+(?: \w+)?,? (?:and|or) \w+", own)
    if len(triads) > TRIAD_MAX:
        out.append(("WARN", f"{len(triads)} lists of three; keep the ones that carry content"))
    hedges = len(re.findall(HEDGES, own, re.I))
    if words and hedges / words * 100 > HEDGES_PER_100_MAX:
        out.append(("WARN", f"{hedges} hedges; commit, or say exactly what you don't know"))
    sents = sentences(own)
    if sents and re.match(THROAT_CLEARING, sents[0].strip(), re.I):
        out.append(("FAIL", "first sentence announces instead of saying"))
    if sents and re.match(RECAP_CLOSE, sents[-1].strip(), re.I):
        out.append(("FAIL", "last sentence recaps; end on something that does work"))
    lengths = [len(s.split()) for s in sents]
    if len(lengths) >= MIN_SENTENCES_FOR_RHYTHM and statistics.pstdev(lengths) < RHYTHM_STDEV_MIN:
        out.append(("WARN", f"flat rhythm (sentence length stdev {statistics.pstdev(lengths):.1f}); vary it"))
    long_ones = [n for n in lengths if n > LONG_SENTENCE]
    if long_ones:
        out.append(("WARN", f"{len(long_ones)} sentence(s) over {LONG_SENTENCE} words"))
    expo = re.findall(EXPOSITION, own, re.I)
    if len(expo) > EXPOSITION_MAX:
        out.append(("WARN", f"{len(expo)} explaining/bridge phrases ({', '.join(sorted({e[0].strip().lower() for e in expo}))}); "
                            "trust the reader, see presence.md"))
    if form in BUTTON_FORMS:
        paras = [p for p in re.split(r"\n\s*\n", own) if p.strip() and not re.match(r"\s*([#>`-]|\*\s|\d+\.)", p)]
        buttons = 0
        for p in paras:
            ps = sentences(p)
            if len(ps) >= 3 and len(ps[-1].split()) <= BUTTON_WORDS:
                buttons += 1
        if buttons > BUTTON_MAX:
            out.append(("WARN", f"{buttons} paragraphs end on a short punchy line; keep one or two, end the rest on plain facts"))
    bullets = re.findall(r"^\s*[-*]\s+", text, re.M)
    if len(bullets) > max_bullets:
        out.append(("WARN", f"{len(bullets)} bullets; keep the ones that change a decision"))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--form", choices=FORMS, default="any")
    args = ap.parse_args()
    findings = check(Path(args.file).read_text(encoding="utf8"), args.form)
    for level, msg in findings:
        print(f"{level}: {msg}")
    if not findings:
        print("clean")
    sys.exit(1 if any(level == "FAIL" for level, _ in findings) else 0)


if __name__ == "__main__":
    main()
