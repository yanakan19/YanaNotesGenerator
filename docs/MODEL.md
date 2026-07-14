# Model recommendation for /YanaNotesGenerator

**Run this command on a Claude Sonnet model with extended thinking (thinking mode) enabled.**

## Why Sonnet thinking, not Opus

Generating a week of notes is a long, mechanical, high volume job: render 150+ slide pages, vision read every one, transform structured extractions into LaTeX, compile. It is not a job that needs Opus level reasoning; it needs stamina, consistency, and low cost per page. Sonnet with thinking is the sweet spot:

- **Cost and speed.** A single week can be 150 to 250 page reads plus a large LaTeX synthesis. Sonnet is far cheaper per token and faster, which matters when this runs every week of term across several modules.
- **Vision extraction is structured, not open ended.** Reading a slide into "text, equations to LaTeX, tables to tabular, figures to crop markers" is pattern work. Sonnet does this reliably, and thinking mode gives it room to get equations and matrices right before writing them.
- **The hard reasoning is offloaded to rules, not the model.** Uniform formatting, `Term: FullName (UNITS)` varlists, `Step X:` worked examples, braced box titles, the no dash rule: these are prescriptive and identical every week. The command carries the intelligence; the model just applies it.

Opus is not wrong here, just overkill for the money. Reserve Opus for genuinely hard one off reasoning (a confusing derivation, a subtle bug in a compile). For the weekly grind, Sonnet thinking wins.

## What the command does to keep Sonnet reliable

1. **Small checkpointed batches (5 to 6 pages).** Each batch is appended to `extraction/<file>.md` before the next is read. A mid size model is most accurate on focused turns, and this makes any interruption free to resume (the skip rule never re-visions a completed file).
2. **The files are the memory.** The model never has to hold a whole week in context: extractions feed the master markdown, and the markdown is the sole source for tutor mode. This keeps every turn's working set small.
3. **Literal numbered steps (A1 to A9).** One phase at a time, in order, so the model is never improvising structure.

## Practical setup

- In Cowork or Claude Code, select a Sonnet model and turn thinking on before running `/YanaNotesGenerator`.
- If a specific step needs deeper reasoning (a messy derivation in a revision answer), you can switch to Opus for that one question in tutor mode, then switch back.
- Everything else in the workflow (the LaTeX style, the repo layout, the GitHub sync) is model independent.
