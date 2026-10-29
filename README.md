# TruthLens AI — AI-Powered Deepfake and Misinformation Awareness Platform

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Flask%203.1-00f2fe.svg)](https://palletsprojects.com/p/flask/)
[![Database](https://img.shields.io/badge/Database-SQLite3-8b5cf6.svg)](https://sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-10b981.svg)](LICENSE)
[![Tests: 15 Passed](https://img.shields.io/badge/Tests-15%2F15%20Passing-emerald.svg)](tests/)
[![Capstone](https://img.shields.io/badge/Capstone-Cybersecurity%202026-c4b5fd.svg)](docs/)

> **Tagline:** *"Pause. Investigate. Verify."*  
> **Academic Capstone:** Final-Year College Project titled *"AI Deepfake and Misinformation Awareness Project"*

TruthLens AI is an interactive cybersecurity awareness and verification platform engineered to help students, researchers, and digital citizens identify suspicious online claims, understand synthetic media (deepfakes) and online scams, evaluate domain and source credibility, and follow a structured, evidence-based verification protocol.

---

## 🌟 Key Features & Modules

### 📊 Module A: Main Dashboard
- **Live Empirical Analytics:** Real-time metrics computed directly from actual SQLite database records (total reports, user submissions vs. demonstration samples, mean confidence score).
- **Interactive Charts (Chart.js):** Dynamic doughnut chart showing verdict distributions and horizontal bar chart tracking misinformation by domain.
- **7-Stage Workflow Visualizer:** Step-by-step graphic illustrating the investigative pipeline.
- **Recent Audit Activity:** Real-time ledger of evaluated claims with click-to-inspect modal.

### 🔍 Module B: AI-Powered Claim Verification
- **7-Stage Evidence Pipeline:** Deconstructs submitted claims into empirical assertions vs. emotive opinions.
- **5 Standard Academic Verdicts:**
  - `Supported by available evidence`
  - `Contradicted by available evidence`
  - `Misleading or missing context`
  - `Unverified — more evidence required`
  - `Suspicious indicators detected`
- **Dual-Engine Architecture:** Operates with live generative AI APIs (Google Gemini) or 100% offline via a deterministic NLP heuristic engine.

### 🧪 Module C: Deepfake Awareness & Image Forensics Lab
- **Safe Image Upload:** Validates MIME types (JPEG, PNG, WEBP) up to 5MB in an isolated sandbox.
- **Error Level Analysis (ELA):** Re-compresses imagery at a known quality level and amplifies compression differences to highlight digital splicing.
- **EXIF Metadata Extraction:** Parses camera make, model, original timestamps, and software generation tags (Photoshop, Midjourney, Stable Diffusion).
- **Visual Inconsistency Checklist:** Interactive checks for pupil reflections, earlobe asymmetry, and background warping.
- **Reverse Image Search Launcher:** Direct integration with Google Lens, TinEye, Yandex, and Bing Visual Search.

### 🌐 Module D: Source Credibility Explorer
- **Domain Anatomy Inspection:** Audits HTTPS protocol status, domain structure, and TLD risk meters.
- **Typosquatting & Brand Impersonation Heuristics:** Flags deceptive brand mimicry (e.g., unauthorized domains imitating `rbi`, `sbi`, or `who`).
- **Educational Reality Checks:** Explains why an HTTPS padlock alone does NOT prove that claims on a website are true.

### 📋 Module E: Interactive Verification Checklist & Dossier
- **10-Step Investigative Workflow:** Complete guide from source identification to statutory reporting.
- **State Tracking & Note-Taking:** Users record evidence findings, update step completion, and track progress (0%–100%).
- **Export Capabilities:** One-click generation of Markdown dossiers and printable PDF reports.

### ⚡ Module I: Mandatory Automation Tool
- **Suspicious Claim to Verification Checklist Pipeline:** Ingests raw social media text, extracts core assertions, categorizes the threat vector, and automatically synthesizes a tailored 10-step verification protocol equipped with targeted Boolean search queries.

### 📚 Module F, G & J: Public Safety, Quiz & Ethics
- **Public Awareness Hub:** Comprehensive guides on deepfakes, phishing, and task scams, with direct links to Indian statutory portals: **Helpline 1930**, **cybercrime.gov.in**, **CERT-In**, and **PIB Fact Check**.
- **Scam & Misinformation Quiz:** 10 original scenario-based questions featuring immediate forensic explanations after each response.
- **Ethics & Responsible AI:** In-depth discourse on false positives, model hallucinations, copyright, and the indispensable role of human oversight.

---

## 🏛️ System Architecture

```
                       [ TruthLens AI Single Page Application ]
                       (Vanilla CSS3 • HTML5 • Chart.js SPA)
                                          │
                  ┌───────────────────────┼───────────────────────┐
                  ▼                       ▼                       ▼
          [ Dashboard API ]       [ Verifier API ]        [ Forensics API ]
          /api/metrics            /api/verify             /api/image-lab/analyze
                  │                       │                       │
                  └───────────────────────┼───────────────────────┘
                                          ▼
                                [ Flask Application Server ]
                                      (app.py / REST)
                                          │
                  ┌───────────────────────┼───────────────────────┐
                  ▼                       ▼                       ▼
         [ NLP Heuristic Engine ]  [ ELA Forensics ]     [ Source Checker ]
         (verifier.py)             (image_lab.py)         (source_checker.py)
                  │                       │                       │
                  └───────────────────────┼───────────────────────┘
                                          ▼
                               [ SQLite Persistence ]
                                   (truthlens.db)
```

---

## 💻 Technology Stack

| Layer | Technology | Rationale |
|---|---|---|
| **Backend** | Python 3.9+ / Flask 3.1 | Lightweight, modular, rapid REST API development |
| **Database** | SQLite3 (`truthlens.db`) | Zero-configuration relational persistence, portable |
| **Frontend** | Semantic HTML5, CSS3, Vanilla JS | High-performance SPA with zero npm build complexity |
| **Forensics** | Pillow (PIL) | Error Level Analysis (ELA) and EXIF metadata extraction |
| **Data Viz** | Chart.js 4.4 | Real-time interactive charts with custom cyber palette |
| **Testing** | Python `unittest` | 15 unit and integration tests covering 10 benchmark cases |

---

## 🚀 Quickstart & Installation (Beginner Friendly)

### 1. Clone or Open the Repository
```bash
cd truthlens-ai
```

### 2. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 3. Run the Application
```bash
python app.py
```

### 4. Open in Your Web Browser
Navigate to:
👉 **`http://127.0.0.1:5000`**

*(Note: The application functions in **100% Offline Demo Mode** right out of the box. To optionally connect live Google Gemini generative AI reasoning, add your key to `.env` as `GEMINI_API_KEY=your_key_here`)*

---

## 🧪 Testing & Empirical Benchmark Validation

TruthLens AI includes an automated benchmark test suite covering 10 mandated capstone scenarios:
1. **Genuine Claim:** ISRO quantum satellite communications (Supported by evidence, 88% confidence)
2. **Misleading Context:** Solar eclipse rainbow over Taj Mahal (Misleading / Missing context)
3. **Unsupported Claim:** Mumbai-London ancient tunnel (Unverified — more evidence required)
4. **Phishing SMS:** Fake RBI midnight KYC update (Suspicious indicators detected)
5. **Giveaway Scam:** Free laptop bonus scheme (Suspicious indicators detected)
6. **Synthetic Media:** Tech CEO 500% crypto trading bot video (Suspicious indicators detected)
7. **Miscaptioned Image:** Protest photo misattributed (Misleading or missing context)
8. **Recycled Media:** Himalayan mothership viral rumor (Suspicious indicators detected)
9. **Impersonation Scam:** Electricity disconnection threat (Suspicious indicators detected)
10. **Ambiguous Technology:** Unpatented battery alloy range claim (Unverified — more evidence required)

### Run the Test Suite
```bash
python -m unittest discover tests
```
Output:
```text
...............
----------------------------------------------------------------------
Ran 15 tests in 0.052s

OK
```

---

## 📁 Project Folder Structure

```
truthlens-ai/
├── app.py                            # Main Flask server and REST API routes
├── requirements.txt                  # Python dependencies
├── truthlens.db                      # SQLite database (auto-initialized)
├── .env                              # Environment configuration
├── .env.example                      # Template environment configuration
├── .gitignore                        # Git ignore rules for secrets and uploads
├── LICENSE                           # MIT License
├── README.md                         # Main project documentation
├── backend/
│   ├── __init__.py                   # Backend package initializer
│   ├── database.py                   # SQLite schemas, seed demo data, and CRUD
│   ├── verifier.py                   # 7-stage verification engine (heuristics + LLM)
│   ├── image_lab.py                  # Image forensics, EXIF parser, and ELA generator
│   ├── source_checker.py             # URL credibility and typosquatting auditor
│   └── automation.py                 # Claim-to-Checklist mandatory automation engine
├── templates/
│   └── index.html                    # Responsive single-page application dashboard
├── static/
│   ├── css/
│   │   └── style.css                 # Custom cyber design system (dark navy / cyan)
│   ├── js/
│   │   ├── app.js                    # SPA router, navigation, and modal manager
│   │   ├── dashboard.js              # Live metrics visualizer & Chart.js renderer
│   │   ├── verifier.js               # Verification form submission & dossier renderer
│   │   ├── deepfake_lab.js           # Image upload, ELA toggle & visual checklist
│   │   ├── source_checker.js         # URL anatomy inspector & risk score meter
│   │   ├── checklist.js              # Interactive 10-step verification dossier
│   │   ├── automation.js             # Claim-to-Checklist automation client
│   │   ├── quiz.js                   # 10-question scam & misinformation quiz
│   │   └── history.js                # Report history ledger, filtering & exports
│   ├── uploads/                      # Isolated directory for uploaded test media
│   └── generated/                    # Output directory for generated ELA images
├── tests/
│   ├── test_verification_benchmarks.py # 10 benchmark scenario unit tests
│   └── test_api_endpoints.py         # Flask REST API integration tests
└── docs/
    ├── research_summary.md           # Academic literature review & 8+ references
    ├── verification_checklist.md     # Standard 10-step investigative guide
    ├── verification_test_results.md  # Detailed benchmark evaluation matrix
    ├── awareness_article.md          # ~1,000-word publishable awareness essay
    ├── social_media_posts.md         # 5 formatted social media awareness posts
    ├── awareness_poster.svg          # High-resolution vector campaign poster
    ├── awareness_poster.html         # Interactive poster viewer & print exporter
    ├── presentation_slides.html      # 7-slide interactive presentation deck
    ├── presentation_slides.md        # Slide presentation markdown source
    ├── claim_to_checklist_automation.md # Mandatory automation tool documentation
    ├── prompt_library.md             # Generative AI prompts & ethical guardrails
    ├── verification_report_sample.md # Before/after case study analysis
    ├── final_capstone_report.md      # Comprehensive academic final report
    ├── installation_and_user_guide.md# Quickstart & evaluation demonstration guide
    ├── demonstration_script.md       # 5-minute spoken viva defense script
    └── ethical_ai_and_limitations.md # Ethical statement, bias & human oversight
```

---

## ⚖️ Ethical Principles & Limitations

- **Probabilistic Fallibility:** TruthLens AI explicitly states that automated detectors cannot reliably identify 100% of deepfakes due to social media compression artifacts.
- **Zero Deceptive Synthesis:** The platform strictly prohibits the generation of deceptive deepfakes of real individuals.
- **Anti-Hallucination Guardrails:** If live evidence is unavailable, claims are honestly designated *Unverified — more evidence required* rather than fabricating citations.
- **Statutory Reporting:** Directly connects users to official Indian emergency cybercrime channels: **Helpline 1930** and [cybercrime.gov.in](https://cybercrime.gov.in).

---

## 📤 GitHub Publication Commands

To publish this project to your GitHub account:

```bash
# 1. Initialize git (if not already initialized)
git init

# 2. Add all project files
git add .

# 3. Commit the implementation
git commit -m "Initial commit: TruthLens AI Capstone Platform complete implementation"

# 4. Rename branch to main
git branch -M main

# 5. Link your GitHub repository (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/truthlens-ai.git

# 6. Push to GitHub
git push -u origin main
```

---

## 📜 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
