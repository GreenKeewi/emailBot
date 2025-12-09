"""
Business categories configuration.
Edit this file to customize the categories to search for.
"""

CATEGORIES = [
    "plumbers",
    "dentists",
    "electricians",
    "roofers",
    "HVAC contractors",
    "lawyers",
    "accountants",
    "real estate agents",
    "insurance agents",
    "financial advisors",
    "chiropractors",
    "veterinarians",
    "auto repair shops",
    "landscaping services",
    "cleaning services",
    "general contractors",
    "painters",
    "carpet cleaners",
    "pest control services",
    "locksmiths",
]

def get_categories():
    """Return the list of business categories to search."""
    return CATEGORIES

def add_category(category):
    """Add a new category to the list."""
    if category not in CATEGORIES:
        CATEGORIES.append(category)
        return True
    return False

def remove_category(category):
    """Remove a category from the list."""
    if category in CATEGORIES:
        CATEGORIES.remove(category)
        return True
    return False
