import unittest
from parse_leads import check_scam

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

if __name__ == '__main__':
    unittest.main()
