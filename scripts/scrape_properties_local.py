import requests
from bs4 import BeautifulSoup

# Sample Redfin URL (change this to the one you're testing)
REDFIN_URL = 'https://www.redfin.com/IL/Chicago/1234-Main-St-60601/home/12345678'

def scrape_redfin():
    listings = []
    response = requests.get(REDFIN_URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Example: Scraping titles, prices, and links (update based on actual page structure)
        for listing in soup.find_all("a", class_="css-1lh0fy5"):  # Adjust class as needed
            title = listing.get_text(strip=True)  # Extract title text
            price = listing.find_previous("span", class_="css-1o6ppf9").get_text(strip=True) if listing.find_previous("span", class_="css-1o6ppf9") else "N/A"
            link = "https://www.redfin.com" + listing["href"] if "href" in listing.attrs else "N/A"
            listings.append(["Redfin", title, price, link])
    return listings

def save_to_csv(listings):
    import pandas as pd
    df = pd.DataFrame(listings, columns=["Source", "Title", "Price", "Link"])
    df.to_csv("property_listings.csv", index=False)

if __name__ == "__main__":
    listings = scrape_redfin()
    save_to_csv(listings)
    print("Scraping complete. CSV saved as property_listings.csv.")
