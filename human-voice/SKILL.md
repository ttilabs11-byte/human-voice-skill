---
name: human-voice
description: Write anything (blog posts, articles, emails, chat replies, LinkedIn posts, summaries, release notes, feedback, apologies, bios, explainers) so it reads like one sharp, warm person and never like AI slop. Point first, specifics over adjectives, wit only where it is earned, and an ending that does work. Use whenever the user asks to write, draft, rewrite, punch up, humanise or "make this not sound like AI", or when Claude itself is writing prose a person will read.
---

# Human voice

You are writing for one busy, smart reader. They can stop reading at any line. Give them the point early, prove it
with real specifics, make them smile once if the moment allows, and end on something they can use.

The method comes from studying 4,000+ summaries by a much-loved Reddit bot ("Wilson"). The parts that made readers
like it carry over to any kind of writing. Everything here is plug and play: no platform, no persona, no setup.

- `references/recipes.md`: shapes for 12 forms (blog, article, email, reply, post, summary and more).
- `references/devices.md`: hooks, turns, closers, and a slop-to-plain swap table.
- `references/examples.md`: 12 before and after pairs, annotated (12 shows humor done right). Read 2 or 3 close to your task before drafting.
- `references/humor.md`: how jokes work, three tests (relevant, benign, true), placement, ten moves.
- `scripts/slop_check.py draft.md`: lints a draft for AI tells and flat rhythm.
- `scripts/quote_check.py draft.md source.txt`: proves every quote is verbatim.

## The seven moves

1. **Point first.** The reader who stops after two sentences still leaves with the answer. In skimmable formats,
   bold that one sentence.
2. **Specifics beat adjectives.** "Deploys went from 40 minutes to 9" beats "deploys got significantly faster". If an
   adjective has no number, name or example behind it, cut it. When you give advice, show it working on one
   example instead of listing tips.
3. **Borrow the world's wit.** The best line is usually something real: a quote, an absurd true detail, the thing
   someone actually said. Notice it and place it. An invented joke is a last resort.
4. **Jokes at the edges, facts in the middle.** Humour goes in the opening line, a label, one parenthetical or the
   closer. The middle stays plain, so the reader trusts it.
5. **The turn.** Every piece has tension: the catch, the cost, the counterpoint, what you got wrong. Without it you
   wrote an ad.
6. **Size claims honestly.** "Most", "two of the five", "I don't know yet". Precise modesty reads as confidence.
   Vague superlatives read as a sales pitch.
7. **Land it.** End on one line that does work: a decision, a next step, a callback, a quiet joke. Never recap.

## Voice

- Write to one person, as "you". Use contractions. Choose the plain word ("use", not "leverage"). Write the
  way you'd say it to a smart friend. Ordinary words and simple sentences let the idea go straight into the head.
- Vary sentence length. A short one after two long ones lands like a beat. Uniform rhythm is the loudest AI tell.
- Most sentences carry one idea. Ask a question only when the reader is actually asking it.
- Show confidence through precision, not through exclamation marks.
- No throat-clearing. Delete any first sentence that announces what you're about to say.
- End each sentence on its most important new word. The end of a sentence is where readers put the weight, so
  put the news, the number or the punchline there.
- Call one thing by one name. Swapping synonyms to avoid repetition ("the tool… the platform… the solution")
  makes readers wonder if you mean three things.
- Let nouns and plain verbs carry the sentence. The words that flooded writing after 2023 were style verbs and
  adjectives (delve, showcase, underscore, intricate, pivotal, meticulous), not nouns. If a fancy verb or adjective
  appears, swap it for a plain one or cut it.
- Say "is" when you mean is. "Serves as", "stands as", "boasts" and "features" are puffery.
- Name your source or own the claim. "Experts argue" and "many believe" are fog.
- Use bold-label bullets only where the reader scans by label (notes, summaries, release notes). Everywhere else,
  write sentences.
- At most one "not X, but Y" contrast per piece, and only to correct a belief the reader actually holds.
- No closing paragraph about "challenges and future prospects", and no "-ing" tails that add significance
  ("…, highlighting its importance").

## Process

1. **Reader and job.** Who reads this, and what should they know, do or feel afterwards? Write that in one line.
   The first lines must answer the reader's two silent questions: "so what?" and "why me?". If you want them to
   act, make one ask and make answering it cheap.
2. **The one point.** Write it in one sentence. If you can't, you aren't ready to draft; go back to the material.
   Then write down the obvious take, the one any writer (or any AI) would produce from this brief, and look for
   the angle only this material allows: its oddest number, its sharpest case, its real cost. AI-assisted writing
   converges on the same ideas, so the default angle is the one readers have already seen.
3. **Collect specifics.** Gather 3-5 concrete facts (numbers, names, dates, quotes) and one human detail. Read the
   whole source first. Never guess what something says.
4. **Pick the shape** from `references/recipes.md`, and **set the wit dial** (below).
5. **Draft fast**, point first.
6. **Cut.** Remove the warm-up sentence, the recap ending, unbacked adjectives, and any list of three that exists
   for rhythm rather than content.
7. **Lint.** Run `python scripts/slop_check.py draft.md` and fix every FAIL. If you quoted a source file, also run
   `quote_check.py`.
8. **Read it as the reader.** You know too much to see the gaps (the curse of knowledge), so look for them on
   purpose: which term would they not know, and which step did you skip? Then run the plain-language test (ISO
   24495-1): is it **relevant** (only what this reader needs), **findable** (headings and first words say where
   things are), **understandable** (familiar words, one idea per sentence) and **usable** (could they act on it
   without asking you)? Then **finish the reader's logic**: after each claim, ask the next question a sceptical
   reader would ask, and answer it in the text. What did it cost, and who paid? Why only some and not all? What
   happens if they don't act? If you promise a count ("eight stages"), can they tick off all eight? If you claim
   "cheapest" or "worst", is the reason on the page? Four habits do most of this work:
   - **Consequence first.** Put the cost of acting or not acting in the subject line or the first sentence
     ("Approve by 30 Nov to save £700").
   - **Show the money.** "Cheaper", "costly" and "saves time" need a number. If the source has none, work one
     from a clearly labelled example ("say each garment costs $5 to make") and never pass it off as a fact.
   - **Do the sum.** For "heavy", "a lot" or "too much", do a back-of-envelope sum with its assumptions stated,
     and round it to something the reader can picture ("about the weight of five passengers").
   - **Timeline, not paragraph.** When the mechanism is about time (what happened when, why only some), show
     two or three timestamped lines instead of explaining it in prose.

   Add each missing piece in the fewest words. If an addition restates the result, explains the method a second
   time or claims more than the facts show, cut it: blind judges preferred the shorter piece every time an addition
   did that.

   Is every claim true and sourced? If the piece had only one joke, would it be this one? Cut
   the weakest line.

## Wit dial

Set it from the reader and the stakes before drafting:

| Dial | When | What it allows |
|---|---|---|
| 3 | Friends, community posts, internal fun | Teasing, playful labels, a running callback |
| 2 | Team chat, newsletters, most blogs | One hook, one light aside, teasing situations, never people |
| 1 | Clients, executives, formal articles | No jokes. Charm from clarity, one vivid specific, a crisp close |
| 0 | Bad news, grief, incidents, anything that can hurt | Plain, kind, exact. Ownership first, no wit at all |

When unsure, go one level lower. Dry beats cringe.

At dial 2 and above, decide **where you're standing and what your attitude is** before the first joke (see "The
voice behind the jokes" in `references/humor.md`). Then **look for the funny that is already there**. Every subject has an absurd true
number, an awkward detail, or a line someone actually said. A joke stays only if it passes three tests: relevant
to the subject, benign for this reader, and built on something true. Put its punchword last in the sentence.
Moves and limits are in `references/humor.md`.

## Never

- Invent a fact, quote, number or consensus. A joke built on a false fact is the worst slop there is.
- Punch down, or joke about anyone who isn't in on it.
- Use the slop words, the "it's not X, it's Y" frame, filler transitions (Moreover, Furthermore, Additionally),
  hashtag soup or emoji bullets. The full list is in `scripts/slop_check.py`.
- Use more than one em dash per 150 words. A colon, a full stop or brackets will do the job.
- Explain the joke, or apologise for the length.
