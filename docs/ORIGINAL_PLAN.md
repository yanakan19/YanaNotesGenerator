# Original design plan (historical record)

This is the plan that was approved before the first line of this project was written. Names in
it are the FIRST names used and have since been renamed twice: `tailor-notes` then
`yana-notes-generator` then the current `YanaNotesGenerator`; `uni-notes` then
`yana-notes-generator` then the current repo `YanaNotesGenerator`. Everything else in it,
the formatting contract, the checkpointed pipeline, the writing rules, is still the design in
force today, refined since (see `README.md` and `docs/MODEL.md` for the current state, this
file is kept as the record of why it was built this way).

Known deltas since this plan was written, current behaviour supersedes the text below where
they conflict:
- Margins are 1cm all around (this plan said approximately 1.6cm during early tuning).
- The header sits in the TOP RIGHT and reads `CODE Module Name - Week N : Week Title`
  (this plan specified a centred header without a week title).
- `templates/uninotes.sty` `\notesmodule` macro takes 4 arguments now (code, name, week
  number, week title), not 3.
- Vision extraction (capability A step 3) fans out one Task subagent per unfinished source
  file in parallel rather than reading every source in one thread, batches are 4 to 5 pages
  not 8 to 10, tuned to maximise notes throughput per session on Sonnet class models.
- Every generation run always attaches the PDF, the `.tex`, and the master `.md` in chat.

---

## Plan: Universal University Notes Command + Repo

### Context

Yanakan is starting a new Mechanical Engineering academic year and wants a repeatable
Claude/Cowork workflow that converts uploaded module resources (lecture slides, worksheets
and solutions, revision decks, extras) into compact, complete, uniformly formatted notes. A
previous ad hoc run worked but had weaknesses this design fixes: the template lived in one
deletable chat (now lost), a mid run API error nearly lost 158 pages of vision work (no
checkpointing), tcolorbox title commas caused compile errors, a file was written to the wrong
path, and every run re read PDFs (token expensive). The chosen approach: rebuild the template
fresh, one universal command for all modules, GitHub CLI, repo outside OneDrive.

### Deliverables

A git repo containing a `.claude/commands/` command (router style), `templates/` (the shared
`.sty` style plus a week skeleton `.tex`), `scripts/` (a `pdftoppm` wrapper for page render and
figure crop), a `README.md`, and one folder per module, each containing `module.md` plus one
folder per teaching week (`sources/`, `extraction/`, `figures/`, and the generated
`.md/.tex/.pdf` outputs).

### 1. Shared LaTeX style

One `.sty` file every week imports so formatting is uniform by construction, and a style tweak
later restyles every week on recompile: compact geometry for booklet printing, a fixed header
and centred footer page numbers, a compact one page contents page, hyphenation disabled so
copied prose never breaks mid word, every formula followed by a variable glossary in the fixed
format `Term: FullName (UNITS)`, five braced title tcolorbox environments (definitions, key
results, worked examples, warnings, revision), and tight figure conventions.

Writing rules enforced by the command on every generated document: no dashes or hyphens in
direct prose so text copied into an open book exam answer reads naturally; uniform
subheadings, same hierarchy every week; every equation followed by its variable list on first
use; worked examples from lecture slides AND worksheets in Q&A format with numbered
`Step X:` explanations mirroring the official solution method; a Key Summary closing every
week.

### 2. The command

Capabilities: A, GENERATE a week end to end (inventory, render, vision extract with
checkpointing, crop figures, draft the master markdown, transform to LaTeX and compile,
commit and push); B, TUTOR from the master markdown only, never re reading source files; C,
WORKSHEET, fold a worksheet and its solutions into an existing week; D, NEW MODULE, scaffold a
module's folders in seconds; E, SYNC, manual commit and push.

Token discipline baked in from the start: the extraction cache is authoritative and a
completed source is never re vision read; page renders are cheap DPI; image reads are
batched; tutor mode is markdown only; the router body stays lean with formatting detail kept
in the style file, not the prompt.

### 3. Cowork usage pattern

One Cowork project per module, its folder pointed at the module's folder in the repo (the
command works in any chat because it is also installed globally). One chat per week: drop
that week's files into the week's `sources/` folder, open a fresh chat, run the command
naming the week. Ask follow up questions in the same chat, tutor mode recalls from the
markdown.

### 4. GitHub

Install the GitHub CLI, authenticate once, create the repo, and push. After that pushes are
automatic at the end of every generation run.

### Verification (all completed)

Compile a demo exercising every box environment, a table, a cropped figure, a variable list
block, a one page contents page, and the header and footer format, confirm a clean PDF. Lint
the demo and every generated document for zero dashes or hyphens in prose. Run the full
pipeline on a tiny sample PDF end to end and confirm the extraction skip on rerun works. Push
to GitHub and confirm the repo. Pilot on one real week of slides as the true end to end test,
shipped as `ES386/Week 06` in this repo.
