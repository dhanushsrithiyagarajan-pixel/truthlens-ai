"""
TruthLens AI - Flask API & Database Integration Test Suite
"""

import unittest
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from backend.database import init_db

class TestApiEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        init_db()

    def test_metrics_endpoint(self):
        """Verify that /api/metrics returns valid live data structure."""
        response = self.client.get('/api/metrics')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "success")
        self.assertIn("total_reports", data["data"])
        self.assertIn("verdict_counts", data["data"])
        self.assertIn("category_counts", data["data"])

    def test_verify_claim_submission(self):
        """Verify that /api/verify correctly evaluates and stores a claim."""
        payload = {
            "claim": "RBI issues alert regarding fake PAN-Aadhaar links draining funds.",
            "source_url": "https://rbi-security-notice.top/alert",
            "source_name": "Forward",
            "category": "finance"
        }
        response = self.client.post('/api/verify',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "success")
        self.assertIn("report_id", data)
        self.assertIn("verdict", data["data"])

    def test_source_inspection(self):
        """Verify that /api/source/inspect audits domain anatomy."""
        payload = {"url": "https://who-influenza-cure.click/bulletin"}
        response = self.client.post('/api/source/inspect',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["data"]["tld"], ".click")

    def test_automation_claim_to_checklist(self):
        """Verify that mandatory automation /api/automation/claim-to-checklist creates 10 steps."""
        payload = {
            "claim": "Electricity disconnection SMS asking to call Officer Sharma.",
            "category": "cybersecurity"
        }
        response = self.client.post('/api/automation/claim-to-checklist',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "success")
        self.assertEqual(len(data["data"]["steps"]), 10)
        self.assertIn("checklist_id", data["data"])

    def test_reports_history_and_export(self):
        """Verify reports retrieval and markdown export."""
        response = self.client.get('/api/reports')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreater(data["count"], 0)
        first_id = data["data"][0]["id"]

        # Export test
        export_res = self.client.get(f'/api/export/report/{first_id}?format=markdown')
        self.assertEqual(export_res.status_code, 200)
        self.assertIn(b"TruthLens AI", export_res.data)

if __name__ == '__main__':
    unittest.main()
