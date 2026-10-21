# human-voice

A Claude skill for writing anything (blog posts, emails, chat replies, posts, explainers, release notes, apologies)
so it reads like one sharp, warm person and not like AI slop.

It started as a study of Wilson, the r/ClaudeAI TL;DR bot, and grew into a general writing skill shaped by research
and blind A/B judging.

## What's inside
- `SKILL.md`: seven moves (point first, specifics over adjectives, borrow the world's wit, jokes at the edges,
  the turn, honest sizing, land it), the voice rules, an 8-step process and a wit dial from 0 to 3.
- `references/recipes.md`: shapes for 12 forms.
- `references/devices.md`: hooks, turns, closers, sentence moves and a slop-to-plain swap table.
- `references/humor.md`: the voice behind the jokes, how to build one joke, three tests (relevant, benign, true)
  and where jokes go.
- `references/examples.md`: 12 annotated before-and-after pairs.
- `scripts/slop_check.py`: a linter for AI tells, style-word density, reading grade, repeated phrases and flat
  rhythm. `python scripts/slop_check.py draft.md --form blog|email|post|reply|chat|summary|notes|any`
- `scripts/quote_check.py`: proves every quoted line is verbatim in the source.

## Install
Copy the `human-voice` folder into `~/.claude/skills/`. Claude Code picks it up the next time a session starts.

## Evidence
- Wikipedia, "Signs of AI writing"
- Kobak et al., "Delving into LLM-assisted writing in biomedical publications through excess vocabulary"
  (Science Advances, 2025)
- Paech et al., "Antislop" (2025)
- Rogers and Lasky-Fink, "Writing for Busy Readers"
- Pinker, "The Sense of Style"
- ISO 24495-1 (plain language)
- Nielsen Norman Group reading research
- Doshi and Hauser, Science Advances 2024
- McGraw and Warren (benign violation)
- Bitterly, Brooks and Schweitzer (JPSP 2017)
- Greg Dean and Judy Carter on joke structure
- Jentzsch and Kersting (2023) on repetitive ChatGPT jokes

Blind judging, with two model judges and shuffled labels: each version beat the one before it. Across three
rounds, the later version won 25 of 30 judgements. These are model judges, not human readers.

## Licence
MIT. See `LICENSE`.
