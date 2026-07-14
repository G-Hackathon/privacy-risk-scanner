import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


# -----------------------------
# Tracker Signatures
# -----------------------------

TRACKERS = {
    "Google Analytics": [
        "google-analytics.com",
        "analytics.js",
        "gtag(",
        "ga.js"
    ],

    "Google Tag Manager": [
        "googletagmanager.com"
    ],

    "Facebook Pixel": [
        "connect.facebook.net",
        "fbq("
    ],

    "Hotjar": [
        "hotjar"
    ],

    "Mixpanel": [
        "mixpanel"
    ],

    "Microsoft Clarity": [
        "clarity.ms"
    ]
}


# -----------------------------
# Security Headers
# -----------------------------

SECURITY_HEADERS = [

    "Content-Security-Policy",

    "Strict-Transport-Security",

    "X-Frame-Options",

    "X-Content-Type-Options",

    "Referrer-Policy"

]


# -----------------------------
# AI Explanations
# -----------------------------

EXPLANATIONS = {

    "Website is not using HTTPS.": {
        "severity": "High",
        "explanation":
        "The connection is not encrypted.",
        "recommendation":
        "Avoid entering sensitive information."
    },

    "Privacy Policy not found.": {
        "severity": "Medium",
        "explanation":
        "The website does not clearly explain how it handles personal data.",
        "recommendation":
        "Review the website carefully before sharing personal information."
    },

    "Cookies detected.": {
        "severity": "Low",
        "explanation":
        "Cookies may be used for login sessions, preferences, or tracking.",
        "recommendation":
        "Disable non-essential cookies if possible."
    },

    "Password field detected.": {
        "severity": "Medium",
        "explanation":
        "The website requests account credentials.",
        "recommendation":
        "Only sign in if you trust the website."
    },

    "Email collection detected.": {
        "severity": "Low",
        "explanation":
        "The website requests an email address.",
        "recommendation":
        "Share only if necessary."
    }

}


# -----------------------------
# Grade Calculator
# -----------------------------

def get_grade(score):

    if score >= 95:
        return "A+"

    elif score >= 90:
        return "A"

    elif score >= 80:
        return "B"

    elif score >= 70:
        return "C"

    elif score >= 60:
        return "D"

    return "F"


# -----------------------------
# AI Builder
# -----------------------------

def build_ai_results(risks):

    results = []

    for risk in risks:

        if risk in EXPLANATIONS:

            info = EXPLANATIONS[risk]

            results.append({

                "title": risk,

                "severity": info["severity"],

                "explanation": info["explanation"],

                "recommendation": info["recommendation"]

            })

    return results


# -----------------------------
# Main Scanner
# -----------------------------

def analyze(url):

    score = 100

    risks = []

    suggestions = []

    trackers = []

    security_headers = []

    third_party_scripts = 0

    parsed = urlparse(url)

    domain = parsed.netloc

    try:

        response = requests.get(

            url,

            timeout=8,

            headers={

                "User-Agent":
                "Mozilla/5.0"

            }

        )

    except Exception as e:

        return {

            "url": url,

            "score": 0,

            "grade": "F",

            "risks": [

                "Website could not be reached."

            ],

            "suggestions": [

                str(e)

            ],

            "trackers": [],

            "security_headers": [],

            "third_party_scripts": 0,

            "ai_analysis": []

        }

    html = response.text

    html_lower = html.lower()

    soup = BeautifulSoup(html, "html.parser")

    # -----------------------------
    # HTTPS
    # -----------------------------

    if not url.startswith("https://"):

        score -= 20

        risks.append(

            "Website is not using HTTPS."

        )

        suggestions.append(

            "Use HTTPS websites whenever possible."

        )

    # -----------------------------
    # Privacy Policy
    # -----------------------------

    if "privacy policy" not in html_lower:

        score -= 15

        risks.append(

            "Privacy Policy not found."

        )

        suggestions.append(

            "Read the site's privacy practices."

        )

    # -----------------------------
    # Cookies
    # -----------------------------

    if "cookie" in html_lower:

        score -= 5

        risks.append(

            "Cookies detected."

        )

    # -----------------------------
    # Login Forms
    # -----------------------------

    if soup.find("input", {"type": "password"}):

        score -= 5

        risks.append(

            "Password field detected."

        )

    if soup.find("input", {"type": "email"}):

        score -= 3

        risks.append(

            "Email collection detected."

        )

    # ====== PART 2 STARTS BELOW ======
    # -----------------------------
    # Tracker Detection
    # -----------------------------

    for tracker, signatures in TRACKERS.items():

        detected = False

        for signature in signatures:

            if signature.lower() in html_lower:

                detected = True
                break

        if detected:

            trackers.append(tracker)

            risks.append(f"{tracker} detected.")

            score -= 6

            if tracker == "Google Analytics":

                EXPLANATIONS[f"{tracker} detected."] = {
                    "severity": "Medium",
                    "explanation": "Google Analytics collects visitor statistics and browsing behaviour.",
                    "recommendation": "Use tracker blocking extensions if you wish to reduce analytics tracking."
                }

            elif tracker == "Google Tag Manager":

                EXPLANATIONS[f"{tracker} detected."] = {
                    "severity": "Medium",
                    "explanation": "Google Tag Manager loads tracking and marketing scripts.",
                    "recommendation": "Review browser privacy settings to reduce unnecessary tracking."
                }

            elif tracker == "Facebook Pixel":

                EXPLANATIONS[f"{tracker} detected."] = {
                    "severity": "High",
                    "explanation": "Facebook Pixel is commonly used for advertising and cross-site tracking.",
                    "recommendation": "Consider limiting third-party tracking or using a privacy-focused browser."
                }

            elif tracker == "Hotjar":

                EXPLANATIONS[f"{tracker} detected."] = {
                    "severity": "Medium",
                    "explanation": "Hotjar records visitor interactions to improve website usability.",
                    "recommendation": "Review the privacy policy before sharing personal information."
                }

            elif tracker == "Mixpanel":

                EXPLANATIONS[f"{tracker} detected."] = {
                    "severity": "Medium",
                    "explanation": "Mixpanel collects user behaviour analytics.",
                    "recommendation": "Only provide information that is necessary."
                }

            elif tracker == "Microsoft Clarity":

                EXPLANATIONS[f"{tracker} detected."] = {
                    "severity": "Medium",
                    "explanation": "Microsoft Clarity records user interactions and browsing behaviour.",
                    "recommendation": "Use browser privacy controls if you wish to minimise tracking."
                }

    # -----------------------------
    # Third-party Scripts
    # -----------------------------

    scripts = soup.find_all("script", src=True)

    for script in scripts:

        src = script["src"]

        if src.startswith("http"):

            third_party_scripts += 1

    if third_party_scripts > 15:

        score -= 10

        risks.append("Large number of third-party scripts.")

        suggestions.append(
            "This website loads many external scripts."
        )

    elif third_party_scripts > 5:

        score -= 5

        risks.append("Several third-party scripts.")

    # -----------------------------
    # Security Headers
    # -----------------------------

    headers = response.headers

    for header in SECURITY_HEADERS:

        if header in headers:

            security_headers.append(header)

        else:

            score -= 2

    if len(security_headers) < 3:

        suggestions.append(
            "Website is missing several recommended security headers."
        )

    # -----------------------------
    # Overall Suggestions
    # -----------------------------

    if len(trackers) >= 3:

        suggestions.append(
            "Multiple tracking technologies were detected."
        )

    if score >= 90:

        suggestions.append(
            "Excellent privacy practices detected."
        )

    elif score >= 75:

        suggestions.append(
            "Overall privacy is good but could be improved."
        )

    elif score >= 50:

        suggestions.append(
            "Exercise caution before sharing sensitive information."
        )

    else:

        suggestions.append(
            "High privacy risk. Consider avoiding sensitive activities on this website."
        )

    # -----------------------------
    # AI Analysis
    # -----------------------------

    ai_analysis = build_ai_results(risks)

    # -----------------------------
    # Prevent Negative Scores
    # -----------------------------

    score = max(score, 0)

    # -----------------------------
    # Final Result
    # -----------------------------

    return {

        "url": url,

        "domain": domain,

        "score": score,

        "grade": get_grade(score),

        "risks": risks,

        "suggestions": suggestions,

        "trackers": trackers,

        "security_headers": security_headers,

        "third_party_scripts": third_party_scripts,

        "ai_analysis": ai_analysis

    }
