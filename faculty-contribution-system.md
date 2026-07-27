# MOLE faculty contribution system

How faculty submit their materials each year, and how the system is set up and run.

**Josh owns the one-time setup.** The rotating **director** runs the yearly activity.
Golden rule throughout: **faculty must never be _required_ to use GitHub** — emailing the
director their files is always a valid path.

---

## One-time planning (Josh)

Build the reusable machinery once, so each year is a few minutes of operation.

- **Own `CONTRIBUTING.md`** going forward — the faculty-facing how-to in moledata (first
  draft is done and in the repo).

- **Decide the submission mechanics — Issues vs Pull Requests.** They do different jobs:
  - **Pull Requests = how materials come in.** A faculty member (or a TA / you, on their
    behalf) opens a PR: slides & labs → **moledata**, bio → the **website** repo. You review
    and merge. This is the gate that keeps `main` clean.
  - **Issues = how the director tracks who's done what.** One tracking issue per faculty with
    a checklist (slides ✓, bio ✓, lab ✓). It's a dashboard, not a task pushed onto faculty.

- **Build the reusable tracking setup:**
  - An **issue template** (`.github/ISSUE_TEMPLATE/faculty-checklist.md`): the checklist +
    deadlines + an "or just email the director your files" line.
  - **One org-level Project board.** GitHub Projects can be owned by the **organization**
    (`molevolworkshop`), not a single repo, and a project **can span multiple repositories** —
    so one board tracks the slides issues/PRs in moledata *and* the bio PRs in the website, in
    a single "who's behind?" view. Columns e.g. Not started / In progress / Done.
    - Caveat: the board is cross-repo, but **Project automation workflows are per-repo** — if
      you wire up auto-add / auto-move, configure it in each repo separately.
  - A **labels** convention and a **per-year milestone** (e.g. "MOLE 2027").

- **Optional automation (don't over-build):** a small Action that opens the year's faculty
  issues from a roster file.

**Design constraints (these matter):**

- **Never require faculty to touch GitHub.** Issues/board are the director's tracking layer;
  faculty can always just email, and you or a TA do the git part. If the system adds burden to
  faculty, it's the wrong design.
- **The bio is part of the contribution, not a separate thing.** A faculty's yearly submission
  is their slides/labs **and** their bio, together — one checklist, one reminder. (Bios are
  markdown in the website `faculty/` folder — kept as markdown deliberately, easy for non-savvy
  faculty.)
- **Keep the yearly operation light** for a rotating director — template + roster + board
  should make it a few minutes.

---

## Yearly activity (director)

Each year, using the setup above:

- Create that year's **milestone** and spin up (or clone) the **Project board**.
- Open **one tracking issue per faculty** from the roster, using the issue template.
- As materials arrive — PRs to moledata (slides/labs), PRs to the website (bios), or plain
  emails — tick the checklist and move the card.
- **Chase who's behind** from the board.

> This yearly activity is the **director's**, so it also belongs in the maintainer playbook
> (`mole-logistics`). Keep one source of truth: reference this doc from there rather than
> duplicating the steps.

---

## Context you'll need

- **Repos:** `moledata` (slides in `lectures/`, labs in `labs/`), the Jekyll website
  (`molevolworkshop.github.io`), and `mole-logistics` (the org playbook, incl. the annual
  `timeline.md`).
- **Naming standard (final, already applied):** lectures grouped **by faculty**
  (`lectures/<faculty>/<short-title>.pdf`, no year; companion files share the slide's prefix),
  lab folders in `snake_case`, current-year-only + one release per year.
- **The website** pulls moledata in at deploy as `materials/`, and `schedule.md` is the
  hand-maintained table linking every talk (moledata + off-site). A **link-checker** (GitHub
  Action in the website repo) flags broken links on every `schedule.md` change. moledata also
  auto-pings the website to rebuild on each push.

---

## Other shared items (not part of this system — decide together)

- **Post-workshop tag & release SOP** — a consistent tag scheme across the 3 repos + a
  one-step way to cut all releases, plus adding the release step into `timeline.md`. Underpins
  the whole current-year-only model.
- **Link-checker upgrade** — extend it to also verify internal permalink links and `faculty-`
  pages (it currently checks moledata file paths and off-site URLs).
- **Per-lab `README.md`s** for each lab folder. (The top-level `lectures/README.md` and
  `labs/README.md` are already refreshed.)
