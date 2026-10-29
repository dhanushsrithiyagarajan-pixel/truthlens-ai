import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'truthlens.db')

def get_connection():
    """Establish connection to SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables and seed sample records if empty."""
    conn = get_connection()
    cursor = conn.cursor()

    # Table 1: Verification Reports
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        claim TEXT NOT NULL,
        source_url TEXT,
        source_name TEXT,
        category TEXT NOT NULL,
        verdict TEXT NOT NULL,
        confidence INTEGER NOT NULL,
        main_claim TEXT NOT NULL,
        factual_statements TEXT,
        opinion_statements TEXT,
        corroboration_needs TEXT,
        evidence_summary TEXT,
        suspicious_indicators TEXT,
        recommendations TEXT,
        limitations TEXT,
        is_demo INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Table 2: Interactive Checklists & Automations
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS checklists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        claim_title TEXT NOT NULL,
        category TEXT NOT NULL,
        checklist_data TEXT NOT NULL,
        completed_steps INTEGER DEFAULT 0,
        total_steps INTEGER DEFAULT 10,
        final_verdict TEXT,
        final_notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Table 3: Quiz Logs
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS quiz_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        score INTEGER NOT NULL,
        total_questions INTEGER NOT NULL,
        percentage REAL NOT NULL,
        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()

    # Check if we should seed initial demonstration records
    cursor.execute('SELECT COUNT(*) FROM reports')
    count = cursor.fetchone()[0]
    if count == 0:
        seed_demo_data(cursor)
        conn.commit()

    conn.close()

def seed_demo_data(cursor):
    """Seed benchmark educational records clearly labeled as Demonstration Data."""
    sample_reports = [
        {
            "claim": "RBI issues alert warning that linking Aadhaar to PAN on unauthorized third-party links will lead to direct bank account debit.",
            "source_url": "https://rbi-notice-alert.top/pan-link-warning",
            "source_name": "Viral WhatsApp Forward / Unofficial Blog",
            "category": "finance",
            "verdict": "Suspicious indicators detected",
            "confidence": 88,
            "main_claim": "The Reserve Bank of India has issued an urgent directive claiming third-party PAN-Aadhaar linking causes automatic unauthorized account debits.",
            "factual_statements": json.dumps([
                "Claims an official RBI advisory was released on an urgent basis.",
                "Asserts that bank accounts are automatically debited upon entering details on specific sites."
            ]),
            "opinion_statements": json.dumps([
                "Framed with high panic and urgency ('Act immediately before midnight today')."
            ]),
            "corroboration_needs": json.dumps([
                "Search RBI official circulars repository (rbi.org.in).",
                "Verify domain registration of 'rbi-notice-alert.top'.",
                "Consult Press Information Bureau (PIB Fact Check) advisories."
            ]),
            "evidence_summary": "Domain uses a deceptive top-level domain (.top) impersonating the central bank. No matching notification exists in official RBI press releases. Official RBI communication guidelines mandate notifications solely through rbi.org.in.",
            "suspicious_indicators": json.dumps([
                "Lookalike domain impersonating official regulator",
                "Artificial panic/urgency ('within 24 hours')",
                "Lack of official press release number or verifiable circular ID",
                "Generic greeting and unverified contact numbers"
            ]),
            "recommendations": json.dumps([
                "Do not click the provided link or enter financial credentials.",
                "Visit the official RBI website (rbi.org.in) directly.",
                "Report suspicious messages to the National Cyber Crime Reporting Portal (cybercrime.gov.in) or call 1930."
            ]),
            "limitations": "Static domain analysis and official gazette cross-referencing. Live banking API access is not conducted.",
            "is_demo": 1
        },
        {
            "claim": "WHO announces complete eradication of all seasonal influenza variants through new universal vaccine protocol in 2026.",
            "source_url": "https://global-health-news-wire.click/who-flu-cure",
            "source_name": "Health Daily Wire",
            "category": "health",
            "verdict": "Contradicted by available evidence",
            "confidence": 92,
            "main_claim": "The World Health Organization declared seasonal influenza completely eradicated worldwide in 2026.",
            "factual_statements": json.dumps([
                "States that the WHO released an eradication declaration in 2026.",
                "Asserts universal vaccine protocol eliminated all circulating strains."
            ]),
            "opinion_statements": json.dumps([
                "Overstated revolutionary rhetoric claiming total permanent immunity for human population."
            ]),
            "corroboration_needs": json.dumps([
                "WHO Disease Outbreak News and Global Influenza Surveillance and Response System (GISRS).",
                "Peer-reviewed medical literature (Lancet, NEJM, PubMed)."
            ]),
            "evidence_summary": "WHO GISRS continues active monitoring of seasonal A(H1N1), A(H3N2), and B strains. While universal mRNA and mosaic flu vaccines are in clinical trials, no eradication declaration has ever been issued. Viral mutation dynamics make immediate total eradication biologically improbable.",
            "suspicious_indicators": json.dumps([
                "Sensational medical breakthrough claim unsupported by peer-reviewed literature",
                "Absence of official WHO press release link or scientific trial registry ID",
                "Disreputable ad-heavy aggregator domain"
            ]),
            "recommendations": json.dumps([
                "Check WHO official updates at who.int.",
                "Verify through biomedical repositories like PubMed and ICMR bulletins.",
                "Consult certified healthcare practitioners before modifying preventive measures."
            ]),
            "limitations": "Evaluated against current biomedical consensus and WHO public declarations. Does not perform clinical trial auditing.",
            "is_demo": 1
        },
        {
            "claim": "ISRO successfully launches indigenous quantum key distribution satellite demonstrator for defense communications.",
            "source_url": "https://isro.gov.in/press-release-quantum-comms.html",
            "source_name": "Press Trust of India & ISRO Press Release",
            "category": "cybersecurity",
            "verdict": "Supported by available evidence",
            "confidence": 95,
            "main_claim": "ISRO demonstrated satellite-based quantum secure communication capabilities.",
            "factual_statements": json.dumps([
                "ISRO conducted satellite quantum key distribution (QKD) demonstrations.",
                "Project connects defense research establishments with quantum secure optical links."
            ]),
            "opinion_statements": json.dumps([]),
            "corroboration_needs": json.dumps([
                "Verify official press release on isro.gov.in.",
                "Cross-check coverage across national news agencies (PTI, ANI)."
            ]),
            "evidence_summary": "Independently verified through official ISRO press releases and collaborative research publications with Raman Research Institute. Milestone extensively documented across national press agencies.",
            "suspicious_indicators": json.dumps([]),
            "recommendations": json.dumps([
                "Refer to isro.gov.in and peer-reviewed conference publications for technical specifications."
            ]),
            "limitations": "Classified cryptographic details are naturally outside the scope of public verification.",
            "is_demo": 1
        },
        {
            "claim": "Leaked video shows prominent tech CEO endorsing guaranteed 500% weekly return cryptocurrency automated trading bot.",
            "source_url": "https://telegram.org/channel/crypto-wealth-bot-leak",
            "source_name": "Telegram Forward / Viral Video",
            "category": "finance",
            "verdict": "Suspicious indicators detected",
            "confidence": 96,
            "main_claim": "A renowned technology executive personally verified and endorsed a high-yield algorithmic cryptocurrency scheme in a video recording.",
            "factual_statements": json.dumps([
                "Features visual appearance of known executive speaking about financial investment.",
                "Promises 500% guaranteed weekly returns."
            ]),
            "opinion_statements": json.dumps([
                "Claims this is an 'exclusive loophole hidden by Wall Street elites'."
            ]),
            "corroboration_needs": json.dumps([
                "Perform reverse video frame search on speech segments.",
                "Analyze lip synchronization and phonetic phoneme alignment.",
                "Check official executive social media channels and corporate SEC filings."
            ]),
            "evidence_summary": "Classic deepfake audio-visual dubbing impersonation scam. The visual footage originates from a 2023 keynote address, manipulated using voice cloning to pitch an unregulated Telegram deposit address. Guaranteed 500% returns are mathematically unsustainable and characteristic of Ponzi fraud.",
            "suspicious_indicators": json.dumps([
                "High-risk promise of guaranteed extraordinary returns (Ponzi hallmark)",
                "Audio-video sync mismatch and unnatural vocal cadence",
                "Call to send crypto to unverified external wallet address",
                "No official corporate corroboration or regulatory registration"
            ]),
            "recommendations": json.dumps([
                "Do not transfer funds to the advertised wallet address.",
                "Report video to the hosting social media platform for synthetic impersonation.",
                "File an alert with CERT-In and Indian Cybercrime Reporting Portal (1930 / cybercrime.gov.in)."
            ]),
            "limitations": "Behavioral scam signature and acoustic provenance analysis. Cryptographic wallet tracing requires blockchain ledger tools.",
            "is_demo": 1
        },
        {
            "claim": "Photograph shows rare double rainbow over the Taj Mahal during solar eclipse with violet auroral clouds.",
            "source_url": "https://instagram.com/p/viral-taj-eclipse",
            "source_name": "Social Media Aggregator",
            "category": "other",
            "verdict": "Misleading or missing context",
            "confidence": 91,
            "main_claim": "A photograph captures a simultaneous total solar eclipse, double rainbow, and auroral display over Agra, India.",
            "factual_statements": json.dumps([
                "Claims image is an authentic single-exposure photograph taken at the Taj Mahal."
            ]),
            "opinion_statements": json.dumps([
                "Described as a 'once-in-a-century miraculous astronomical event'."
            ]),
            "corroboration_needs": json.dumps([
                "Astrophysical timeline check: dates of total solar eclipses visible from Agra.",
                "Atmospheric physics check: rainbows require direct sunlight, which is occluded during eclipse totality.",
                "Geomagnetic latitude check: auroras do not naturally extend to Agra's equatorial/tropical latitude."
            ]),
            "evidence_summary": "Scientifically impossible single exposure. A total solar eclipse blocks the direct solar ray refraction necessary for rainbow formation. Agra (latitude ~27°N) is geomagnetic tropical and does not exhibit polar auroras. Reverse image search traces elements to Midjourney/Photoshop composite art created for an art contest.",
            "suspicious_indicators": json.dumps([
                "Physics inconsistency: simultaneous eclipse and bright refractive rainbow",
                "Geographic impossibility: polar auroral phenomena in northern tropical plains",
                "Composite digital artwork repurposed and shared as authentic documentary capture"
            ]),
            "recommendations": json.dumps([
                "Credit original digital artist rather than claiming it as a physical documentary photograph.",
                "Verify astronomical events through NASA Eclipse Web or Indian Institute of Astrophysics (IIA)."
            ]),
            "limitations": "Physical law and reverse-image contextual inspection. Does not evaluate pixel-level compression noise.",
            "is_demo": 1
        }
    ]

    for item in sample_reports:
        cursor.execute('''
        INSERT INTO reports (
            claim, source_url, source_name, category, verdict, confidence,
            main_claim, factual_statements, opinion_statements, corroboration_needs,
            evidence_summary, suspicious_indicators, recommendations, limitations, is_demo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item['claim'], item['source_url'], item['source_name'], item['category'],
            item['verdict'], item['confidence'], item['main_claim'],
            item['factual_statements'], item['opinion_statements'], item['corroboration_needs'],
            item['evidence_summary'], item['suspicious_indicators'], item['recommendations'],
            item['limitations'], item['is_demo']
        ))

# CRUD Operations

def get_all_reports(category=None, verdict=None, search=None):
    """Retrieve all reports with optional filtering."""
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM reports WHERE 1=1"
    params = []

    if category and category != 'all':
        query += " AND category = ?"
        params.append(category)

    if verdict and verdict != 'all':
        query += " AND verdict = ?"
        params.append(verdict)

    if search:
        query += " AND (claim LIKE ? OR main_claim LIKE ? OR source_name LIKE ?)"
        term = f"%{search}%"
        params.extend([term, term, term])

    query += " ORDER BY id DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()

    reports = []
    for row in rows:
        r = dict(row)
        for key in ['factual_statements', 'opinion_statements', 'corroboration_needs', 'suspicious_indicators', 'recommendations']:
            try:
                r[key] = json.loads(r[key]) if r[key] else []
            except Exception:
                r[key] = []
        reports.append(r)

    conn.close()
    return reports

def get_report_by_id(report_id):
    """Retrieve a single report by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reports WHERE id = ?", (report_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    r = dict(row)
    for key in ['factual_statements', 'opinion_statements', 'corroboration_needs', 'suspicious_indicators', 'recommendations']:
        try:
            r[key] = json.loads(r[key]) if r[key] else []
        except Exception:
            r[key] = []
    return r

def save_report(data):
    """Save a new verification report to the database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO reports (
        claim, source_url, source_name, category, verdict, confidence,
        main_claim, factual_statements, opinion_statements, corroboration_needs,
        evidence_summary, suspicious_indicators, recommendations, limitations, is_demo
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('claim', ''),
        data.get('source_url', ''),
        data.get('source_name', 'Unknown Source'),
        data.get('category', 'other'),
        data.get('verdict', 'Unverified — more evidence required'),
        data.get('confidence', 50),
        data.get('main_claim', data.get('claim', '')),
        json.dumps(data.get('factual_statements', [])),
        json.dumps(data.get('opinion_statements', [])),
        json.dumps(data.get('corroboration_needs', [])),
        data.get('evidence_summary', ''),
        json.dumps(data.get('suspicious_indicators', [])),
        json.dumps(data.get('recommendations', [])),
        data.get('limitations', 'Evidence-based preliminary assessment. Independent human verification required.'),
        data.get('is_demo', 0)
    ))

    report_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return report_id

def delete_report(report_id):
    """Delete a report by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reports WHERE id = ?", (report_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def get_dashboard_metrics():
    """Compute live dashboard metrics from database."""
    conn = get_connection()
    cursor = conn.cursor()

    # Total reports count
    cursor.execute("SELECT COUNT(*) FROM reports")
    total_reports = cursor.fetchone()[0]

    # Live user reports vs seeded demo reports
    cursor.execute("SELECT COUNT(*) FROM reports WHERE is_demo = 0")
    user_reports = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reports WHERE is_demo = 1")
    demo_reports = cursor.fetchone()[0]

    # Reports by verdict
    cursor.execute("SELECT verdict, COUNT(*) FROM reports GROUP BY verdict")
    verdict_counts = {row[0]: row[1] for row in cursor.fetchall()}

    # Reports by category
    cursor.execute("SELECT category, COUNT(*) FROM reports GROUP BY category")
    category_counts = {row[0]: row[1] for row in cursor.fetchall()}

    # Average confidence
    cursor.execute("SELECT AVG(confidence) FROM reports")
    avg_confidence = cursor.fetchone()[0]
    avg_confidence = round(avg_confidence, 1) if avg_confidence else 0.0

    # Total checklists created
    cursor.execute("SELECT COUNT(*) FROM checklists")
    total_checklists = cursor.fetchone()[0]

    # Total quiz attempts & average score
    cursor.execute("SELECT COUNT(*), AVG(percentage) FROM quiz_logs")
    quiz_stats = cursor.fetchone()
    total_quizzes = quiz_stats[0] if quiz_stats else 0
    avg_quiz_score = round(quiz_stats[1], 1) if quiz_stats and quiz_stats[1] else 0.0

    # Recent 5 reports
    cursor.execute("SELECT id, claim, category, verdict, confidence, created_at, is_demo FROM reports ORDER BY id DESC LIMIT 5")
    recent_reports = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return {
        "total_reports": total_reports,
        "user_reports": user_reports,
        "demo_reports": demo_reports,
        "verdict_counts": verdict_counts,
        "category_counts": category_counts,
        "avg_confidence": avg_confidence,
        "total_checklists": total_checklists,
        "total_quizzes": total_quizzes,
        "avg_quiz_score": avg_quiz_score,
        "recent_reports": recent_reports
    }

# Checklist Operations

def save_checklist(data):
    """Save or update an interactive verification checklist."""
    conn = get_connection()
    cursor = conn.cursor()

    checklist_id = data.get('id')
    checklist_data_json = json.dumps(data.get('checklist_data', []))

    if checklist_id:
        cursor.execute('''
        UPDATE checklists
        SET claim_title = ?, category = ?, checklist_data = ?, completed_steps = ?,
            total_steps = ?, final_verdict = ?, final_notes = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        ''', (
            data.get('claim_title'),
            data.get('category', 'other'),
            checklist_data_json,
            data.get('completed_steps', 0),
            data.get('total_steps', 10),
            data.get('final_verdict', 'In Progress'),
            data.get('final_notes', ''),
            checklist_id
        ))
    else:
        cursor.execute('''
        INSERT INTO checklists (
            claim_title, category, checklist_data, completed_steps, total_steps, final_verdict, final_notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('claim_title', 'Untitled Verification'),
            data.get('category', 'other'),
            checklist_data_json,
            data.get('completed_steps', 0),
            data.get('total_steps', 10),
            data.get('final_verdict', 'In Progress'),
            data.get('final_notes', '')
        ))
        checklist_id = cursor.lastrowid

    conn.commit()
    conn.close()
    return checklist_id

def get_checklist_by_id(checklist_id):
    """Retrieve checklist by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM checklists WHERE id = ?", (checklist_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    c = dict(row)
    try:
        c['checklist_data'] = json.loads(c['checklist_data'])
    except Exception:
        c['checklist_data'] = []
    return c

def log_quiz_result(score, total, percentage):
    """Log anonymous quiz completion for academic analytics."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO quiz_logs (score, total_questions, percentage) VALUES (?, ?, ?)",
                   (score, total, percentage))
    conn.commit()
    conn.close()
