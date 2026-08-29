import unittest
from unittest.mock import patch, MagicMock, call

try:
    import parse_leads
    from parse_leads import check_scam, main
except ModuleNotFoundError:
    import scripts.parse_leads as parse_leads
    from scripts.parse_leads import check_scam, main

class TestParseLeads(unittest.TestCase):
    def test_check_scam_no_flags(self):
        lead = {
            'contact': 'casting@legitstudio.com',
            'notes': 'Looking for actors.',
            'project': 'Big Feature Film'
        }
        warnings = check_scam(lead)
        self.assertEqual(len(warnings), 0)

    def test_check_scam_fee(self):
        lead = {
            'contact': 'casting@legitstudio.com',
            'notes': 'There is a small fee for auditioning.',
            'project': 'Big Feature Film'
        }
        warnings = check_scam(lead)
        self.assertEqual(len(warnings), 1)
        self.assertIn("Fee Scam", warnings[0])

    def test_check_scam_free_email(self):
        lead = {
            'contact': 'director123@gmail.com',
            'notes': 'Looking for actors.',
            'project': 'Big Feature Film'
        }
        warnings = check_scam(lead)
        self.assertEqual(len(warnings), 1)
        self.assertIn("Free email domain", warnings[0])

    def test_check_scam_vague_project(self):
        lead = {
            'contact': 'casting@legitstudio.com',
            'notes': 'Looking for actors.',
            'project': 'Ad'
        }
        warnings = check_scam(lead)
        self.assertEqual(len(warnings), 1)
        self.assertIn("Missing or vague project name", warnings[0])

    def test_check_scam_multiple_flags(self):
        lead = {
            'contact': 'scammer@yahoo.com',
            'notes': 'Payment required before audition.',
            'project': ''
        }
        warnings = check_scam(lead)
        self.assertEqual(len(warnings), 3)

    def test_check_scam_missing_contact(self):
        lead = {
            'contact': '',
            'notes': 'Looking for actors.',
            'project': 'Big Feature Film'
        }
        warnings = check_scam(lead)
        self.assertEqual(len(warnings), 1)
        self.assertIn("Missing contact information", warnings[0])

    @patch(f"{parse_leads.__name__}.get_github_repo")
    @patch(f"{parse_leads.__name__}.get_csv_data")
    def test_main(self, mock_get_csv_data, mock_get_github_repo):
        mock_repo = MagicMock()
        mock_get_github_repo.return_value = mock_repo

        mock_get_csv_data.return_value = [
            {'id': '1', 'project': 'Awesome Project', 'role': 'Lead', 'status': 'NEW', 'source': 'Web', 'contact': 'a@b.com', 'contact_type': 'Email', 'date_found': '2023-01-01', 'notes': ''},
            {'id': '2', 'project': 'Scam Project', 'role': 'Extra', 'status': 'NEW', 'source': 'Web', 'contact': 'scammer@gmail.com', 'contact_type': 'Email', 'date_found': '2023-01-01', 'notes': 'Fee required'},
            {'id': '3', 'project': 'Old Project', 'role': 'Lead', 'status': 'SENT', 'source': 'Web', 'contact': 'c@d.com', 'contact_type': 'Email', 'date_found': '2023-01-01', 'notes': ''},
        ]

        mock_issue1 = MagicMock()
        mock_issue2 = MagicMock()
        mock_repo.create_issue.side_effect = [mock_issue1, mock_issue2]

        main()

        self.assertEqual(mock_repo.create_issue.call_count, 2)

        mock_issue1.add_to_labels.assert_called_with('lead-new')
        self.assertNotIn(call('warning'), mock_issue1.add_to_labels.call_args_list)

        mock_issue2.add_to_labels.assert_any_call('warning')
        mock_issue2.add_to_labels.assert_any_call('lead-new')

    @patch(f"{parse_leads.__name__}.get_github_repo")
    def test_main_no_repo(self, mock_get_github_repo):
        mock_get_github_repo.return_value = None
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)

if __name__ == '__main__':
    unittest.main()
