## Fetch Filtered GoatCounter Stats to Monthly CSV (`get-site-stats.yml`)
- **Trigger Events:** Manual workflow dispatch, scheduled weekly (Mondays at 08:00 UTC), or on the 1st of every month to lock in closed monthly totals.

Automates privacy-preserving web analytics tracking by querying the GoatCounter API (`moleevolution`). The aggregated totals are written to `stats/monthly_traffic.csv`, and the updated statistics file is automatically committed and pushed back to the repository.

## Sync Tracking Issues (`track-issues.yml`)
- **Trigger Events:** Manual workflow dispatch.

Performs cross-repository synchronization for workshop logistics. It checks out the current repository alongside both the primary `molevolworkshop.github.io` website repo and the `moledata` repo, then executes an internal Python script to create github issues for all the labs, lectures, and faculty profiles. Each respective type has a corresponding tag so that anybody may filter issues based on the desired type. These are meant for tracking issues as they are completed in their respective repos.
