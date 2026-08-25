import os
from tracker_utils import get_csv_data, get_github_repo

def load_template(name):
    path = f'templates/{name}.md'
    if os.path.exists(path):
        with open(path, 'r') as f:
            return f.read()
    print(f"Warning: Template {name}.md not found.")
    return ""

def fill_template(template, lead):
    for key, value in lead.items():
        template = template.replace(f"{{{{{key}}}}}", value)
    return template

def main():
    csv_path = 'data/casting_leads.csv'
    leads = get_csv_data(csv_path)
    repo = get_github_repo()
    
    if not repo:
        return

    # Find open issues for new leads
    issues = repo.get_issues(state='open', labels=['lead-new'])
    
    email_tmpl = load_template('email_template')
    dm_tmpl = load_template('dm_template')

    for issue in issues:
        # Extract lead ID from title or body if needed, or match by project/role
        # For simplicity, we'll just append drafts to the issue if not already present
        if "### Personalized Drafts" in issue.body:
            continue
            
        # Finding the lead in CSV based on issue title (basic matching)
        matching_lead = None
        for lead in leads:
            if lead['project'] in issue.title and lead['role'] in issue.title:
                matching_lead = lead
                break
        
        if matching_lead:
            email_draft = fill_template(email_tmpl, matching_lead) if email_tmpl else "Warning: email_template.md not found."
            dm_draft = fill_template(dm_tmpl, matching_lead) if dm_tmpl else "Warning: dm_template.md not found."
            
            draft_body = f"""
---
### Personalized Drafts
#### Email Version
```markdown
{email_draft}
```

#### DM Version (IG/WhatsApp)
```markdown
{dm_draft}
```
            """
            issue.edit(body=issue.body + draft_body)
            print(f"Added drafts to issue {issue.number}")

if __name__ == "__main__":
    main()
