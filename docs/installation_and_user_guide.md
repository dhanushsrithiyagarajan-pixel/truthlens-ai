# TruthLens AI — Installation & User Demonstration Guide
## Beginner-Friendly Quickstart for College Presentations & Viva Voce
**Project:** TruthLens AI — AI-Powered Deepfake & Misinformation Awareness Platform  
**Target Audience:** Students, College Examiners, Evaluators, and General Users  

---

### 1. Prerequisites
You do **not** need complex database servers, Docker containers, or Node.js/npm. TruthLens AI runs directly on standard Python 3.9+:

- **Operating System:** Windows 10/11, macOS, or Linux.
- **Python:** Python 3.9 or higher (Verify with `python --version`).
- **Web Browser:** Google Chrome, Microsoft Edge, Firefox, or Safari.

---

### 2. Quickstart Installation (Under 2 Minutes)

#### Step 1: Open Terminal in Project Directory
Open PowerShell or Command Prompt and ensure you are in the project folder:
```powershell
cd c:\Users\Admin\OneDrive\Desktop\truthlens-ai
```

#### Step 2: Install Python Dependencies
Run pip to ensure dependencies are installed:
```powershell
python -m pip install -r requirements.txt
```
*(Dependencies: Flask, python-dotenv, requests, Pillow, reportlab, google-genai)*

#### Step 3: Run the TruthLens AI Server
Start the local application server:
```powershell
python app.py
```

You will see:
```text
==================================================
 TruthLens AI - AI Deepfake & Misinformation Platform
 'Pause. Investigate. Verify.'
 Server starting on http://127.0.0.1:5000
==================================================
```

#### Step 4: Open in Web Browser
Open your browser and navigate to:
👉 **`http://127.0.0.1:5000`**

---

### 3. Live Demonstration Guide for College Evaluators

Follow this exact flow during your live demonstration:

#### 1. The Main Dashboard (Module A)
- Point out the **Live Platform Metrics**: Show that total reports, mean confidence, and active checklists are calculated directly from the SQLite database.
- Highlight the **Real-time Charts**: Explain the Verdict Distribution doughnut chart and Misinformation by Category bar chart.
- Show the **7-Stage Visual Verification Workflow**.

#### 2. AI-Powered Claim Verification (Module B)
- Click on **"🔍 Verify Claim"** in the top navigation.
- Click the benchmark button **"Phishing/Finance Scam Sample"** to auto-populate the form.
- Click **"Run Evidence Verification Analysis"**.
- Walk the examiner through the resulting **Structured Dossier**:
  - Show the verdict badge: *Suspicious indicators detected*.
  - Show the **Confidence Meter** (88%).
  - Highlight the separation of **Empirical Factual Statements** from **Emotive Opinion Rhetoric**.
  - Review the **Suspicious Indicators** (e.g., lookalike domain, artificial midnight deadline).

#### 3. Mandatory Automation (Module I)
- From the verification result, click **"⚡ Convert to Interactive 10-Step Checklist"** (or open the **"⚡ Automation"** tab).
- Show how the system programmatically decomposes the claim, infers the threat vector, and synthesizes 10 tailored verification steps.
- Check off 2–3 steps, enter investigation notes, and click **"Save Checklist State"**.
- Click **"Print / Save PDF Dossier"** to demonstrate printable export capability!

#### 4. Deepfake Forensics Lab (Module C)
- Navigate to **"🧪 Deepfake Lab"**.
- Drag or select an image file.
- Explain the **Visual Inconsistency Checklist** (eye reflections, ear asymmetry, background warping).
- Click **"Run Forensic Analysis & Error Level Analysis (ELA)"**.
- Show the side-by-side **Original vs. ELA Derivative** and explain how compression quantization anomalies expose spliced elements.
- Show the **EXIF Camera Metadata Table** and highlight the mandatory forensic disclaimer: *No automated tool can reliably detect every deepfake; human verification is indispensable.*

#### 5. Source Credibility Explorer (Module D)
- Open **"🌐 Source Explorer"**.
- Enter `https://rbi-notice-alert.top/verify`.
- Click **"Audit Source Credibility"**.
- Show how the tool detects the high-risk `.top` TLD, flags the brand lookalike keyword, and computes the risk meter score.

#### 6. Scam Quiz & Public Safety Hub (Modules F & G)
- Open **"🎯 Scam Quiz"**: Answer a question to show the instant educational explanation.
- Open **"📚 Learning Hub"**: Point out the official Indian statutory cybercrime reporting channels: **National Helpline 1930** and **cybercrime.gov.in**.

---

### 4. Running the Automated Test Suite

To demonstrate code quality and academic verification to examiners, run the test suite:
```powershell
python -m unittest discover tests
```
Output:
```text
...............
----------------------------------------------------------------------
Ran 15 tests in 0.052s

OK
```
All 15 tests execute and pass in under a second!

---

### 5. Troubleshooting & FAQs

- **Q: Does this require an internet connection?**  
  **A:** No. TruthLens AI includes a full offline heuristic rule engine. It runs 100% locally with zero internet access required.
- **Q: How do I enable live Google Gemini LLM mode?**  
  **A:** Open `.env`, set `GEMINI_API_KEY=your_key_here`, and restart `python app.py`. The engine automatically detects the key and switches to generative reasoning mode.
- **Q: Where is data stored?**  
  **A:** All verification audits, checklists, and quiz logs are stored in `truthlens.db` (SQLite) in the project root directory.
