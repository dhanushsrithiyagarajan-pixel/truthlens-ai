# TruthLens AI — Prompt Engineering & AI Research Library
## Documentation of Structured Prompts, Verification Heuristics & Ethical Guardrails
**Document Purpose:** Records all generative AI system prompts, few-shot schemas, heuristic decomposition templates, and ethical guardrails utilized throughout the development and operation of TruthLens AI.

---

### 1. System Prompt: Objective Claim Verification Engine
- **Target Model:** Gemini 2.5 Flash / Standard Generative LLMs
- **Module:** Module B (Claim Verification)
- **File Reference:** `backend/verifier.py`
- **Purpose:** Restrains generative models from making unsubstantiated real/fake binary assertions and enforces rigorous JSON schema output.

```text
You are TruthLens AI, an objective, rigorous cybersecurity and fact-checking research engine.
Your task is to analyze claims submitted by students and citizens.

Core Operational Rules:
1. Never claim that an image, video, or claim is definitely fake or real without sufficient evidence.
2. Clearly distinguish verified facts, unverified claims, suspicious indicators, and AI-generated assessments.
3. Choose strictly ONE verdict from the 5 academic standards:
   - "Supported by available evidence"
   - "Contradicted by available evidence"
   - "Misleading or missing context"
   - "Unverified — more evidence required"
   - "Suspicious indicators detected"
4. Assign a numerical confidence rating (0-100) reflecting empirical evidence strength.
5. Separate testable factual statements from emotional opinions.
6. Do NOT invent citations, URLs, or non-existent gazette notices. If unverified, state so clearly.
7. Output valid JSON matching the exact schema.
```

---

### 2. Prompt: Structured Claim Decomposition & Fact Extraction
- **Input Variables:** `claim_text`, `source_url`, `source_name`, `category`, `context`
- **Output Requirement:** Strict JSON format with empirical decomposition.

```text
Analyze the following submission:
Claim: {claim_text}
Source URL: {source_url}
Source Name: {source_name}
Category: {category}
Context: {context}

Respond ONLY with a JSON object in this format:
{
    "main_claim": "One concise sentence summarizing the core factual assertion",
    "verdict": "Choose one exact verdict string",
    "confidence": 85,
    "factual_statements": ["statement 1", "statement 2"],
    "opinion_statements": ["opinion 1"],
    "corroboration_needs": ["need 1", "need 2"],
    "evidence_summary": "Comprehensive explanation of evidence or lack thereof",
    "suspicious_indicators": ["indicator 1", "indicator 2"],
    "recommendations": ["recommendation 1", "recommendation 2"],
    "limitations": "Explicit statement of verification limitations"
}
```

---

### 3. Prompt: Visual Consistency & Forensics Synthesis
- **Module:** Module C (Deepfake Awareness Lab)
- **File Reference:** `backend/image_lab.py`
- **Purpose:** Guides users through structured forensic observation before running algorithmic filters.

```text
Evaluate observed visual anomalies across 8 standardized synthetic artifacts:
1. Earlobe and jewelry asymmetry
2. Inconsistent specular pupil reflections
3. Dental blur or abnormal teeth uniformity
4. Warped background architectural straight lines
5. Porcelain over-smoothed skin textures
6. Contradictory lighting and shadow vectors
7. Anomalous hand anatomy (extra digits)
8. Discontinuous glasses frames or apparel seams
```

---

### 4. Heuristic Rule-Based NLP Pipeline (Offline Engine)
- **Module:** `backend/verifier.py` (`analyze_with_heuristics`)
- **Purpose:** Provides 100% deterministic, offline functionality when no API credentials are present.
- **Pattern Matching Subsets:**
  - `URGENCY_KEYWORDS`: Catches emotional pressure and deadlines (`urgent`, `before midnight`, `act now`).
  - `SCAM_FINANCIAL_KEYWORDS`: Catches high-yield Ponzi inducement (`guaranteed return`, `500%`, `crypto bot`, `free gift`).
  - `PHISHING_KEYWORDS`: Catches credential harvesting (`update KYC`, `account blocked`, `install APK`).
  - `SUSPICIOUS_DOMAINS_TLD`: Catches disposable registries (`.top`, `.xyz`, `.click`, `.work`).

---

### 5. Ethical Constraints and Guardrails
1. **Anti-Hallucination Guardrail:** If an entity cannot be corroborated against known authoritative registers (such as WHO, RBI, PIB, or peer-reviewed literature), the prompt enforces the label *Unverified — more evidence required*.
2. **No Deceptive Media Generation:** Prompts are restricted to analysis, decomposition, and defense education. No prompt may be used to synthesize deceptive audio, deepfake portraits of real living persons, or forged identity documents.
3. **Transparent Mode Attribution:** Every report generated explicitly notes whether it was produced via generative LLM analysis or the local heuristic fact-check engine.
