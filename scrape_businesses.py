import requests
import os
import pandas as pd
import re
from bs4 import BeautifulSoup

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

CATEGORIES = {
    "personal trainers": "Fitness Trainer",
    "photographers": "Photography Studio",
    "wedding planners": "Event Planning",
    "real estate agents": "Real Estate Agency",
    "home renovation contractors": "Home Improvement",
    "boutique marketing agencies": "Marketing Agency",
    "auto repair shops": "Auto Repair",
    "custom furniture makers": "Furniture Store",
    "caterers": "Catering Business",
    "local coffee shops": "Coffee Shop",
    "spa and wellness centers": "Spa & Wellness",
    "tattoo artists": "Tattoo Shop",
    "barbers": "Barber Shop",
    "restaurants": "Restaurant",
    "independent clothing brands": "Clothing Store"
}

HEADERS = {"User-Agent": "Mozilla/5.0"}

def extract_email_from_website(website_url):
    """Scrape email addresses from a website."""
    try:
        response = requests.get(website_url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", soup.text))
            return emails.pop() if emails else "N/A"
    except requests.exceptions.RequestException:
        pass
    return "N/A"

def fetch_businesses(category, business_type):
    """Fetch businesses from SerpApi."""
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_maps",
        "q": f"{category} in USA",
        "type": "search",
        "api_key": SERPAPI_KEY,
        "hl": "en",
        "num": 25
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    businesses = []
    if "local_results" in data:
        for result in data["local_results"][:25]:
            website = result.get("website", "N/A")
            businesses.append({
                "Business Name": result.get("title", "N/A"),
                "Business Type": business_type,
                "Website": website,
                "Phone Number": result.get("phone", "N/A"),
                "Address": result.get("address", "N/A"),
            })
    return businesses

def main():
    all_businesses = []
    for category, business_type in CATEGORIES.items():
        all_businesses.extend(fetch_businesses(category, business_type))

    # Now, scrape emails for businesses with a website
    for business in all_businesses:
        business["Email"] = extract_email_from_website(business["Website"]) if business["Website"] != "N/A" else "N/A"

    # Generate timestamped CSV filename
    timestamp = pd.Timestamp.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"businesses_{timestamp}.csv"

    df = pd.DataFrame(all_businesses)
    df.to_csv(filename, index=False)
    print(f"CSV file '{filename}' generated successfully!")

if __name__ == "__main__":
    main()
