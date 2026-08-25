import csv
import os

def get_csv_data(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def update_csv_status(file_path, lead_id, new_status):
    rows = []
    updated = False
    fieldnames = []
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            if row['id'] == str(lead_id):
                row['status'] = new_status
                updated = True
            rows.append(row)
    
    if updated:
        with open(file_path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    return updated

def get_github_repo():
    token = os.getenv('GITHUB_TOKEN')
    repo_name = os.getenv('GITHUB_REPOSITORY')
    if not token or not repo_name:
        return None
    # Keep optional GitHub access out of pure local helpers and test collection.
    # The dependency remains declared in requirements.txt for runtime use.
    from github import Github
    g = Github(token)
    return g.get_repo(repo_name)
