"""
Configuration file for CT Local Business Lead & Email Scraper
"""

# Priority Locations
PRIORITY_TOWNS = [
    "Norwalk",
    "Wilton",
    "Darien"
]

# Secondary CT Towns (For expanded searches)
SECONDARY_TOWNS = [
    "Westport",
    "Fairfield",
    "Stratford",
    "Milford",
    "Ridgefield",
    "Danbury",
    "Bethel",
    "Trumbull",
    "Shelton",
    "Monroe"
]

# STRICT EXCLUDED TOWNS
EXCLUDED_TOWNS = [
    "Stamford",
    "New Canaan",
    "Greenwich"
]

# Target Business Query Categories
TARGET_SEARCH_TERMS = [
    "restaurant",
    "deli",
    "bakery",
    "cafe",
    "salon",
    "barbershop",
    "nail salon",
    "grocery",
    "laundromat",
    "dry cleaner",
    "auto repair",
    "food truck"
]

# Known Major National Chains & Franchises to Exclude
CHAIN_EXCLUSIONS = [
    "chipotle", "starbucks", "dunkin", "dunkin'", "subway", "mcdonald", "mcdonald's",
    "domino's", "dominos", "papa john", "pizza hut", "little caesars", "burger king",
    "wendy's", "taco bell", "panera", "five guys", "jersey mike's", "jimmy john's",
    "great clips", "supercuts", "sport clips", "hair cutteria", "cvs", "walgreens",
    "rite aid", "7-eleven", "wawa", "auto zone", "autozone", "advance auto", "pep boys",
    "meineke", "mavis", "jiffy lube", "midas", "firestone", "valvoline", "planet fitness",
    "massage envy", "t-mobile", "verizon", "att", "at&t", "chick-fil-a", "popeyes",
    "kfc", "sonic", "arby's", "dairy queen", "panda express", "sweetgreen", "cava"
]

# Web Request Configuration
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, Gecko) Chrome/122.0.0.0 Safari/537.36"
REQUEST_TIMEOUT = 10  # seconds
REQUEST_DELAY_MIN = 1.0  # seconds
REQUEST_DELAY_MAX = 2.0  # seconds

# Generic Email Providers to Flag (Needs Verification)
GENERIC_EMAIL_PROVIDERS = [
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com",
    "icloud.com", "comcast.net", "optimum.net", "sbcglobal.net"
]
