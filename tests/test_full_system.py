"""
TruthLens AI - Comprehensive Module Functionality Validation
Tests every single required module end-to-end against the live backend.
"""

import sys
import os
import json
import io
from PIL import Image

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from backend.database import init_db

def run_checks():
    client = app.test_client()
    init_db()

    print("--- 1. Testing Index & Dashboard HTML ---")
    r = client.get('/')
    assert r.status_code == 200, f"Index failed: {r.status_code}"
    assert b"TruthLens AI" in r.data
    print("PASS: Index HTML rendered successfully (200 OK)")

    print("--- 2. Testing Dashboard Metrics API ---")
    r = client.get('/api/metrics')
    assert r.status_code == 200
    data = json.loads(r.data)["data"]
    assert "total_reports" in data
    assert "verdict_counts" in data
    assert "category_counts" in data
    assert data["total_reports"] >= 5
    print(f"PASS: Metrics returned live data (Total reports: {data['total_reports']}, Avg confidence: {data['avg_confidence']}%)")

    print("--- 3. Testing Claim Verification Pipeline ---")
    claim_payload = {
        "claim": "Urgent alert: Electricity to be disconnected tonight at 9:30 PM due to unpaid bill, contact 9876543210 or install app.",
        "source_url": "http://power-bill-payment.top/pay",
        "source_name": "SMS Message",
        "category": "cybersecurity",
        "context": "Received unsolicited SMS"
    }
    r = client.post('/api/verify', data=json.dumps(claim_payload), content_type='application/json')
    assert r.status_code == 200
    res_data = json.loads(r.data)
    assert res_data["status"] == "success"
    report = res_data["data"]
    assert report["verdict"] == "Suspicious indicators detected"
    assert len(report["suspicious_indicators"]) > 0
    print(f"PASS: Claim verified. Verdict: '{report['verdict']}', Confidence: {report['confidence']}%")

    print("--- 4. Testing Source Credibility Explorer ---")
    source_payload = {"url": "https://rbi-notice-alert.top/pan-link-warning"}
    r = client.post('/api/source/inspect', data=json.dumps(source_payload), content_type='application/json')
    assert r.status_code == 200
    s_data = json.loads(r.data)["data"]
    assert s_data["tld"] == ".top"
    assert len(s_data["caution_indicators"]) > 0
    print(f"PASS: Source inspected. Domain: '{s_data['domain']}', Risk Score: {s_data['risk_score']}/100, Tier: '{s_data['credibility_tier']}'")

    print("--- 5. Testing Deepfake Lab & Forensics (EXIF + ELA) ---")
    # Create an in-memory test image
    img = Image.new('RGB', (200, 200), color=(73, 109, 137))
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    buf.seek(0)

    data = {
        'image': (buf, 'test_sample.jpg'),
        'visual_checks': json.dumps({'ear_asymmetry': True, 'pupil_reflection_mismatch': True})
    }
    r = client.post('/api/image-lab/analyze', data=data, content_type='multipart/form-data')
    assert r.status_code == 200
    img_res = json.loads(r.data)
    assert img_res["status"] == "success"
    assert "ela_url" in img_res
    assert "metadata" in img_res
    assert "assessment" in img_res
    print(f"PASS: Deepfake Lab processed image. ELA generated: {bool(img_res['ela_url'])}, Assessment verdict: '{img_res['assessment']['verdict']}'")

    print("--- 6. Testing Mandatory Automation (Claim to Checklist) ---")
    auto_payload = {
        "claim": "Viral forward claiming WHO announced complete eradication of seasonal flu in 2026.",
        "category": "health",
        "source_url": "https://health-wire.click/flu"
    }
    r = client.post('/api/automation/claim-to-checklist', data=json.dumps(auto_payload), content_type='application/json')
    assert r.status_code == 200
    auto_res = json.loads(r.data)["data"]
    assert len(auto_res["steps"]) == 10
    checklist_id = auto_res["checklist_id"]
    print(f"PASS: Automation generated custom 10-step protocol (Checklist ID #{checklist_id})")

    # Update checklist step
    update_payload = {
        "id": checklist_id,
        "claim_title": auto_res["claim_title"],
        "category": auto_res["inferred_category"],
        "checklist_data": auto_res["steps"],
        "completed_steps": 3,
        "total_steps": 10,
        "final_verdict": "Contradicted by available evidence",
        "final_notes": "Checked WHO GISRS database; claim is unsubstantiated."
    }
    r_up = client.post('/api/checklists/update', data=json.dumps(update_payload), content_type='application/json')
    assert r_up.status_code == 200
    print("PASS: Checklist progress & notes successfully updated in database")

    print("--- 7. Testing Scam Quiz Submission ---")
    quiz_payload = {"score": 9, "total": 10}
    r = client.post('/api/quiz/submit', data=json.dumps(quiz_payload), content_type='application/json')
    assert r.status_code == 200
    q_data = json.loads(r.data)
    assert q_data["percentage"] == 90.0
    print(f"PASS: Quiz result recorded. Score: {q_data['score']}/10 ({q_data['percentage']}%)")

    print("--- 8. Testing Report History & Exports ---")
    r_hist = client.get('/api/reports')
    assert r_hist.status_code == 200
    reports = json.loads(r_hist.data)["data"]
    assert len(reports) > 0
    test_report_id = reports[0]["id"]

    # Export Markdown
    r_md = client.get(f'/api/export/report/{test_report_id}?format=markdown')
    assert r_md.status_code == 200
    assert b"TruthLens AI" in r_md.data

    # Export JSON
    r_json = client.get(f'/api/export/report/{test_report_id}?format=json')
    assert r_json.status_code == 200
    assert json.loads(r_json.data)["id"] == test_report_id
    print(f"PASS: History retrieved ({len(reports)} records) and exported to Markdown/JSON successfully.")

    print("\nALL 8 MODULE WORKFLOWS PASSED VALIDATION WITH ZERO ERRORS!")

if __name__ == '__main__':
    run_checks()
