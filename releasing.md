# Releasing (freezing) a year's materials

At the end of each workshop, we **freeze that year** by cutting a GitHub **Release** on each
of the three working repos. A Release permanently tags the repo at that moment and gives a
dated, downloadable snapshot — so anyone can always go back to exactly what a given year
looked like.

**Because the repos only ever hold the _current_ year, this release is the only record of
the year. Don't skip it.**

## The three repos to release

- `moledata` — slides and lab materials
- `molevolworkshop.github.io` — the website
- `mole-logistics` — this playbook

## Tag name

Use the **plain year** as the tag: `2027`. One release per repo per year, the same tag on all
three, so a given year lines up across them.

## Steps (GitHub website — no command line needed)

Do this for **each** of the three repos:

1. Open the repo on GitHub → **Releases** (right-hand sidebar) → **Draft a new release**.
2. **Choose a tag** → type the year (e.g. `2027`) → **Create new tag: 2027 on publish**.
3. Leave the target as **`main`**.
4. **Release title:** `MOLE 2027`.
5. _(Optional)_ Add a short description — dates, location, anything notable that year.
6. Click **Publish release**.

GitHub then creates the tag, a release page, and a downloadable `Source code (zip / tar.gz)`
capturing every file at that moment (moledata's Git LFS files are included).

## To look at a past year later

Go to the repo's **Releases** page and pick the year — download its zip, or use the tag
dropdown to browse the repo "as of" that tag.

## Optional extras (not required)

- **Faster, if you use the `gh` CLI:** one line per repo —
  `gh release create 2027 --title "MOLE 2027" --notes "..."`.
- **Citable archive (DOI):** connect a repo to [Zenodo](https://zenodo.org) once; after that,
  every GitHub Release automatically gets a DOI, making that year's materials citable. Nice for
  an academic workshop, but entirely optional.

> We deliberately keep this a **manual, few-minute task** rather than automating it across
> repos — it happens once a year, and a simple checklist a rotating director can follow beats a
> fragile cross-repo automation to maintain.
