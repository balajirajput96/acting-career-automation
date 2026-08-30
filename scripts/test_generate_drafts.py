import unittest
from unittest.mock import patch, MagicMock, mock_open

import importlib
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:
    import scripts.generate_drafts as generate_drafts
    from scripts.generate_drafts import fill_template, load_template, main
except ModuleNotFoundError:
    import generate_drafts
    from generate_drafts import fill_template, load_template, main


class TestGenerateDrafts(unittest.TestCase):
    def test_fill_template(self):
        template = "Hello {{name}}, role: {{role}}, project: {{project}}"
        lead = {"name": "Jane Doe", "role": "Lead Actress", "project": "Indie Film"}

        expected_output = "Hello Jane Doe, role: Lead Actress, project: Indie Film"
        result = fill_template(template, lead)
        self.assertEqual(result, expected_output)

    def test_fill_template_missing_key(self):
        template = "Hello {{name}}, role: {{role}}, source: {{source}}"
        lead = {"name": "John Smith", "role": "Extra"}
        expected_output = "Hello John Smith, role: Extra, source: {{source}}"
        result = fill_template(template, lead)
        self.assertEqual(result, expected_output)

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data="template content")
    def test_load_template_exists(self, mock_open, mock_exists):
        mock_exists.return_value = True
        content = load_template("dummy_template")
        self.assertEqual(content, "template content")

    @patch("os.path.exists")
    @patch("builtins.print")
    def test_load_template_not_exists(self, mock_print, mock_exists):
        mock_exists.return_value = False
        content = load_template("dummy_template")
        self.assertEqual(content, "")
        mock_print.assert_called_once_with(
            "Warning: Template dummy_template.md not found."
        )

    @patch(f"{generate_drafts.__name__}.get_github_repo")
    @patch(f"{generate_drafts.__name__}.get_csv_data")
    @patch(f"{generate_drafts.__name__}.load_template")
    def test_main(self, mock_load_template, mock_get_csv_data, mock_get_github_repo):
        mock_repo = MagicMock()
        mock_get_github_repo.return_value = mock_repo

        mock_issue1 = MagicMock()
        mock_issue1.body = "Some body"
        mock_issue1.title = "Awesome Project - Lead Role"
        mock_issue1.number = 1

        mock_issue2 = MagicMock()
        mock_issue2.body = "### Personalized Drafts"
        mock_issue2.title = "Another Project - Lead Role"
        mock_issue2.number = 2

        mock_issue3 = MagicMock()
        mock_issue3.body = "No match"
        mock_issue3.title = "Unknown Project - Lead Role"
        mock_issue3.number = 3

        mock_repo.get_issues.return_value = [mock_issue1, mock_issue2, mock_issue3]

        mock_get_csv_data.return_value = [
            {
                "id": "1",
                "project": "Awesome Project",
                "role": "Lead Role",
                "name": "Actor1",
            },
            {
                "id": "2",
                "project": "Another Project",
                "role": "Lead Role",
                "name": "Actor2",
            },
        ]

        mock_load_template.side_effect = ["Email: {{name}}", "DM: {{name}}"]

        main()

        mock_issue1.edit.assert_called_once()
        args, kwargs = mock_issue1.edit.call_args
        self.assertIn("Email: Actor1", kwargs["body"])
        self.assertIn("DM: Actor1", kwargs["body"])

        mock_issue2.edit.assert_not_called()
        mock_issue3.edit.assert_not_called()

    @patch(f"{generate_drafts.__name__}.get_github_repo")
    def test_main_no_repo(self, mock_get_github_repo):
        mock_get_github_repo.return_value = None
        main()  # Should return without doing anything


import unittest
from unittest.mock import patch, MagicMock


class TestGenerateDraftsMain(unittest.TestCase):
    @patch(f"{generate_drafts.__name__}.get_github_repo")
    @patch(f"{generate_drafts.__name__}.get_csv_data")
    @patch(f"{generate_drafts.__name__}.load_template")
    def test_main_missing_template(
        self, mock_load_template, mock_get_csv_data, mock_get_github_repo
    ):
        mock_repo = MagicMock()
        mock_get_github_repo.return_value = mock_repo

        mock_issue = MagicMock()
        mock_issue.body = "Some body"
        mock_issue.title = "Awesome Project - Lead Role"
        mock_issue.number = 1

        mock_repo.get_issues.return_value = [mock_issue]

        mock_get_csv_data.return_value = [
            {
                "id": "1",
                "project": "Awesome Project",
                "role": "Lead Role",
                "name": "Actor1",
            },
        ]

        mock_load_template.side_effect = ["", "DM: {{name}}"]  # missing email

        generate_drafts.main()

        mock_issue.edit.assert_called_once()
        args, kwargs = mock_issue.edit.call_args
        self.assertIn("Warning: email_template.md not found.", kwargs["body"])
        self.assertIn("DM: Actor1", kwargs["body"])

    @patch(f"{generate_drafts.__name__}.get_github_repo")
    @patch(f"{generate_drafts.__name__}.get_csv_data")
    @patch(f"{generate_drafts.__name__}.load_template")
    def test_main_missing_template2(
        self, mock_load_template, mock_get_csv_data, mock_get_github_repo
    ):
        mock_repo = MagicMock()
        mock_get_github_repo.return_value = mock_repo

        mock_issue = MagicMock()
        mock_issue.body = "Some body"
        mock_issue.title = "Awesome Project - Lead Role"
        mock_issue.number = 1

        mock_repo.get_issues.return_value = [mock_issue]

        mock_get_csv_data.return_value = [
            {
                "id": "1",
                "project": "Awesome Project",
                "role": "Lead Role",
                "name": "Actor1",
            },
        ]

        mock_load_template.side_effect = ["Email: {{name}}", ""]  # missing dm

        generate_drafts.main()

        mock_issue.edit.assert_called_once()
        args, kwargs = mock_issue.edit.call_args
        self.assertIn("Warning: dm_template.md not found.", kwargs["body"])
        self.assertIn("Email: Actor1", kwargs["body"])


if __name__ == "__main__":
    unittest.main()
