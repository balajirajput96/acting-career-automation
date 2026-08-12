import os
import sys
from tracker_utils import get_csv_data, get_github_repo

def check_scam(row):
    warnings = []
    contact = row.get('contact', '').lower()
    notes = row.get('notes', '').lower()
    project = row.get('project', '').lower()

    if 'fee' in notes or 'payment' in notes or 'charge' in notes:
        warnings.append("⚠️ Potential Fee Scam detected in notes.")
    
    scam_domains = ['@gmail.com', '@yahoo.com', '@hotmail.com', '@outlook.com']
    if any(domain in contact for domain in scam_domains):
        warnings.append("⚠️ Free email domain used (Gmail/Yahoo/etc.). Verify authenticity.")

    if not project or project == 'unknown' or len(project) < 3:
        warnings.append("⚠️ Missing or vague project name.")

    return warnings

def main():
    csv_path = 'data/casting_leads.csv'
    leads = get_csv_data(csv_path)
    repo = get_github_repo()
    
    if not repo:
        print("Error: Could not access GitHub repository.")
        sys.exit(1)

    new_leads = [l for l in leads if l['status'].upper() == 'NEW']
    
    for lead in new_leads:
        warnings = check_scam(lead)
        warning_text = "\n".join(warnings) if warnings else "No obvious red flags detected."
        
        title = f"[NEW LEAD] {lead['project']} - {lead['role']}"
        body = f"""
### Lead Details
- **Project:** {lead['project']}
- **Role:** {lead['role']}
- **Source:** {lead['source']}
- **Contact:** {lead['contact']} ({lead['contact_type']})
- **Date Found:** {lead['date_found']}

### Scam Check Results
{warning_text}

### Instructions
Use `/sent` to mark as sent, `/rejected` if not interested, or `/callback` for follow-ups.
        """
        
        issue = repo.create_issue(title=title, body=body)
        if warnings:
            issue.add_to_labels("warning")
        issue.add_to_labels("lead-new")
        print(f"Created issue for lead {lead['id']}")

if __name__ == "__main__":
    main()
