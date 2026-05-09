blocked_terms = [
    "legal advice",
    "legal hiring advice",
    "salary negotiation",
    "politics",
    "hack",
    "jailbreak",
    "ignore previous instructions",
    "bypass"
]

def is_blocked(text):

    text = text.lower()

    for term in blocked_terms:

        if term in text:
            return True

    return False