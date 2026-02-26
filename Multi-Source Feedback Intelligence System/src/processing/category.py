KEYWORD_MAP = {
    "Bug": ["crash", "error", "bug", "issue", "broken"],
    "Performance": ["slow", "lag", "freeze"],
    "Pricing": ["price", "cost", "expensive", "refund", "charge"],
    "UI": ["interface", "design", "layout"],
    "Feature": ["feature", "add", "request"],
}

# Deterministic keyword-based categorization. Returns a single category.
def categorize_text(text: str) -> str:
  
    if not text:
        return "Other"

    text_lower = text.lower()

    for category, keywords in KEYWORD_MAP.items():
        for keyword in keywords:
            if keyword in text_lower:
                return category

    return "Other"