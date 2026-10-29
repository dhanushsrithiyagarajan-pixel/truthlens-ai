"""
TruthLens AI - Deepfake Awareness & Image Forensics Lab
Provides educational image analysis: EXIF metadata parsing, Error Level Analysis (ELA),
visual artifact checklists, and reverse image search guidance.
"""

import os
import io
import math
from PIL import Image, ImageChops, ImageEnhance
from PIL.ExifTags import TAGS

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_exif(image_path):
    """
    Extract readable EXIF metadata from an uploaded image.
    Looks for camera models, timestamps, and AI generator/software footprints.
    """
    metadata = {
        "has_exif": False,
        "camera_make": "Not found",
        "camera_model": "Not found",
        "date_time_original": "Not found",
        "software": "Not found",
        "dimensions": "Unknown",
        "color_space": "Unknown",
        "raw_tags": {},
        "ai_or_editing_clues": []
    }

    try:
        with Image.open(image_path) as img:
            metadata["dimensions"] = f"{img.width} x {img.height} pixels"
            metadata["format"] = img.format
            metadata["mode"] = img.mode

            exif_data = img._getexif()
            if exif_data:
                metadata["has_exif"] = True
                for tag_id, value in exif_data.items():
                    tag_name = TAGS.get(tag_id, tag_id)
                    # Convert bytes or large unprintable structures
                    if isinstance(value, bytes):
                        try:
                            value_str = value.decode('utf-8', errors='ignore')
                        except Exception:
                            value_str = f"Binary ({len(value)} bytes)"
                    else:
                        value_str = str(value)

                    if str(tag_name) in ['Make', 'Model', 'Software', 'DateTimeOriginal', 'DateTime', 'Artist', 'Copyright']:
                        metadata["raw_tags"][str(tag_name)] = value_str

                    if tag_name == 'Make':
                        metadata["camera_make"] = value_str
                    elif tag_name == 'Model':
                        metadata["camera_model"] = value_str
                    elif tag_name in ['DateTimeOriginal', 'DateTime']:
                        metadata["date_time_original"] = value_str
                    elif tag_name == 'Software':
                        metadata["software"] = value_str

            # Check for AI synthesis signatures or editing markers in tags or image headers
            software_lower = str(metadata["software"]).lower()
            if any(term in software_lower for term in ['photoshop', 'gimp', 'canva', 'lightroom']):
                metadata["ai_or_editing_clues"].append(f"Edited with software: {metadata['software']}")
            elif any(term in software_lower for term in ['midjourney', 'stable diffusion', 'dall-e', 'comfyui', 'novelai']):
                metadata["ai_or_editing_clues"].append(f"AI synthesis signature in metadata: {metadata['software']}")

            # PNG or WebP info dictionaries often hold generation parameters (e.g. A1111 prompts)
            if hasattr(img, 'info') and img.info:
                for k, v in img.info.items():
                    k_str = str(k).lower()
                    v_str = str(v)
                    if any(term in k_str or term in v_str.lower() for term in ['prompt', 'negative_prompt', 'steps', 'sampler', 'cfg scale', 'seed']):
                        metadata["ai_or_editing_clues"].append(f"Metadata tag '{k}' contains diffusion model generation parameters.")
                        metadata["has_exif"] = True
                        break

    except Exception as e:
        metadata["error"] = str(e)

    return metadata

def generate_ela(image_path, output_path, quality=90, scale=15):
    """
    Generate Error Level Analysis (ELA) image.
    ELA resaves the image at a known JPEG quality and calculates the pixel difference
    between the original and recompressed image.
    Spliced or foreign elements often show different compression error levels.
    """
    try:
        with Image.open(image_path) as orig:
            orig = orig.convert('RGB')
            # Save temporary recompressed version in memory
            buffer = io.BytesIO()
            orig.save(buffer, 'JPEG', quality=quality)
            buffer.seek(0)
            recompressed = Image.open(buffer)

            # Calculate difference
            diff = ImageChops.difference(orig, recompressed)

            # Amplify the differences so human eyes can inspect them
            extrema = diff.getextrema()
            max_diff = max([ex[1] for ex in extrema]) if extrema else 1
            if max_diff == 0:
                max_diff = 1

            enhancer = ImageEnhance.Brightness(diff)
            ela_image = enhancer.enhance(scale)
            ela_image.save(output_path, 'JPEG')
            return True, None
    except Exception as e:
        return False, str(e)

def compute_forensic_assessment(exif_meta, visual_checks=None):
    """
    Computes an educational forensic synthesis based on metadata findings
    and user-observed visual indicators.
    """
    score = 0
    clues = list(exif_meta.get("ai_or_editing_clues", []))
    indicators = []

    # Metadata checks
    if not exif_meta.get("has_exif"):
        indicators.append("No EXIF metadata detected (typical of social media compression or synthetic generators).")
    else:
        indicators.append("EXIF metadata preserved; camera and timestamp attributes inspected.")

    if clues:
        score += 35
        for c in clues:
            indicators.append(f"Metadata Alert: {c}")

    # Visual checklist evaluation if provided
    checklist_weight = {
        "ear_asymmetry": 15,
        "pupil_reflection_mismatch": 20,
        "teeth_blur_uniformity": 15,
        "background_warping": 20,
        "skin_over_smoothing": 15,
        "unnatural_lighting_direction": 15,
        "hand_anatomy_anomalies": 20,
        "jewelry_clothing_discontinuity": 15
    }

    if visual_checks and isinstance(visual_checks, dict):
        for check, checked in visual_checks.items():
            if checked and check in checklist_weight:
                score += checklist_weight[check]
                clean_name = check.replace('_', ' ').title()
                indicators.append(f"Visual Inconsistency Observed: {clean_name}")

    # Determine educational assessment
    if score >= 60:
        verdict = "Multiple Synthetic / Tampering Indicators Present"
        confidence = min(85, 50 + score // 2)
        summary = "Image exhibits significant anomalies across visual consistency markers or metadata tags characteristic of generative AI synthesis or digital compositing."
    elif score >= 25:
        verdict = "Inconclusive / Suspicious Patterns Noted"
        confidence = 55
        summary = "Several inconsistencies or metadata omissions were noted. The media warrants reverse image provenance verification before acceptance."
    else:
        verdict = "No Obvious High-Confidence Anomalies Detected"
        confidence = 45
        summary = "Image does not present overt synthetic artifacts on inspected dimensions. However, modern high-fidelity diffusion models often leave minimal visual traces. Technical analysis alone cannot prove authenticity."

    educational_notes = [
        "Modern diffusion models (e.g., Flux, Midjourney v6, SDXL) generate highly realistic skin textures and symmetry.",
        "Social media platforms (WhatsApp, Twitter/X, Instagram) automatically strip all camera EXIF data upon upload for privacy.",
        "Therefore, absence of EXIF data does NOT automatically imply malicious synthesis.",
        "Always cross-reference with reverse image search engines and trusted editorial wires."
    ]

    return {
        "verdict": verdict,
        "confidence": confidence,
        "indicators": indicators,
        "summary": summary,
        "educational_notes": educational_notes,
        "disclaimer": "CRITICAL: This is an educational forensics tool. TruthLens AI never claims definitive proof of authenticity or fakery without cryptographic watermarking (e.g. C2PA provenance)."
    }
