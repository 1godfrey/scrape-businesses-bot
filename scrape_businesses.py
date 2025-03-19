import requests
import os
import pandas as pd

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

CATEGORIES = {
    "tattoo artists": "Tattoo Shop",
    "barbers": "Barber Shop",
    "restaurants": "Restaurant",
    "independent clothing brands": "Clothing Store"
}

def fetch_businesses(category, business_type):
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_maps",
        "q": category + " in USA",
        "type": "search",
        "api_key": SERPAPI_KEY,
        "hl": "en",
        "num": 10
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    businesses = []
    if "local_results" in data:
        for result in data["local_results"][:10]:
            businesses.append({
                "Business Name": result.get("title", "N/A"),
                "Business Type": business_type,
                "Email": result.get("email", "N/A"),
                "Phone Number": result.get("phone", "N/A"),
                "Link to website": result.get("website", "N/A"),
                "Address": result.get("address", "N/A"),
            })
    return businesses

def main():
    all_businesses = []
    for category, business_type in CATEGORIES.items():
        all_businesses.extend(fetch_businesses(category, business_type))

    df = pd.DataFrame(all_businesses)
    df.to_csv("businesses.csv", index=False)
    print("CSV file generated successfully!")

if __name__ == "__main__":
    main()
