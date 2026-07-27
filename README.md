# MOLE workshop organization logistics

Important things for MOLE 2027:
- Apply to ACCESS extension on July 20, 2026 (needs to be done by Tracy Heath or Jeremy Brown as PIs)
    - **Done** on July 16 by Jeremy and Claudia [notes](https://github.com/molevolworkshop/mole-logistics/tree/main/virtual-machines)
- Add a session after the (optional) ethics where faculty/participants present the types of activites they have worked on to move the needle and have an impact in the state of the world
- Consider moving Joe's first part of lecture earlier (1st day?)

Post 2026 workshop to-do items:
- port slack to discord 

# README

The organizational playbook for the [Workshop on Molecular Evolution (MOLE)](https://molevolworkshop.github.io/), held each May at the MBL in Woods Hole. This repo covers the *running* of the workshop — timeline, director duties, TA/CA info, virtual machines, and participant communications. It doesn't hold course materials or the website; see [Other MOLE repos](#other-mole-repos) below.

If you're new here: start with [timeline.md](#timelinemd) for the year-by-year checklist, and [day2day-director.md](#day2day-directormd) for what to watch during the workshop itself.

## Contents

### Running the workshop

- [`timeline.md`](timeline.md) — the year-by-year checklist for the director(s), from the ACCESS allocation renewal through to shelving the VMs at the end of the workshop. Start here when planning the next MOLE.
- [`day2day-director.md`](day2day-director.md) — a short checklist of things to keep an eye on while the workshop is actually running (socials, reimbursements, certificates).
- [`releasing.md`](releasing.md) — how to freeze a finished workshop year as a tagged GitHub Release across `moledata`, the website, and this repo, so any past year stays recoverable.
- [`faculty-contribution-system.md`](faculty-contribution-system.md) — how faculty contribute slides/bios via the org-level Project board (Josh's one-time setup), and what the director does each year to run that process.

### TA / CA reference

- [`tas-info/`](tas-info/) — handbooks for the teaching assistants and course assistant: roles, break/supply logistics, the t-shirt contest, and per-lab notes. See [`tas-info/README.md`](tas-info/README.md) for the full index.

### Virtual machines

- [`virtual-machines/`](virtual-machines/) — setting up the ACCESS/Jetstream2 allocation and the participant/faculty VMs.
    - [`virtual-machines/README.md`](virtual-machines/README.md) — overview of the VM setup process and folder layout.
    - `virtual-machines/jetstream2026.md` — the detailed, step-by-step VM build guide.
    - `virtual-machines/ssh.md` — collecting and using participant/faculty SSH keys.
    - `virtual-machines/late-additions/` — dated scripts for managing already-running VMs (replacing files, shelving/unshelving, locking/unlocking). See its own [README](virtual-machines/late-additions/README.md).

### Participant communications

- [`emails/welcome-participants.md`](emails/welcome-participants.md) — the pre-workshop welcome email template.
- [`name-tags/`](name-tags/) — generating printable name tags (with VM IP addresses on the back) from the faculty/student roster. See [`name-tags/readme.md`](name-tags/readme.md).

## Other MOLE repos

All under [github.com/molevolworkshop](https://github.com/molevolworkshop):

- [`molevolworkshop.github.io`](https://github.com/molevolworkshop/molevolworkshop.github.io) — the workshop website (Jekyll: bios, schedule).
- [`moledata`](https://github.com/molevolworkshop/moledata) — course materials: lecture slides (`lectures/`) and lab data (`labs/`).
- [`molevolworkshop.github.io-archive`](https://github.com/molevolworkshop/molevolworkshop.github.io-archive) — the old, pre-2026 website, archived/frozen.
