import os
import sys
from datetime import datetime, timedelta
from tracker_utils import get_github_repo

def main():
    repo = get_github_repo()
    if not repo:
        print("Error: Could not access GitHub repository.")
        sys.exit(1)

    # Get issues labeled 'lead-sent' that are older than 7 days
    seven_days_ago = datetime.now() - timedelta(days=7)
    
    issues = repo.get_issues(state=\'open\', labels=[\'lead-sent\'])
    
    for issue in issues:
        # Check if the issue was last updated more than 7 days ago
        # This is a simplification; ideally, we'd track when it was *sent*
        # For now, we'll use issue creation date as a proxy for 'sent' if no other info
        if issue.created_at < seven_days_ago:
            if \'follow-up-needed\' not in [l.name for l in issue.labels]:
                issue.add_to_labels(\'follow-up-needed\')
                issue.create_comment("It's been 7 days since this lead was marked as 'sent'. Consider a follow-up. Use `/followed-up` to mark as followed up.")
                print(f"Added follow-up reminder to issue {issue.number}")

if __name__ == "__main__":
    main()
