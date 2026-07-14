EXPLANATIONS = {

    "Website is not using HTTPS.": {

        "severity": "High",

        "explanation":
        "The connection is not encrypted. Information such as passwords or personal details could potentially be intercepted while being transmitted.",

        "recommendation":
        "Avoid entering sensitive information unless the website uses HTTPS."

    },

    "Privacy Policy not found.": {

        "severity": "Medium",

        "explanation":
        "Users cannot easily determine how their personal information is collected, stored, shared, or deleted.",

        "recommendation":
        "Look for another page describing the site's privacy practices before sharing personal information."

    },

    "Cookies detected.": {

        "severity": "Low",

        "explanation":
        "Cookies are commonly used to remember preferences and sessions, but they can also be used to track browsing behavior.",

        "recommendation":
        "Review the cookie preferences and disable non-essential cookies if available."

    },

    "Password field detected.": {

        "severity": "Medium",

        "explanation":
        "The website requests account credentials. Make sure the site is trustworthy before signing in.",

        "recommendation":
        "Use a strong unique password and enable multi-factor authentication when possible."

    },

    "Email collection detected.": {

        "severity": "Low",

        "explanation":
        "The website asks for an email address, which may be used for communication or marketing.",

        "recommendation":
        "Only provide an email address if you trust the website."

    },

    "Google Analytics detected.": {

        "severity": "Medium",

        "explanation":
        "Google Analytics records visitor activity to help website owners understand how people use their site.",

        "recommendation":
        "Use tracker blocking extensions if you want to reduce analytics tracking."

    },

    "Google Tag Manager detected.": {

        "severity": "Medium",

        "explanation":
        "Google Tag Manager makes it easier to load tracking scripts from multiple providers.",

        "recommendation":
        "Review browser privacy settings to reduce unnecessary tracking."

    },

    "Facebook Pixel detected.": {

        "severity": "High",

        "explanation":
        "Facebook Pixel can be used to measure advertising effectiveness and build advertising audiences across websites.",

        "recommendation":
        "Consider limiting third-party tracking or using privacy-focused browser settings."

    },

    "Hotjar detected.": {

        "severity": "Medium",

        "explanation":
        "Hotjar records user interactions such as clicks, scrolling, and navigation to improve website usability.",

        "recommendation":
        "Review the site's privacy policy to understand how interaction data is handled."

    },

    "Mixpanel detected.": {

        "severity": "Medium",

        "explanation":
        "Mixpanel collects product usage analytics and user behavior information.",

        "recommendation":
        "Share only the information necessary for using the service."

    },

    "Microsoft Clarity detected.": {

        "severity": "Medium",

        "explanation":
        "Microsoft Clarity captures user interactions to help website owners improve their sites.",

        "recommendation":
        "Use browser privacy controls if you prefer to minimize behavioral tracking."

    }

}


def explain(risks):

    explanations = []

    for risk in risks:

        if risk in EXPLANATIONS:

            info = EXPLANATIONS[risk]

            explanations.append({

                "title": risk,

                "severity": info["severity"],

                "explanation": info["explanation"],

                "recommendation": info["recommendation"]

            })

    return explanations
