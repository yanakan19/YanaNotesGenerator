# YanaNotesGenerator

Turn a folder of lecture slides, worksheets, solutions and revision decks into **compact, complete, uniformly formatted LaTeX study notes**, one command, every module, every week.

`/YanaNotesGenerator` reads every page as an image, crops the diagrams that matter straight from the originals, drafts a master markdown it can later answer questions from, and compiles a print ready PDF. Formatting is identical across every document because it all comes from one shared style file, so a tweak there restyles every week of every module on recompile.

> **Visual walkthrough of the pipeline:** open [`docs/how-it-works.html`](docs/how-it-works.html) in a browser.
> **Which model to run it on:** see [`docs/MODEL.md`](docs/MODEL.md) (short answer: Claude Sonnet with thinking on).

---

## Quick start

**Already set up?** A weekly run is three steps:

1. Drop the week's files into `ES327/Week 05/sources/`, **in the order they were delivered** (Part 1 before Part 2, revision deck last; the pipeline reads files by upload time).
2. Open a fresh chat in that module's Cowork project.
3. Run `/YanaNotesGenerator Week 5`.

It runs on its own to a compiled PDF, commits, and pushes. Then ask it anything from the week in the same chat.

**First time on a new machine?** See [Installation](#installation) below.

---

## What it produces

For `ES327 Week 5` you get, in `ES327/Week 05/`:

| File | What it is |
| --- | --- |
| `ES327_Week05_Notes.pdf` | the finished notes, print ready as a booklet |
| `ES327_Week05_Notes.tex` | the LaTeX source (imports the shared style) |
| `ES327_Week05_Notes.md` | the **master markdown**, the recall source tutor mode reads |
| `figures/*.png` | diagrams cropped from the original slides at 300 DPI |
| `extraction/*.md` | the per file vision cache (checkpoint, one per source PDF) |

The PDF always has: a title block, a one page contents, lecture content in delivery order, a Key Summary, a Worked Examples Q&A section, and a Revision Questions and Answers section.

---

## Repository layout

```
YanaNotesGenerator/
├── .claude/commands/YanaNotesGenerator.md   # the command itself
├── templates/
│   ├── uninotes.sty            # ALL shared styling lives here (single source of uniformity)
│   ├── week_template.tex       # skeleton each week's .tex is built from
│   └── module_template.md      # blank module.md, copied when scaffolding a module
├── scripts/
│   └── render_pages.ps1        # pdftoppm wrapper: page render (150 DPI) + figure crop (300 DPI)
├── docs/
│   ├── how-it-works.html       # visual pipeline guide
│   └── MODEL.md                # which Claude model to run this on, and why
└── <MODULE CODE>/              # one folder per module, e.g. ES386/, ES327/
    ├── module.md               # module code + full name (drives every page header)
    └── Week NN/
        ├── sources/            # you upload lecture PDFs, worksheets, solutions here
        ├── extraction/         # generated: checkpointed vision cache
        ├── figures/            # generated: cropped diagrams
        ├── pages-cache/        # generated, gitignored: rendered page images
        └── <CODE>_WeekNN_Notes.{md,tex,pdf}   # generated outputs
```

Only `sources/` is yours; everything else in a week folder is generated. `pages-cache/` is the one thing not committed (bulky and regenerable); the notes, the markdown and even the extraction cache are all versioned so a `git clone` restores everything.

---

## The five capabilities

The one command routes on what you give it:

| Say | It does |
| --- | --- |
| `/YanaNotesGenerator Week 5` | **GENERATE** the week's notes end to end (the default). |
| `explain mode superposition` / `quiz me on week 3` | **TUTOR** from the master markdown only, never re-reading a PDF, so recall is near free. |
| upload a worksheet + solutions after notes exist | **WORKSHEET**: fold each solved problem into that week's Worked Examples, then recompile. |
| `set up module ES327 Design of Mechanical Systems` | **NEW MODULE**: scaffold `module.md` and a folder per teaching week. |
| `sync` / `push` | **SYNC**: commit and push on demand. |

Run it with no arguments to see the menu.

---

## How a generation run works

Seven stages, each writing to disk before the next, so an interrupted run resumes for free:

1. **Inventory** `sources/` by upload time and classify each file.
2. **Render** each PDF to page images at 150 DPI (`pages-cache/`).
3. **Vision extract**, five to six pages per batch, appending to `extraction/<file>.md` after every batch. A file stamped `EXTRACTION COMPLETE` is never read again, so no page is ever vision read twice.
4. **Crop** crucial diagrams from the original page at 300 DPI (`figures/`).
5. **Draft** the master markdown from the extractions (the tutor recall source).
6. **Transform** to LaTeX on the shared style and **compile** twice with `pdflatex`.
7. **Lint** prose for stray dashes, then **commit and push**.

Full illustrated version in [`docs/how-it-works.html`](docs/how-it-works.html).

---

## Formatting contract

Enforced by the command on every document, so all notes look identical:

- **Header** reads `MODULECODE: Module Name - Week N Notes`; page numbers centred in the footer; a one page contents; tight booklet margins for printing.
- **No dashes or hyphens in prose**, so text pastes cleanly into an open book exam answer; line break hyphenation is disabled too.
- **Every equation** is centred and followed on first use by a `Term: FullName (UNITS)` variable list.
- **Worked examples and revision questions** are in Q&A format with `Step X:` explanations mirroring the official solution method.
- **A Key Summary** closes every week.

All of this is defined once in `templates/uninotes.sty`. Change a colour or margin there and every module restyles on next compile.

---

## Recommended model

Run the command on **Claude Sonnet with extended thinking enabled**. It is fast, cheap per page, and reliable at structured vision extraction, which is what a 150+ page week needs; the hard consistency work is carried by the command's rules, not the model. Full reasoning in [`docs/MODEL.md`](docs/MODEL.md).

---

## Installation

Prerequisites: **MiKTeX** (provides `pdflatex` and `pdftoppm`), **Git**, and optionally the **GitHub CLI** (`gh`) for one line repo setup.

1. **Clone** onto a machine:
   ```powershell
   git clone https://github.com/yanakan19/YanaNotesGenerator.git C:\Users\mryx1\repos\YanaNotesGenerator
   ```
   The command uses absolute paths under `C:\Users\mryx1\repos\YanaNotesGenerator`; clone there, or update the paths in `.claude/commands/YanaNotesGenerator.md` and `docs/MODEL.md` if you clone elsewhere.

2. **Make the command global** so it works in any session, not just this repo:
   ```powershell
   Copy-Item ".\.claude\commands\YanaNotesGenerator.md" "$env:USERPROFILE\.claude\commands\YanaNotesGenerator.md" -Force
   ```

3. **Enable MiKTeX auto install** of missing packages (first compile pulls a few):
   ```powershell
   initexmf --set-config-value="[MPM]AutoInstall=1"
   ```

4. **Scaffold your first module** in a chat: `/YanaNotesGenerator set up module ES327 Design of Mechanical Systems`.

### Cowork setup (once per module)

1. New Cowork project, named after the module.
2. Point its folder at `C:\Users\mryx1\repos\YanaNotesGenerator\<MODULE CODE>` (or the repo root for one project across all modules).
3. Because the command is installed globally, it is available in every chat there.

### GitHub

This repo is `YanaNotesGenerator` under the `yanakan19` account. To connect a fresh clone:

```powershell
gh auth login          # browser login, GitHub.com + HTTPS
git remote add origin https://github.com/yanakan19/YanaNotesGenerator.git
git push -u origin main
```

After that the command pushes automatically at the end of every generation run; force one any time with `/YanaNotesGenerator sync`.

---

## Compile a week by hand

Rarely needed (the command does it), but if you want to:

```powershell
Set-Location "C:\Users\mryx1\repos\YanaNotesGenerator\<MODULE>\Week NN"
$env:TEXINPUTS = ".;C:\Users\mryx1\repos\YanaNotesGenerator\templates;"
pdflatex -interaction=nonstopmode <CODE>_WeekNN_Notes.tex   # run twice
```

---

## Worked reference: ES386 Week 6

The repo ships one fully worked week (Units 6 and 7 of ES386, two lecture decks plus a worksheet and a handout, 89 slide pages) as a live example of the output: `ES386/Week 06/ES386_Week06_Notes.pdf`. Use it as the visual target for what a generated week should look like.
