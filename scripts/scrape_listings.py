import requests
import csv
import time
from bs4 import BeautifulSoup

# Define the URLs to scrape
URLS = {
    "craigslist": "https://chicago.craigslist.org/search/rea",
    "zillow": "https://www.zillow.com/chicago-il/real-estate/",
    "redfin": "https://www.redfin.com/city/29470/IL/Chicago",
    "facebook_marketplace": "https://www.facebook.com/marketplace/chicago/propertyrentals"
}

HEADERS = {"User-Agent": "Mozilla/5.0"}

def scrape_craigslist():
    listings = []
    response = requests.get(URLS["craigslist"], headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        for listing in soup.find_all("li", class_="result-row"):
            title = listing.find("a", class_="result-title").text
            price = listing.find("span", class_="result-price").text if listing.find("span", class_="result-price") else "N/A"
            link = listing.find("a", class_="result-title")["href"]
            listings.append(["Craigslist", title, price, link])
    return listings

def scrape_zillow():
    listings = []
    response = requests.get(URLS["zillow"], headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        for listing in soup.find_all("article"):
            title = listing.find("address").text if listing.find("address") else "N/A"
            price = listing.find("span", class_="list-card-price").text if listing.find("span", class_="list-card-price") else "N/A"
            link = listing.find("a", class_="list-card-link")["href"] if listing.find("a", class_="list-card-link") else "N/A"
            listings.append(["Zillow", title, price, f"https://www.zillow.com{link}"])
    return listings

def scrape_redfin():
    listings = []
    response = requests.get(URLS["redfin"], headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        for listing in soup.find_all("div", class_="HomeCardContainer"):
            title = listing.find("span", class_="homeAddress").text if listing.find("span", class_="homeAddress") else "N/A"
            price = listing.find("span", class_="homePrice").text if listing.find("span", class_="homePrice") else "N/A"
            link = listing.find("a", class_="cover-all")["href"] if listing.find("a", class_="cover-all") else "N/A"
            listings.append(["Redfin", title, price, f"https://www.redfin.com{link}"])
    return listings

def scrape_facebook_marketplace():
    listings = []
    print("Facebook Marketplace scraping requires manual authentication and a headless browser.")
    return listings

def save_to_csv(data, filename="property_listings.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Source", "Title", "Price", "Link"])
        writer.writerows(data)

def main():
    all_listings = []
    print("Scraping Craigslist...")
    all_listings.extend(scrape_craigslist())

    print("Scraping Zillow...")
    time.sleep(2)
    all_listings.extend(scrape_zillow())

    print("Scraping Redfin...")
    time.sleep(2)
    all_listings.extend(scrape_redfin())

    print("Scraping Facebook Marketplace...")
    all_listings.extend(scrape_facebook_marketplace())

    save_to_csv(all_listings)
    print("Scraping complete. Data saved to property_listings.csv")

if __name__ == "__main__":
    main()
