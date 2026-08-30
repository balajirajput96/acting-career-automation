import unittest
import os
import tempfile
import sys
from io import StringIO

try:
    from check_csv_header import validate_csv_header, EXPECTED_HEADER
except ModuleNotFoundError as exc:
    if exc.name != "check_csv_header":
        raise
    from scripts.check_csv_header import validate_csv_header, EXPECTED_HEADER


class TestCheckCSVHeader(unittest.TestCase):
    def setUp(self):
        # Create temporary files
        self.fd_valid, self.path_valid = tempfile.mkstemp(suffix=".csv")
        self.fd_invalid, self.path_invalid = tempfile.mkstemp(suffix=".csv")
        self.fd_empty, self.path_empty = tempfile.mkstemp(suffix=".csv")

        # Write valid header
        with os.fdopen(self.fd_valid, "w", encoding="utf-8") as f:
            f.write(",".join(EXPECTED_HEADER) + "\n")
            f.write(
                "1,2026-07-01,Backstage,The Great Gatsby,Jay Gatsby,Email,casting@greatgatsby.com,SENT,Sent reel.\n"
            )

        # Write invalid header
        with os.fdopen(self.fd_invalid, "w", encoding="utf-8") as f:
            f.write(
                "id,date_found,source,wrong_column,role,contact_type,contact,status,notes\n"
            )

        # Leave the empty one empty
        os.close(self.fd_empty)

    def tearDown(self):
        for path in [self.path_valid, self.path_invalid, self.path_empty]:
            if os.path.exists(path):
                os.remove(path)

    def test_validate_csv_header_valid(self):
        # It should just print success and return without exiting
        try:
            validate_csv_header(self.path_valid)
        except SystemExit:
            self.fail("validate_csv_header exited unexpectedly for a valid file.")

    def test_validate_csv_header_invalid(self):
        with self.assertRaises(SystemExit) as cm:
            validate_csv_header(self.path_invalid)
        self.assertEqual(cm.exception.code, 1)

    def test_validate_csv_header_empty(self):
        with self.assertRaises(SystemExit) as cm:
            validate_csv_header(self.path_empty)
        self.assertEqual(cm.exception.code, 1)

    def test_validate_csv_header_non_existent(self):
        with self.assertRaises(SystemExit) as cm:
            validate_csv_header("non_existent_file.csv")
        self.assertEqual(cm.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
