import csv
import json
import subprocess

def sync_csv_to_sheets(csv_path, spreadsheet_id):
    values = []
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            values.append(row)
    
    # Prepare the JSON for gws
    data = {
        "range": "Sheet1!A1",
        "values": values
    }
    
    with open('update_values.json', 'w') as f:
        json.dump(data, f)
    
    # Run gws command
    cmd = [
        'gws', 'sheets', 'spreadsheets', 'values', 'update',
        '--params', json.dumps({"spreadsheetId": spreadsheet_id, "range": "Sheet1!A1", "valueInputOption": "RAW"}),
        '--json', json.dumps(data)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print("Successfully synced CSV to Google Sheets.")
    else:
        print(f"Error syncing to Google Sheets: {result.stderr}")

if __name__ == "__main__":
    SPREADSHEET_ID = "1nlejtnIjU4paJUUJtR37kYuCM8CQz5YD5tPcmytR46s"
    sync_csv_to_sheets('data/casting_leads.csv', SPREADSHEET_ID)
