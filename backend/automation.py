"""
TruthLens AI - Mandatory Automation Engine: Suspicious Claim to Verification Checklist
Automatically decomposes claims, categorizes issues, synthesizes 10 tailored verification steps,
and prepares an interactive checklist dossier ready for user execution and export.
"""

import re
import os
import json
from .database import save_checklist

def generate_claim_checklist(claim_text, category="other", source_url=""):
    """
    Executes automated transformation of a raw claim into a structured,
    actionable 10-step verification dossier.
    """
    clean_claim = claim_text.strip()
    words = clean_claim.split()

    # Step 1: Extract Main Factual Claim
    main_sentence = clean_claim.split('.')[0] if '.' in clean_claim else clean_claim
    if len(main_sentence) > 160:
        main_sentence = main_sentence[:157] + '...'

    # Step 2: Categorize the likely issue and entities
    inferred_category = category
    text_lower = clean_claim.lower()

    if any(k in text_lower for k in ['rbi', 'bank', 'rupees', 'loan', 'crypto', 'bonus', 'salary', 'lottery', '500%']):
        inferred_category = 'finance'
    elif any(k in text_lower for k in ['cure', 'doctor', 'remedy', 'who', 'flu', 'cancer', 'vaccine', 'virus']):
        inferred_category = 'health'
    elif any(k in text_lower for k in ['hack', 'otp', 'password', 'phish', 'apk', 'cert-in', 'malware', 'leak']):
        inferred_category = 'cybersecurity'
    elif any(k in text_lower for k in ['minister', 'election', 'court', 'parliament', 'law', 'police', 'modi', 'biden']):
        inferred_category = 'politics'
    elif any(k in text_lower for k in ['photo', 'video', 'alien', 'taj mahal', 'eclipse', 'ufo', 'miracle']):
        inferred_category = 'multimedia_or_other'

    # Step 3 & 4: Generate 10 Structured Tailored Verification Steps
    # Key search terms extracted from the claim
    query_keywords = "+".join([re.sub(r'[^a-zA-Z0-9]', '', w) for w in words[:6] if len(w) > 3])

    steps = [
        {
            "step_id": 1,
            "title": "Source & Origin Identification",
            "category": "Source Check",
            "instruction": f"Identify the primary creator or earliest indexed post for this claim. Do not rely solely on forwarded messages.",
            "target_action": f"Search Google News for exact phrase: \"{main_sentence[:60]}\"",
            "completed": False,
            "user_notes": ""
        },
        {
            "step_id": 2,
            "title": "Author Credentials & Publication Timestamp",
            "category": "Attribution",
            "instruction": "Check whether the author is an accredited specialist in this domain and verify when the article was first published.",
            "target_action": "Inspect author byline, biographical portfolio, and cross-reference on LinkedIn / ORCID.",
            "completed": False,
            "user_notes": ""
        },
        {
            "step_id": 3,
            "title": "Reverse Media & Keyframe Verification",
            "category": "Media Forensics",
            "instruction": "If the claim incorporates an image or video capture, test whether the visual is authentic, recycled from past archives, or AI-synthesized.",
            "target_action": "Upload keyframe or photo to Google Lens, TinEye, or TruthLens Deepfake Awareness Lab.",
            "completed": False,
            "user_notes": ""
        },
        {
            "step_id": 4,
            "title": "Original Context & Chronology Check",
            "category": "Contextual Alignment",
            "instruction": "Verify if the original quote or footage was captured during a different year, event, or geographic region.",
            "target_action": "Check if an old event is being re-circulated as happening today.",
            "completed": False,
            "user_notes": ""
        },
        {
            "step_id": 5,
            "title": "Independent Multi-Source Corroboration",
            "category": "Cross-Referencing",
            "instruction": "Look for corroboration across at least two established, independent news wires or academic journals.",
            "target_action": "Consult Reuters, AP News, PTI, or official gazette registries.",
            "completed": False,
            "user_notes": ""
        },
        {
            "step_id": 6,
            "title": "Primary Document & Citation Audit",
            "category": "Evidence Review",
            "instruction": "If laws, government schemes, medical trials, or regulatory fines are mentioned, locate the primary official document.",
            "target_action": "Search official portals (e.g., pib.gov.in, rbi.org.in, who.int, cert-in.org.in).",
            "completed": False,
            "user_notes": ""
        },
        {
            "step_id": 7,
            "title": "Visual Artifacts & Synthetic Consistency",
            "category": "Forensic Inspection",
            "instruction": "Inspect fine media textures for diffusion model artifacts: warped backgrounds, asymmetric eyes, inconsistent earlobes, and unnatural lighting.",
            "target_action": "Run Error Level Analysis (ELA) and zoom into high-contrast edge boundaries.",
            "completed": False,
            "user_notes": ""
        },
        {
            "step_id": 8,
            "title": "Emotional Manipulation & Artificial Urgency Audit",
            "category": "Linguistic Heuristics",
            "instruction": "Analyze psychological triggers: Does the post provoke extreme panic, outrage, or demand immediate money transfer before midnight?",
            "target_action": "Identify sensational hyperbolic adjectives and pressure tactics.",
            "completed": False,
            "user_notes": ""
        },
        {
            "step_id": 9,
            "title": "Cyber Scam & Phishing Indicators",
            "category": "Threat Assessment",
            "instruction": "Verify whether the message asks to download an untrusted APK, share banking OTP, or log into a lookalike domain.",
            "target_action": "Evaluate URL using TruthLens Source Credibility Explorer.",
            "completed": False,
            "user_notes": ""
        },
        {
            "step_id": 10,
            "title": "Final Synthesis, Verdict & Responsible Reporting",
            "category": "Decision & Action",
            "instruction": "Synthesize the findings. If fraudulent or false, avoid amplifying it and report to relevant cybersecurity portals.",
            "target_action": "Assign final status and export verified TruthLens verification dossier.",
            "completed": False,
            "user_notes": ""
        }
    ]

    # Save to SQLite
    checklist_record = {
        "claim_title": clean_claim,
        "category": inferred_category,
        "checklist_data": steps,
        "completed_steps": 0,
        "total_steps": 10,
        "final_verdict": "In Progress — Verification Pending",
        "final_notes": f"Automated 10-step verification protocol generated by TruthLens AI Automation Engine for claim: \"{main_sentence}\""
    }

    db_id = save_checklist(checklist_record)

    return {
        "checklist_id": db_id,
        "claim_title": clean_claim,
        "main_claim": main_sentence,
        "inferred_category": inferred_category,
        "source_url": source_url,
        "steps": steps,
        "automation_mode": "Automated Claim-to-Checklist Pipeline (10-Stage Protocol)",
        "message": "Custom 10-step verification protocol generated successfully. You can now execute and update findings for each step."
    }
