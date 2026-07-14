# Model recommendation for /YanaNotesGenerator

**Run this command on a Claude Sonnet model, thinking mode on if available.** The pipeline is tuned to get the most weeks of notes out of one session's token budget, on a model with less reasoning headroom than Opus.

## Why Sonnet thinking, not Opus

Generating a week of notes is a long, mechanical, high volume job: render 150+ slide pages, vision read every one, transform structured extractions into LaTeX, compile. It is not a job that needs Opus level reasoning; it needs stamina, consistency, and low cost per page. Sonnet with thinking is the sweet spot:

- **Cost and speed.** A single week can be 150 to 250 page reads plus a large LaTeX synthesis. Sonnet is far cheaper per token and faster, which matters when this runs every week of term across several modules.
- **Vision extraction is structured, not open ended.** Reading a slide into "text, equations to LaTeX, tables to tabular, figures to crop markers" is pattern work. Sonnet does this reliably, and thinking mode gives it room to get equations and matrices right before writing them.
- **The hard reasoning is offloaded to rules, not the model.** Uniform formatting, `Term: FullName (UNITS)` varlists, `Step X:` worked examples, braced box titles, the no dash rule: these are prescriptive and identical every week. The command carries the intelligence; the model just applies it.

Opus is not wrong here, just overkill for the money. Reserve Opus for genuinely hard one off reasoning (a confusing derivation, a subtle bug in a compile). For the weekly grind, Sonnet thinking wins.

## What the command does to keep Sonnet reliable, and to maximise throughput

1. **Parallel subagent fan out for extraction.** When a week has several unfinished source files, the command dispatches one `Task` subagent per file instead of reading every source serially in one thread. Each subagent's context only ever holds its own file's pages, and it reports back a single line, not its full extraction (that is already checkpointed to disk). This is the main throughput lever: the orchestrating chat's context stays roughly flat regardless of how many total pages a week has, so a single session budget covers more sources, and more weeks, before it runs out.
2. **Small checkpointed batches (4 to 5 pages).** Each batch is appended to `extraction/<file>.md` before the next is read. A mid size model is most accurate on focused turns, and this makes any interruption free to resume (the skip rule never re-visions a completed file).
3. **The files are the memory.** The model never has to hold a whole week in context: extractions feed the master markdown, and the markdown is the sole source for tutor mode. This keeps every turn's working set small.
4. **Literal numbered steps (A1 to A9).** One phase at a time, in order, so the model is never improvising structure.
5. **Self aware of its own context budget.** If a run's chat is getting long, the command stops at the next checkpoint and tells the user to continue in a fresh chat rather than pushing through a degraded turn. Because every phase writes to disk before moving on, this costs nothing to resume.

## Practical setup

- In Cowork or Claude Code, select a Sonnet model and turn thinking on before running `/YanaNotesGenerator`.
- If a specific step needs deeper reasoning (a messy derivation in a revision answer), you can switch to Opus for that one question in tutor mode, then switch back.
- Everything else in the workflow (the LaTeX style, the repo layout, the GitHub sync) is model independent.
