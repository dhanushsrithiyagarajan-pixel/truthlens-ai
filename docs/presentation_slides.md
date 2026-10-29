# TruthLens AI — College Capstone Presentation Slides (Markdown Source)
**Title:** TruthLens AI: AI-Powered Deepfake and Misinformation Awareness Platform  
**Tagline:** "Pause. Investigate. Verify."  
**Degree:** Final-Year / College Cybersecurity Capstone Defense  

---

## Slide 1: Title & Capstone Introduction
- **Project Name:** TruthLens AI
- **Subtitle:** AI-Powered Deepfake and Misinformation Awareness Platform
- **Tagline:** *"Pause. Investigate. Verify."*
- **Domain:** Cybersecurity, Digital Media Forensics, Applied AI Ethics
- **Technology Stack:** Python 3.9 (Flask), SQLite, Vanilla CSS3 / HTML5 SPA, Chart.js, Pillow (Forensics)

---

## Slide 2: Problem Statement & Motivation
- **The Generative Explosion:** Latent diffusion models and neural vocoders enable instant generation of synthetic photos, videos, and cloned voices.
- **Cognitive Exploitation:** Misinformation exploits manufactured urgency ("Act before midnight") and outrage to bypass rational evaluation.
- **Cheap Fakes & Recycling:** Over 60% of viral visual disinformation repurposes genuine historical photographs with deceptive modern captions.
- **The Core Deficiency:** Citizens lack a structured, multi-source investigative protocol.

---

## Slide 3: Proposed Architecture & Core Modules
- **Dual-Mode Verification Engine:** Transparent NLP heuristic analyzer + optional Gemini LLM reasoning.
- **Deepfake Forensics Lab:** EXIF camera metadata inspection, Error Level Analysis (ELA), visual inconsistency checklists.
- **Source Credibility Explorer:** URL structural anatomy, typosquatting heuristics, and TLD threat modeling.
- **Interactive Verification Dossier:** 10-step investigative workflow with persistent SQLite state.
- **Public Awareness & Cybercrime Portals:** Direct guidance on Indian statutory helplines (1930 / cybercrime.gov.in).

---

## Slide 4: Mandatory Technical Automation
- **Tool:** "Suspicious Claim to Verification Checklist" Pipeline
- **Workflow:**
  1. *Entity & Claim Extraction:* Automatically decomposes raw claims into factual assertions.
  2. *Threat Vector Ingestion:* Categorizes threats (phishing, financial fraud, biomedical claims).
  3. *Tailored Protocol Synthesis:* Formulates 10 dynamic investigative steps with targeted search queries.
  4. *Persistent Synchronization:* Saves state to SQLite and opens directly in the interactive dossier editor.

---

## Slide 5: Testing Methodology & Empirical Results
- **10 Benchmark Scenarios:** Evaluated across genuine news, misleading composites, phishing, Ponzi schemes, and synthetic dubbing.
- **Test Suite Pass Rate:** 15/15 unit and integration test assertions passed (`tests/test_verification_benchmarks.py`).
- **Honest Uncertainty:** Ambiguous or uncorroborated claims labeled strictly as *Unverified — more evidence required*.
- **Anti-Hallucination Guardrails:** Zero synthetic sources, URLs, or fake citations generated.

---

## Slide 6: Ethics, Limitations & Responsible AI
- **The Fallibility of AI Detectors:** Lossy compression (WhatsApp/X) degrades forensic signals, creating false positives.
- **No Deceptive Deepfakes:** The platform strictly prohibits generating deceptive media of real individuals.
- **Human-in-the-Loop:** Algorithmic ratings serve as *advisory tools*, not definitive judicial verdicts.
- **Statutory Integration:** Prominently links to CERT-In, PIB Fact Check, and the National Cyber Crime Reporting Portal.

---

## Slide 7: Conclusion & Future Work
- **Summary:** TruthLens AI delivers a production-grade, beginner-friendly educational suite ready for academic defense and public awareness.
- **Future Milestones:**
  1. Hardware-level C2PA provenance cryptographic signature validation.
  2. Browser extension for automated lateral reading nudges.
  3. Regional Indian language multilingual support (Hindi, Tamil, Telugu, Bengali).
