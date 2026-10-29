"""
TruthLens AI - Flask Application Server
AI-Powered Deepfake and Misinformation Awareness Platform
Cybersecurity Capstone Project
"""

import os
import json
import uuid
from flask import Flask, render_template, request, jsonify, send_from_directory, Response
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment configuration
load_dotenv()

from backend.database import (
    init_db, get_dashboard_metrics, get_all_reports, get_report_by_id,
    save_report, delete_report, save_checklist, get_checklist_by_id, log_quiz_result
)
from backend.verifier import analyze_claim
from backend.image_lab import extract_exif, generate_ela, compute_forensic_assessment, allowed_file
from backend.source_checker import inspect_url
from backend.automation import generate_claim_checklist

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'truthlens-dev-secret-key-2026')
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB maximum upload
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
app.config['GENERATED_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'generated')

# Ensure necessary directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['GENERATED_FOLDER'], exist_ok=True)

# Initialize SQLite database and seed demo data if needed
init_db()

@app.route('/')
def index():
    """Renders the main TruthLens AI dashboard."""
    return render_template('index.html')

# ----------------- Module A: Dashboard Metrics API -----------------

@app.route('/api/metrics', methods=['GET'])
def api_metrics():
    """Returns live metrics derived directly from actual database records."""
    try:
        metrics = get_dashboard_metrics()
        return jsonify({"status": "success", "data": metrics})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ----------------- Module B: Claim Verification API -----------------

@app.route('/api/verify', methods=['POST'])
def api_verify():
    """
    Submits a claim for structured 7-stage verification.
    Stores the resulting verification report in SQLite.
    """
    data = request.get_json() or {}
    claim = data.get('claim', '').strip()
    source_url = data.get('source_url', '').strip()
    source_name = data.get('source_name', '').strip()
    category = data.get('category', 'other')
    context = data.get('context', '').strip()

    if not claim:
        return jsonify({"status": "error", "message": "Claim text is required."}), 400

    try:
        analysis = analyze_claim(claim, source_url, source_name, category, context)
        # Mark as user submission (is_demo = 0)
        analysis['is_demo'] = 0
        report_id = save_report(analysis)
        analysis['id'] = report_id

        return jsonify({
            "status": "success",
            "report_id": report_id,
            "data": analysis
        })
    except Exception as e:
        return jsonify({"status": "error", "message": f"Verification failed: {str(e)}"}), 500

# ----------------- Module C: Deepfake Awareness Lab API -----------------

@app.route('/api/image-lab/analyze', methods=['POST'])
def api_image_analyze():
    """
    Accepts uploaded image, parses EXIF metadata, generates Error Level Analysis (ELA),
    and produces educational forensics checklist assessment.
    """
    if 'image' not in request.files:
        return jsonify({"status": "error", "message": "No image file provided."}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No file selected."}), 400

    if not allowed_file(file.filename):
        return jsonify({"status": "error", "message": "Unsupported file format. Please upload JPG, PNG, or WEBP."}), 400

    filename = secure_filename(file.filename)
    unique_prefix = uuid.uuid4().hex[:10]
    saved_filename = f"{unique_prefix}_{filename}"
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], saved_filename)
    file.save(upload_path)

    # Generate ELA derivative
    ela_filename = f"ela_{unique_prefix}.jpg"
    ela_path = os.path.join(app.config['GENERATED_FOLDER'], ela_filename)
    ela_success, ela_error = generate_ela(upload_path, ela_path)

    # Extract EXIF metadata
    exif_meta = extract_exif(upload_path)

    # Optional visual checks passed from user checklist
    visual_checks_raw = request.form.get('visual_checks', '{}')
    try:
        visual_checks = json.loads(visual_checks_raw)
    except Exception:
        visual_checks = {}

    assessment = compute_forensic_assessment(exif_meta, visual_checks)

    # Reverse search helper URLs
    reverse_search_tools = [
        {"name": "Google Lens", "url": "https://lens.google.com", "description": "Powerful visual search for matching imagery across web pages."},
        {"name": "TinEye Reverse Image Search", "url": "https://tineye.com", "description": "Specialized in identifying earliest date of indexing and modified copies."},
        {"name": "Yandex Visual Search", "url": "https://yandex.com/images", "description": "Particularly effective for facial matching and uncropped origins."},
        {"name": "Bing Visual Search", "url": "https://www.bing.com/visualsearch", "description": "Secondary corroboration tool for high-resolution sources."}
    ]

    return jsonify({
        "status": "success",
        "image_url": f"/static/uploads/{saved_filename}",
        "ela_url": f"/static/generated/{ela_filename}" if ela_success else None,
        "filename": filename,
        "metadata": exif_meta,
        "assessment": assessment,
        "reverse_search_tools": reverse_search_tools
    })

# ----------------- Module D: Source Credibility Explorer API -----------------

@app.route('/api/source/inspect', methods=['POST'])
def api_source_inspect():
    """Inspects a domain and URL structure for security, credibility, and typo-squatting."""
    data = request.get_json() or {}
    url = data.get('url', '').strip()
    if not url:
        return jsonify({"status": "error", "message": "Source URL is required."}), 400

    inspection = inspect_url(url)
    if "error" in inspection:
        return jsonify({"status": "error", "message": inspection["error"]}), 400

    return jsonify({"status": "success", "data": inspection})

# ----------------- Module E & I: Verification Checklist & Automation API -----------------

@app.route('/api/automation/claim-to-checklist', methods=['POST'])
def api_claim_to_checklist():
    """
    Mandatory Automation: Ingests suspicious claim, categorizes issue,
    generates tailored 10-step checklist, and stores it in SQLite.
    """
    data = request.get_json() or {}
    claim = data.get('claim', '').strip()
    category = data.get('category', 'other')
    source_url = data.get('source_url', '').strip()

    if not claim:
        return jsonify({"status": "error", "message": "Claim is required for automated checklist generation."}), 400

    checklist_result = generate_claim_checklist(claim, category, source_url)
    return jsonify({"status": "success", "data": checklist_result})

@app.route('/api/checklists/<int:checklist_id>', methods=['GET'])
def api_get_checklist(checklist_id):
    """Retrieve checklist by ID."""
    checklist = get_checklist_by_id(checklist_id)
    if not checklist:
        return jsonify({"status": "error", "message": "Checklist not found."}), 404
    return jsonify({"status": "success", "data": checklist})

@app.route('/api/checklists/update', methods=['POST'])
def api_update_checklist():
    """Updates checklist steps progress and notes."""
    data = request.get_json() or {}
    checklist_id = save_checklist(data)
    return jsonify({"status": "success", "checklist_id": checklist_id})

# ----------------- Module G: Quiz Submission API -----------------

@app.route('/api/quiz/submit', methods=['POST'])
def api_quiz_submit():
    """Logs anonymous quiz performance analytics."""
    data = request.get_json() or {}
    score = int(data.get('score', 0))
    total = int(data.get('total', 10))
    percentage = round((score / total) * 100, 1) if total > 0 else 0.0

    log_quiz_result(score, total, percentage)
    return jsonify({
        "status": "success",
        "score": score,
        "total": total,
        "percentage": percentage
    })

# ----------------- Module H: Report History & Export API -----------------

@app.route('/api/reports', methods=['GET'])
def api_get_reports():
    """Returns stored reports with optional filters."""
    category = request.args.get('category')
    verdict = request.args.get('verdict')
    search = request.args.get('search')

    reports = get_all_reports(category, verdict, search)
    return jsonify({"status": "success", "count": len(reports), "data": reports})

@app.route('/api/reports/<int:report_id>', methods=['GET'])
def api_get_single_report(report_id):
    """Returns a single report by ID."""
    report = get_report_by_id(report_id)
    if not report:
        return jsonify({"status": "error", "message": "Report not found."}), 404
    return jsonify({"status": "success", "data": report})

@app.route('/api/reports/<int:report_id>', methods=['DELETE'])
def api_delete_report(report_id):
    """Deletes a report by ID."""
    success = delete_report(report_id)
    if success:
        return jsonify({"status": "success", "message": f"Report #{report_id} deleted."})
    return jsonify({"status": "error", "message": "Report not found or deletion failed."}), 404

@app.route('/api/export/report/<int:report_id>', methods=['GET'])
def api_export_report(report_id):
    """Exports a report in JSON or Markdown format."""
    format_type = request.args.get('format', 'json').lower()
    report = get_report_by_id(report_id)
    if not report:
        return jsonify({"status": "error", "message": "Report not found."}), 404

    if format_type == 'markdown':
        md_content = f"""# TruthLens AI — Verification Dossier #{report['id']}
**Generated by:** TruthLens AI Platform (Tagline: "Pause. Investigate. Verify.")
**Evaluation Timestamp:** {report['created_at']}
**Record Type:** {'Demonstration Sample' if report['is_demo'] else 'User Live Submission'}

---

## 1. Executive Summary
- **Claim Under Review:** "{report['claim']}"
- **Source Cited:** {report['source_name']} ({report['source_url'] or 'No URL provided'})
- **Domain Category:** {report['category'].upper()}
- **Final Verdict:** **{report['verdict']}**
- **Confidence Rating:** {report['confidence']}%

---

## 2. Claim Decomposition
- **Main Factual Claim:** {report['main_claim']}
- **Factual Assertions:**
{chr(10).join([f"  - {item}" for item in report['factual_statements']]) if report['factual_statements'] else "  - None identified"}
- **Subjective / Opinion Statements:**
{chr(10).join([f"  - {item}" for item in report['opinion_statements']]) if report['opinion_statements'] else "  - None detected"}

---

## 3. Evidence & Forensic Rationale
{report['evidence_summary']}

### Corroboration Requirements:
{chr(10).join([f"- {item}" for item in report['corroboration_needs']])}

### Suspicious Indicators Detected:
{chr(10).join([f"- [!] {item}" for item in report['suspicious_indicators']]) if report['suspicious_indicators'] else "- None identified"}

---

## 4. Recommended Actions
{chr(10).join([f"1. {item}" for item in report['recommendations']])}

---

## 5. Ethical Limitations & Academic Disclaimer
{report['limitations']}
*Note: TruthLens AI provides structured educational assessments and does not replace official law enforcement, judicial determinations, or authoritative regulatory gazettes.*
"""
        return Response(
            md_content,
            mimetype="text/markdown",
            headers={"Content-disposition": f"attachment; filename=truthlens_dossier_{report_id}.md"}
        )

    # Default JSON export
    return Response(
        json.dumps(report, indent=2),
        mimetype="application/json",
        headers={"Content-disposition": f"attachment; filename=truthlens_dossier_{report_id}.json"}
    )

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    debug = os.getenv('FLASK_DEBUG', '1') == '1'
    print(f"==================================================")
    print(f" TruthLens AI - AI Deepfake & Misinformation Platform")
    print(f" 'Pause. Investigate. Verify.'")
    print(f" Server starting on http://{host}:{port}")
    print(f"==================================================")
    app.run(host=host, port=port, debug=debug)

