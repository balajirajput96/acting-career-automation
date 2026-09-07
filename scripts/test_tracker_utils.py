from unittest.mock import patch, MagicMock
import unittest
import os
import csv
import tempfile
import sys

# Ensure scripts dir is in path for all imports in tests
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from scripts.tracker_utils import get_csv_data, update_csv_status, get_github_repo
except ModuleNotFoundError:
    from tracker_utils import get_csv_data, update_csv_status, get_github_repo


class TestTrackerUtils(unittest.TestCase):
    def setUp(self):
        # Create a temporary file
        self.fd, self.temp_path = tempfile.mkstemp(suffix=".csv")

        # Write some sample data to the temp file
        with os.fdopen(self.fd, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "name", "status"])
            writer.writeheader()
            writer.writerow({"id": "1", "name": "John Doe", "status": "NEW"})
            writer.writerow({"id": "2", "name": "Jane Doe", "status": "SENT"})

    def tearDown(self):
        # Remove the temporary file
        if os.path.exists(self.temp_path):
            os.remove(self.temp_path)

    def test_get_csv_data_existing(self):
        data = get_csv_data(self.temp_path)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["id"], "1")
        self.assertEqual(data[0]["name"], "John Doe")
        self.assertEqual(data[0]["status"], "NEW")

    def test_get_csv_data_missing(self):
        data = get_csv_data("non_existent_file.csv")
        self.assertEqual(data, [])

    def test_update_csv_status_success(self):
        updated = update_csv_status(self.temp_path, "1", "REJECTED")
        self.assertTrue(updated)

        # Verify the file was actually updated
        data = get_csv_data(self.temp_path)
        self.assertEqual(data[0]["id"], "1")
        self.assertEqual(data[0]["status"], "REJECTED")

    def test_update_csv_status_not_found(self):
        updated = update_csv_status(self.temp_path, "999", "REJECTED")
        self.assertFalse(updated)

    @patch("os.getenv")
    def test_get_github_repo_missing_vars(self, mock_getenv):
        # Test when variables are missing
        mock_getenv.return_value = None
        repo = get_github_repo()
        self.assertIsNone(repo)

    @patch("os.getenv")
    def test_get_github_repo_success(self, mock_getenv):
        # Mock environment variables
        def mock_env(key):
            if key == "GITHUB_TOKEN":
                return "fake_token"
            if key == "GITHUB_REPOSITORY":
                return "fake/repo"
            return None

        mock_getenv.side_effect = mock_env

        try:
            import scripts.tracker_utils as tu
        except ModuleNotFoundError:
            import tracker_utils as tu

        # the problem is tracker_utils does not import Github until inside the function
        # We need to mock sys.modules to mock the github module
        mock_github_module = MagicMock()
        mock_github_client = MagicMock()
        mock_github_module.Github = MagicMock(return_value=mock_github_client)
        mock_repo = MagicMock()
        mock_github_client.get_repo.return_value = mock_repo

        with patch.dict("sys.modules", {"github": mock_github_module}):
            repo = tu.get_github_repo()

            mock_github_module.Github.assert_called_once_with("fake_token")
            mock_github_client.get_repo.assert_called_once_with("fake/repo")
            self.assertEqual(repo, mock_repo)


if __name__ == "__main__":
    unittest.main()
