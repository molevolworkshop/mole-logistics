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
    slug = fac_id if fac_id else name.lower().replace(r"[^a-z0-9\s-]", "").replace(" ", "-")
    md_path = os.path.join("website-repo", "_faculty", f"{slug}.md")

    if not os.path.exists(md_path):
        return True # Missing file counts as missing bio

    try:
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
            if "Faculty bio coming soon!" in content or len(content.strip()) < 150:
                return True
    except Exception as e:
        print(f"Error reading {md_path}: {e}")
        
    return False

def sync_faculty_issues(existing_titles):
    registry_path = os.path.join("website-repo", "_data", "faculty-registry.csv")
    if not os.path.exists(registry_path):
        print(f"Faculty registry not found at {registry_path}")
        return

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
                    f"You can find the page [here](https://molevolworkshop.github.io/faculty/{fac_id}/)\n\n"
                    f"**Note:** Nothing needs to be done in the `mole-logistics` repository, as it is used for tracking only. "
                    f"Please make all changes and submit your pull request in the [website repository](https://github.com/molevolworkshop/molevolworkshop.github.io).\n\n"
                    f"Instructions for updating the page can be found [here](https://github.com/molevolworkshop/molevolworkshop.github.io/tree/main/_faculty)"
                )
                
                labels = ["faculty-page", "needs-review"]
                if check_bio_status(fac_id, name):
                    labels.append("missing")

                create_issue(title, body, labels)

def sync_material_issues(existing_titles, target_type, label_prefix, folder_name):
    registry_path = os.path.join("moledata-repo", "_data", "materials-registry.csv")
    if not os.path.exists(registry_path):
        print(f"Materials registry not found at {registry_path}")
        return

    with open(registry_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mat_type = row.get("type", row.get("category", "")).strip().lower()
            if mat_type != target_type:
                continue

            item_id = row.get("item_id", row.get("id", "")).strip()
            title_name = row.get("title", item_id).strip()
            faculty_name = row.get("faculty", row.get("presenter", row.get("author", "Unassigned"))).strip()
            material_location = row.get("material_location", row.get("location", "")).strip()

            title = f"Review & Update {target_type.capitalize()} Materials: {title_name} [{item_id}]"
            if title not in existing_titles:
                labels = [label_prefix, "needs-review"]
                
                formatting_instructions = (
                    f"\n\n**Note:** Nothing needs to be done in the `mole-logistics` repository, as it is used for tracking only. "
                    f"Please make all changes and submit your pull request in the [moledata repository](https://github.com/molevolworkshop/moledata).\n\n"
                    f"For details on how changes should be styled and formatted, please consult the "
                    f"[Contributing Guidelines](https://github.com/molevolworkshop/moledata/blob/main/CONTRIBUTING.md)."
                )

                if not material_location:
                    target_dir = os.path.join("moledata-repo", folder_name, item_id)
                    if not os.path.isdir(target_dir):
                        labels.append("missing")
                    body = (
                        f"Please review and update the onsite {target_type} materials for **{title_name}**.\n\n"
                        f"- **Faculty / Author:** {faculty_name}\n"
                        f"- **Item ID:** `{item_id}`\n"
                        f"- **Material Location:** Onsite (`{folder_name}/{item_id}/`)\n\n"
                        f"Please ensure the directory `{folder_name}/{item_id}/` exists in the `moledata` repository with all required files."
                        f"{formatting_instructions}"
                    )
                else:
                    labels.append("offsite")
                    body = (
                        f"Please review and update the off-site {target_type} materials for **{title_name}**.\n\n"
                        f"- **Faculty / Author:** {faculty_name}\n"
                        f"- **Item ID:** `{item_id}`\n"
                        f"- **Material Location:** `{material_location}`\n\n"
                        f"Please verify that the off-site link and materials are up to date."
                        f"{formatting_instructions}"
                    )

                create_issue(title, body, labels)

def main():
    existing_titles = get_existing_issues()
    sync_faculty_issues(existing_titles)
    sync_material_issues(existing_titles, target_type="lecture", label_prefix="lecture", folder_name="lectures")
    sync_material_issues(existing_titles, target_type="lab", label_prefix="lab", folder_name="labs")

if __name__ == "__main__":
    main()