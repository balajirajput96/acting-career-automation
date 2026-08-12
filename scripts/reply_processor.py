import os
import sys
from tracker_utils import get_github_repo

def main():
    repo = get_github_repo()
    if not repo:
        print("Error: Could not access GitHub repository.")
        sys.exit(1)

    issue_number = os.getenv("ISSUE_NUMBER")
    comment_body = os.getenv("COMMENT_BODY")

    if not issue_number or not comment_body:
        print("Error: Missing ISSUE_NUMBER or COMMENT_BODY environment variables.")
        sys.exit(1)

    issue = repo.get_issue(int(issue_number))

    if "/sent" in comment_body:
        issue.remove_from_labels("lead-new")
        issue.add_to_labels("lead-sent")
        # Placeholder for Project board movement: New -> Sent
        issue.create_comment("Lead marked as sent. Moving to 'Sent' column on Project board (manual action needed for now).")
        print(f"Issue {issue_number} marked as sent.")
    elif "/rejected" in comment_body:
        issue.remove_from_labels("lead-new", "lead-sent", "follow-up-needed")
        issue.add_to_labels("lead-rejected")
        # Placeholder for Project board movement: any -> Rejected
        issue.create_comment("Lead marked as rejected. Moving to 'Closed-tracking' column on Project board (manual action needed for now).")
        print(f"Issue {issue_number} marked as rejected.")
    elif "/callback" in comment_body:
        issue.remove_from_labels("lead-new", "lead-sent")
        issue.add_to_labels("lead-callback")
        # Placeholder for Project board movement: Sent -> Callback
        issue.create_comment("Lead marked for callback. Moving to 'Follow-up' column on Project board (manual action needed for now).")
        print(f"Issue {issue_number} marked for callback.")
    elif "/followed-up" in comment_body:
        issue.remove_from_labels("follow-up-needed")
        issue.create_comment("Follow-up reminder dismissed.")
        print(f"Issue {issue_number} follow-up reminder dismissed.")

if __name__ == "__main__":
    main()
