"""
TruthLens AI - Source Credibility Explorer
Inspects domain structure, protocol security, typo-squatting, TLD risk,
and provides structured credibility indicators.
"""

import urllib.parse
import re

SUSPICIOUS_TLDS = {
    '.top': 'Extremely high frequency in disposable malware/phishing campaigns.',
    '.xyz': 'Low-cost TLD frequently used for disposable spam or redirects.',
    '.click': 'Commonly associated with affiliate fraud and clickbait networks.',
    '.tk': 'Historically free domain registrar with high abuse rates.',
    '.ml': 'Free top-level domain frequently utilized in phishing operations.',
    '.work': 'High volume of impersonation and spam listings.',
    '.buzz': 'Associated with viral aggregator spam sites.',
    '.download': 'High risk for deceptive malware delivery.'
}

FAMOUS_BRAND_PATTERNS = [
    (r'google', ['google.com', 'google.co.in', 'googleblog.com']),
    (r'rbi', ['rbi.org.in']),
    (r'isro', ['isro.gov.in']),
    (r'who', ['who.int']),
    (r'sbi', ['onlinesbi.sbi', 'sbi.co.in']),
    (r'hdfc', ['hdfcbank.com']),
    (r'bbc', ['bbc.com', 'bbc.co.uk']),
    (r'reuters', ['reuters.com']),
    (r'pib', ['pib.gov.in', 'factcheck.pib.gov.in']),
    (r'gov', ['gov.in', 'nic.in', 'gov']),
]

def inspect_url(raw_url):
    """
    Evaluates URL security, structural anatomy, potential typosquatting,
    and credibility indicators.
    """
    if not raw_url or not isinstance(raw_url, str):
        return {"error": "Invalid or empty URL provided."}

    url = raw_url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    try:
        parsed = urllib.parse.urlparse(url)
    except Exception as e:
        return {"error": f"Failed to parse URL: {str(e)}"}

    domain = parsed.netloc.lower()
    # Strip port if present
    if ':' in domain:
        domain = domain.split(':')[0]

    path = parsed.path
    protocol = parsed.scheme.lower()

    findings = []
    positive_indicators = []
    caution_indicators = []
    risk_score = 0  # 0 to 100

    # 1. Protocol check
    if protocol == 'https':
        positive_indicators.append("Secure HTTPS connection in use (data in transit is encrypted).")
    else:
        caution_indicators.append("Insecure HTTP connection detected. Information sent to this website can be intercepted.")
        risk_score += 25

    # 2. IP address host check
    if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', domain):
        caution_indicators.append("Website uses a bare numeric IP address instead of a registered domain name (common in evasion tactics).")
        risk_score += 35

    # 3. Subdomain and Typosquatting checks
    domain_parts = domain.split('.')
    if len(domain_parts) >= 2:
        tld = '.' + domain_parts[-1]
        registered_domain = '.'.join(domain_parts[-2:])
        subdomains = domain_parts[:-2]
    else:
        tld = ''
        registered_domain = domain
        subdomains = []

    # Check suspicious TLD
    if tld in SUSPICIOUS_TLDS:
        caution_indicators.append(f"Domain uses '{tld}' top-level domain: {SUSPICIOUS_TLDS[tld]}")
        risk_score += 30

    # Check brand impersonation / typosquatting in subdomains or registered domain
    for brand, legit_domains in FAMOUS_BRAND_PATTERNS:
        if brand in domain:
            if not any(domain == legit or domain.endswith('.' + legit) for legit in legit_domains):
                caution_indicators.append(
                    f"Possible brand lookalike / typosquatting: Domain contains '{brand}' but is NOT an authorized domain ({', '.join(legit_domains[:2])})."
                )
                risk_score += 45

    # Hyphenated deceptive domain check (e.g., bbc-breaking-news-update.com)
    hyphen_count = domain.count('-')
    if hyphen_count >= 3:
        caution_indicators.append(f"High number of hyphens ({hyphen_count}) in domain name; characteristic of disposable phishing portals.")
        risk_score += 20

    # 4. Author / Publication Context in Path
    date_in_path = re.search(r'/(\d{4})/(\d{2})(/(\d{2}))?', path)
    if date_in_path:
        positive_indicators.append(f"Article path contains structured publication datestamp ({date_in_path.group(0)}), typical of organized editorial CMS.")
    else:
        caution_indicators.append("URL path lacks standard date taxonomy. Check page body directly for author byline and publication timestamp.")

    # 5. Government / Academic Recognition
    if domain.endswith('.gov.in') or domain.endswith('.nic.in') or domain.endswith('.gov'):
        positive_indicators.append("Official government top-level domain (.gov / .gov.in).")
        risk_score = max(0, risk_score - 50)
    elif domain.endswith('.edu') or domain.endswith('.ac.in'):
        positive_indicators.append("Accredited academic or university domain.")
        risk_score = max(0, risk_score - 30)

    # Calculate overall credibility status
    if risk_score >= 60:
        credibility_tier = "High Suspicion — Scrutinize Thoroughly"
        badge_color = "red"
    elif risk_score >= 30:
        credibility_tier = "Moderate Caution — Independent Corroboration Advised"
        badge_color = "amber"
    else:
        credibility_tier = "Standard / Low Risk Indicators Observed"
        badge_color = "emerald"

    educational_guidance = [
        "IMPORTANT: An HTTPS padlock or clean modern design only means your connection is encrypted; it does NOT verify that the claim on the page is true.",
        "Check the 'About Us' page: Does it list physical office addresses, editorial staff, and clear ownership?",
        "Compare with 3 independent reputable news wires (Reuters, AP, PTI, BBC) before trusting major breaking announcements.",
        "Never label a website fraudulent based solely on a single indicator (e.g., missing datestamp or unfamiliar design)."
    ]

    return {
        "url": url,
        "domain": domain,
        "protocol": protocol,
        "tld": tld,
        "registered_domain": registered_domain,
        "subdomains": subdomains,
        "risk_score": min(100, risk_score),
        "credibility_tier": credibility_tier,
        "badge_color": badge_color,
        "positive_indicators": positive_indicators,
        "caution_indicators": caution_indicators,
        "educational_guidance": educational_guidance
    }
