import os
import sys
import unittest
from unittest.mock import patch, MagicMock

import reply_processor


class TestReplyProcessor(unittest.TestCase):
    @patch("reply_processor.get_github_repo")
    @patch("os.getenv")
    def test_missing_repo(self, mock_getenv, mock_get_github_repo):
        mock_get_github_repo.return_value = None
        with self.assertRaises(SystemExit) as cm:
            reply_processor.main()
        self.assertEqual(cm.exception.code, 1)

    @patch("reply_processor.get_github_repo")
    @patch("os.getenv")
    def test_missing_env_vars(self, mock_getenv, mock_get_github_repo):
        mock_get_github_repo.return_value = MagicMock()
        mock_getenv.side_effect = lambda k: None
        with self.assertRaises(SystemExit) as cm:
            reply_processor.main()
        self.assertEqual(cm.exception.code, 1)

    @patch("reply_processor.get_github_repo")
    @patch("os.getenv")
    def test_sent_command(self, mock_getenv, mock_get_github_repo):
        mock_repo = MagicMock()
        mock_get_github_repo.return_value = mock_repo

        mock_issue = MagicMock()
        mock_repo.get_issue.return_value = mock_issue

        def mock_env(key):
            if key == "ISSUE_NUMBER":
                return "1"
            if key == "COMMENT_BODY":
                return "/sent"
            return None

        mock_getenv.side_effect = mock_env

        reply_processor.main()

        mock_repo.get_issue.assert_called_once_with(1)
        mock_issue.remove_from_labels.assert_called_once_with("lead-new")
        mock_issue.add_to_labels.assert_called_once_with("lead-sent")
        mock_issue.create_comment.assert_called_once()

    @patch("reply_processor.get_github_repo")
    @patch("os.getenv")
    def test_rejected_command(self, mock_getenv, mock_get_github_repo):
        mock_repo = MagicMock()
        mock_get_github_repo.return_value = mock_repo

        mock_issue = MagicMock()
        mock_repo.get_issue.return_value = mock_issue

        def mock_env(key):
            if key == "ISSUE_NUMBER":
                return "1"
            if key == "COMMENT_BODY":
                return "/rejected"
            return None

        mock_getenv.side_effect = mock_env

        reply_processor.main()

        mock_issue.remove_from_labels.assert_called_once_with(
            "lead-new", "lead-sent", "follow-up-needed"
        )
        mock_issue.add_to_labels.assert_called_once_with("lead-rejected")

    @patch("reply_processor.get_github_repo")
    @patch("os.getenv")
    def test_callback_command(self, mock_getenv, mock_get_github_repo):
        mock_repo = MagicMock()
        mock_get_github_repo.return_value = mock_repo

        mock_issue = MagicMock()
        mock_repo.get_issue.return_value = mock_issue

        def mock_env(key):
            if key == "ISSUE_NUMBER":
                return "1"
            if key == "COMMENT_BODY":
                return "/callback"
            return None

        mock_getenv.side_effect = mock_env

        reply_processor.main()

        mock_issue.remove_from_labels.assert_called_once_with("lead-new", "lead-sent")
        mock_issue.add_to_labels.assert_called_once_with("lead-callback")

    @patch("reply_processor.get_github_repo")
    @patch("os.getenv")
    def test_followed_up_command(self, mock_getenv, mock_get_github_repo):
        mock_repo = MagicMock()
        mock_get_github_repo.return_value = mock_repo

        mock_issue = MagicMock()
        mock_repo.get_issue.return_value = mock_issue

        def mock_env(key):
            if key == "ISSUE_NUMBER":
                return "1"
            if key == "COMMENT_BODY":
                return "/followed-up"
            return None

        mock_getenv.side_effect = mock_env

        reply_processor.main()

        mock_issue.remove_from_labels.assert_called_once_with("follow-up-needed")


if __name__ == "__main__":
    unittest.main()
