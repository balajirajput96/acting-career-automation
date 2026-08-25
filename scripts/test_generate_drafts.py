import unittest

try:
    from generate_drafts import fill_template
except ModuleNotFoundError as exc:
    if exc.name != "generate_drafts":
        raise
    from scripts.generate_drafts import fill_template

class TestGenerateDrafts(unittest.TestCase):
    def test_fill_template(self):
        template = "Hello {{name}}, role: {{role}}, project: {{project}}"
        lead = {
            "name": "Jane Doe",
            "role": "Lead Actress",
            "project": "Indie Film"
        }

        expected_output = "Hello Jane Doe, role: Lead Actress, project: Indie Film"
        result = fill_template(template, lead)
        self.assertEqual(result, expected_output)

    def test_fill_template_missing_key(self):
        template = "Hello {{name}}, role: {{role}}, source: {{source}}"
        lead = {
            "name": "John Smith",
            "role": "Extra"
        }
        # source is missing in the lead dictionary
        # the current implementation of fill_template iterates over lead keys,
        # so missing keys in the lead dict will leave the template placeholder intact.
        expected_output = "Hello John Smith, role: Extra, source: {{source}}"
        result = fill_template(template, lead)
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()
