import csv
import sys
import os

EXPECTED_HEADER = [
    "id",
    "date_found",
    "source",
    "project",
    "role",
    "contact_type",
    "contact",
    "status",
    "notes",
]


def validate_csv_header(file_path):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)

        if header is None:
            print(f"Error: {file_path} is empty.")
            sys.exit(1)

        if header != EXPECTED_HEADER:
            print(f"Error: {file_path} has an invalid header.")
            print(f"Expected: {EXPECTED_HEADER}")
            print(f"Found:    {header}")
            sys.exit(1)

    print(f"Success: {file_path} header is valid.")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(__file__))
    validate_csv_header(os.path.join(base_dir, "data", "casting_leads.csv"))
    validate_csv_header(os.path.join(base_dir, "data", "casting_leads.sample.csv"))
