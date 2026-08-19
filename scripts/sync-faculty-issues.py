import csv
import os
import subprocess
import json

def get_existing_issues():
    # Fetch all open issues to check for duplicates
    result = subprocess.run(
        ["gh", "issue", "list", "--state", "open", "--limit", "200", "--json", "title"],
        capture_output=True, text=True, check=True
    )
    issues = json.loads(result.stdout)
    return {issue["title"] for issue in issues}

def create_issue(title, body, labels):
    cmd = ["gh", "issue", "create", "--title", title, "--body", body]
    for label in labels:
        cmd.extend(["--label", label])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Created: {title}")
    else:
        print(f"Failed to create '{title}': {result.stderr.strip()}")

def check_bio_status(fac_id, name):
    """
    Checks if the faculty member's markdown file exists in the checked-out website repo 
    and whether it still contains placeholder text or is missing entirely.
    """
    # Fallback slug generation matching your site's format
    slug = fac_id if fac_id else name.lower().replace(r"[^a-z0-9\s-]", "").replace(" ", "-")
    md_path = os.path.join("website-repo", "_faculty", f"{slug}.md")

    if not os.path.exists(md_path):
        return True # Missing file counts as missing bio

    try:
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Check if it only has the template / placeholder text
            if "Faculty bio coming soon!" in content or len(content.strip()) < 150:
                return True
    except Exception as e:
        print(f"Error reading {md_path}: {e}")
        
    return False

def main():
    existing_titles = get_existing_issues()

    # Path to registry inside the checked-out website repository directory
    registry_path = os.path.join("website-repo", "_data", "faculty-registry.csv")

    # 1. Sync Faculty Registry Issues
    with open(registry_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            fac_id = row["ID"]
            role = row["role"]
            
            title = f"Review & Update Faculty Page: {name}"
            if title not in existing_titles:
                body = (
                    f"Please verify and update the profile page for **{name}**.\n\n"
                    f"- **Registry ID:** `{fac_id}`\n"
                    f"- **Role:** {role}\n\n"
                    f"You can find the page [here](https://molevolworkshop.github.io/faculty/{fac_id}/)\n"
                    f"Instructions for udpating the page can be found [here](https://github.com/molevolworkshop/molevolworkshop.github.io/tree/main/_faculty)"
                )
                
                # Base labels for all faculty page issues
                labels = ["faculty-page", "needs-review"]
                
                # Conditionally add 'missing-bio' if the md file is blank/template
                if check_bio_status(fac_id, name):
                    labels.append("missing")

                create_issue(title, body, labels)
"""
    # 2. Sync Event Schedule Issues (Lectures & Labs)
    with open("_data/event-schedule.csv", mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            category = row["category"]
            if category in ["lecture", "lab"]:
                title = f"Verify {category.capitalize()}: {row['title']} ({row['date']})"
                if title not in existing_titles:
                    presenter = row.get("presenter", "Unassigned")
                    material = row.get("material_location", "")
                    
                    body = (
                        f"Please review materials and details for this session.\n\n"
                        f"- **Date:** {row['date']} ({row['start_time']} - {row['end_time']})\n"
                        f"- **Room:** {row['room']}\n"
                        f"- **Presenter ID:** `{presenter}`\n"
                        f"- **Current Material Link:** `{material}`\n\n"
                        f"### Checklist\n"
                        f"- [ ] Confirm slides/code repository link is up to date\n"
                        f"- [ ] Verify room assignment and schedule time"
                    )
                    create_issue(title, body, ["type: session-material", "status: needs-review"])
"""


if __name__ == "__main__":
    main()