import unittest
import os
import csv
import tempfile

try:
    from tracker_utils import get_csv_data, update_csv_status
except ModuleNotFoundError as exc:
    if exc.name != "tracker_utils":
        raise
    from scripts.tracker_utils import get_csv_data, update_csv_status


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


if __name__ == "__main__":
    unittest.main()
