import sys
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

import follow_up_tracker


class TestFollowUpTracker(unittest.TestCase):
    @patch("follow_up_tracker.get_github_repo")
    def test_missing_repo(self, mock_get_github_repo):
        mock_get_github_repo.return_value = None
        with self.assertRaises(SystemExit) as cm:
            follow_up_tracker.main()
        self.assertEqual(cm.exception.code, 1)

    @patch("follow_up_tracker.get_github_repo")
    @patch("follow_up_tracker.datetime")
    def test_follow_up_needed(self, mock_datetime, mock_get_github_repo):
        # Setup mock time
        fixed_now = datetime(2023, 1, 10)
        mock_datetime.now.return_value = fixed_now
        mock_datetime.side_effect = lambda *args, **kw: datetime(
            *args, **kw
        )  # Make other datetime calls work

        mock_repo = MagicMock()
        mock_get_github_repo.return_value = mock_repo

        mock_issue_old = MagicMock()
        mock_issue_old.created_at = datetime(2023, 1, 1)  # Older than 7 days
        mock_issue_old.labels = [MagicMock(name="lead-sent")]
        mock_issue_old.labels[0].name = "lead-sent"
        mock_issue_old.number = 1

        mock_issue_new = MagicMock()
        mock_issue_new.created_at = datetime(2023, 1, 5)  # Newer than 7 days
        mock_issue_new.labels = [MagicMock(name="lead-sent")]
        mock_issue_new.labels[0].name = "lead-sent"
        mock_issue_new.number = 2

        mock_issue_already_followed = MagicMock()
        mock_issue_already_followed.created_at = datetime(
            2023, 1, 1
        )  # Older than 7 days

        label1 = MagicMock(name="lead-sent")
        label1.name = "lead-sent"
        label2 = MagicMock(name="follow-up-needed")
        label2.name = "follow-up-needed"

        mock_issue_already_followed.labels = [label1, label2]
        mock_issue_already_followed.number = 3

        mock_repo.get_issues.return_value = [
            mock_issue_old,
            mock_issue_new,
            mock_issue_already_followed,
        ]

        follow_up_tracker.main()

        mock_repo.get_issues.assert_called_once_with(state="open", labels=["lead-sent"])

        mock_issue_old.add_to_labels.assert_called_once_with("follow-up-needed")
        mock_issue_old.create_comment.assert_called_once()

        mock_issue_new.add_to_labels.assert_not_called()
        mock_issue_already_followed.add_to_labels.assert_not_called()


if __name__ == "__main__":
    unittest.main()
