# MOLE faculty contribution system

How faculty submit their materials each year, and how the system is set up and run.



## Faculty Contributions

There are three main items that faculty will update regarding mole-terials:
- Bio page on the website
- Lecture materials
- Lab materials 

Each of these items have their own specific formatting requirements and directory structures.
For standardization and maintainance, it is vital that these standards are maintained. However edits are made, the key is to use PRs as the quality control check.

## Yearly activity (director)

Each year, once the director has the appropriate information, the directory should update the registries:

- `molevolworkshop.github.io/_data/faculty-registry.csv` with current faculty 
- `moledata/_data/materials-registry.csv` with the labs and lectures for the year
- `molevolworkshop.github.io/_data/former-faculty.csv` with faculty not returning
- `molevolworkshop.github.io/_data/event-registry.csv` with non-lab/lecture events to put in the schedule
- `molevolworkshop.github.io/_data/event-schedule.csv` with the schedule, using item id's from the `materials-registry` and `event-registry` 
- `molevolworkshop.github.io/_data/participants.csv` with current participants

With these up to date, many of the issue templates and automated steps will update automatically.

Once you are satisfied with updates (no worries if you don't have all the information, things can ad hoc be updated),
you can use the `track-issues` Github action in `mole-logistics` to create an issue for all items that faculty should update.
These issues serve mostly for the directors to keep track of things; you should direct faculty to the contributing pages for the specific item they are requested to update.
The automatically created issues, should have links to the appropriate resource. Ultimately, however, they will create issues/PRs in the repo containing the requested changes, **not** `mole-logistics`.
Once a faculty member has made the appropriate changes you can close the issue in `mole-logistics` to track what needs to be done yet.
Depending on how the PR was submitted and formatted, the `mole-logisitics` issue may close automatically.



## To do
- make sure all PRs link to mole-logistics for tracking
- use issues to create a project board 