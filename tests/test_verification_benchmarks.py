"""
TruthLens AI - Benchmark Test Suite: 10 Core Capstone Test Scenarios
Evaluates verification accuracy, factual decomposition, verdict calibration, and uncertainty handling.
"""

import unittest
import os
import sys

# Ensure root directory is on python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.verifier import analyze_claim
from backend.source_checker import inspect_url
from backend.automation import generate_claim_checklist

class TestVerificationBenchmarks(unittest.TestCase):
    """
    Test suite executing the 10 mandated capstone benchmark test cases.
    """

    def test_case_01_genuine_claim_reliable_source(self):
        """Case 1: A genuine claim supported by a reliable source."""
        claim = "ISRO successfully launches indigenous quantum key distribution satellite demonstrator for defense communications."
        url = "https://isro.gov.in/press-release-quantum-comms.html"
        source = "ISRO & PTI"
        cat = "cybersecurity"

        result = analyze_claim(claim, source_url=url, source_name=source, category=cat)

        self.assertEqual(result["verdict"], "Supported by available evidence")
        self.assertGreaterEqual(result["confidence"], 80)
        self.assertTrue(len(result["factual_statements"]) > 0)
        self.assertIn("isro.gov.in", result["evidence_summary"])

    def test_case_02_misleading_claim_missing_context(self):
        """Case 2: A misleading claim missing context."""
        claim = "Viral photo shows rare double rainbow over the Taj Mahal during solar eclipse with violet auroral clouds."
        url = "https://instagram.com/p/viral-taj-eclipse"
        source = "Social Media Aggregator"
        cat = "other"

        result = analyze_claim(claim, source_url=url, source_name=source, category=cat)

        self.assertIn(result["verdict"], ["Misleading or missing context", "Contradicted by available evidence"])
        self.assertTrue(len(result["corroboration_needs"]) > 0)

    def test_case_03_unsupported_claim(self):
        """Case 3: An unsupported claim (no primary documentation)."""
        claim = "Ancient manuscript discovered in cellar reveals secret underground tunnel connecting Mumbai to London."
        url = "https://random-blog.net/secret-tunnel"
        source = "Conspiracy Forum"
        cat = "other"

        result = analyze_claim(claim, source_url=url, source_name=source, category=cat)

        self.assertEqual(result["verdict"], "Unverified — more evidence required")
        self.assertTrue("Insufficient primary documentation" in result["evidence_summary"] or "corroboration" in result["evidence_summary"].lower())

    def test_case_04_suspicious_phishing_message(self):
        """Case 4: A suspicious phishing message."""
        claim = "Urgent warning from RBI: Update your KYC by midnight on link or your bank account will be permanently blocked."
        url = "http://rbi-kyc-update-portal.top/login"
        source = "SMS Alert"
        cat = "finance"

        result = analyze_claim(claim, source_url=url, source_name=source, category=cat)

        self.assertEqual(result["verdict"], "Suspicious indicators detected")
        self.assertGreaterEqual(result["confidence"], 85)
        self.assertTrue(any("urgency" in ind.lower() or "tld" in ind.lower() or "protocol" in ind.lower() for ind in result["suspicious_indicators"]))

    def test_case_05_fake_giveaway_scam(self):
        """Case 5: A fake giveaway / lottery scam."""
        claim = "Government distributing free laptop and ₹5,000 allowance to all students. Click here to claim your giveaway bonus."
        url = "https://free-student-bonus-scheme.xyz/apply"
        source = "WhatsApp Forward"
        cat = "cybersecurity"

        result = analyze_claim(claim, source_url=url, source_name=source, category=cat)

        self.assertEqual(result["verdict"], "Suspicious indicators detected")
        self.assertTrue(any("financial" in ind.lower() or "tld" in ind.lower() or "giveaway" in ind.lower() for ind in result["suspicious_indicators"]))

    def test_case_06_manipulated_synthetic_media(self):
        """Case 6: A manipulated or synthetic example with known provenance."""
        claim = "Leaked video shows prominent tech CEO endorsing guaranteed 500% weekly return cryptocurrency automated trading bot."
        url = "https://telegram.org/channel/crypto-wealth-bot-leak"
        source = "Telegram Channel"
        cat = "finance"

        result = analyze_claim(claim, source_url=url, source_name=source, category=cat)

        self.assertEqual(result["verdict"], "Suspicious indicators detected")
        self.assertGreaterEqual(result["confidence"], 85)

    def test_case_07_authentic_image_incorrect_caption(self):
        """Case 7: An authentic image with an incorrect caption."""
        claim = "Photo shows massive crowds protesting new tax laws yesterday in Delhi."
        url = "https://twitter.com/user/status/12345678"
        source = "Social Media Tweet"
        cat = "politics"

        result = analyze_claim(claim, source_url=url, source_name=source, category=cat)

        # Requires independent corroboration and reverse image verification
        self.assertIn(result["verdict"], ["Unverified — more evidence required", "Misleading or missing context"])
        self.assertTrue(any("fact-checking" in rec.lower() or "reverse" in rec.lower() for rec in result["recommendations"]))

    def test_case_08_recycled_image_recent_event(self):
        """Case 8: A recycled image presented as a recent event."""
        claim = "Breaking: Satellite photo proves alien mothership hovered over Himalayas this morning."
        url = "https://viral-ufo-news.click/mothership"
        source = "Viral Blog"
        cat = "other"

        result = analyze_claim(claim, source_url=url, source_name=source, category=cat)

        self.assertIn(result["verdict"], ["Suspicious indicators detected", "Misleading or missing context", "Unverified — more evidence required"])

    def test_case_09_impersonation_scam_example(self):
        """Case 9: An impersonation-style scam example."""
        claim = "SBI Bank Alert: Your electricity bill is pending, contact Officer Sharma on personal WhatsApp or account suspended immediately."
        url = "https://sbi-bill-clearance.work/pay"
        source = "Unsolicited SMS"
        cat = "finance"

        result = analyze_claim(claim, source_url=url, source_name=source, category=cat)

        self.assertEqual(result["verdict"], "Suspicious indicators detected")
        self.assertTrue(len(result["suspicious_indicators"]) > 0)

    def test_case_10_ambiguous_claim_requiring_evidence(self):
        """Case 10: An ambiguous claim requiring additional evidence."""
        claim = "Local startup in Bengaluru develops new battery alloy claiming to double electric vehicle range under testing."
        url = "https://tech-innovators-india.org/battery-announcement"
        source = "Industry Tech Blog"
        cat = "news"

        result = analyze_claim(claim, source_url=url, source_name=source, category=cat)

        self.assertEqual(result["verdict"], "Unverified — more evidence required")
        self.assertTrue(len(result["corroboration_needs"]) > 0)
        self.assertIn("TruthLens AI evaluates linguistic indicators", result["limitations"])

if __name__ == '__main__':
    unittest.main()
