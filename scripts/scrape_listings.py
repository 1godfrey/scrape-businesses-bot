import requests
import csv
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Define the URLs to scrape
URLS = {
    "craigslist": "https://chicago.craigslist.org/search/rea",
    "zillow": "https://www.zillow.com/chicago-il/real-estate/",
    "redfin": "https://www.redfin.com/city/29470/IL/Chicago",
    "facebook_marketplace": "https://www.facebook.com/marketplace/chicago/propertyrentals"
}

HEADERS = {"User-Agent": "Mozilla/5.0"}

def scrape_craigslist():
    """Scrapes Craigslist listings."""
    print("Starting Craigslist scraping...")
    listings = []
    response = requests.get(URLS["craigslist"], headers=HEADERS)
    
    if response.status_code != 200:
        print(f"Failed to access Craigslist. Status Code: {response.status_code}")
        return []

    print("Craigslist page fetched successfully!")
    soup = BeautifulSoup(response.text, "html.parser")

    results = soup.find_all("li", class_="result-row")
    print(f"Found {len(results)} listings on Craigslist.")

    for listing in results:
        try:
            title = listing.find("a", class_="result-title").text
            price = listing.find("span", class_="result-price").text if listing.find("span", class_="result-price") else "N/A"
            link = listing.find("a", class_="result-title")["href"]
            print(f"Craigslist Listing: {title} | {price} | {link}")
            listings.append(["Craigslist", title, price, link])
        except Exception as e:
            print(f"Error processing a Craigslist listing: {e}")

    return listings


def scrape_zillow():
    """ Uses Selenium to scrape Zillow real estate listings. """
    print("Starting Zillow scraping...")
    listings = []

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(URLS["zillow"])
    time.sleep(5)  

    homes = driver.find_elements(By.CSS_SELECTOR, "li.ListItem-c11n-8-84-3")
    print(f"Found {len(homes)} Zillow listings.")

    for i, home in enumerate(homes[:20]):
        try:
            title = home.find_element(By.CSS_SELECTOR, "address").text if home.find_elements(By.CSS_SELECTOR, "address") else "N/A"
            price = home.find_element(By.CSS_SELECTOR, "span[data-test='property-card-price']").text if home.find_elements(By.CSS_SELECTOR, "span[data-test='property-card-price']") else "N/A"
            link = home.find_element(By.TAG_NAME, "a").get_attribute("href") if home.find_elements(By.TAG_NAME, "a") else "N/A"
            print(f"Zillow Listing #{i+1}: {title} | {price} | {link}")
            listings.append(["Zillow", title, price, link])
        except NoSuchElementException as e:
            print(f"Zillow listing error: {e}")

    driver.quit()
    return listings


def scrape_redfin():
    """ Uses Selenium to scrape Redfin real estate listings. """
    print("Starting Redfin scraping...")
    listings = []

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(URLS["redfin"])
    time.sleep(5)

    homes = driver.find_elements(By.CSS_SELECTOR, "div.HomeCardContainer")
    print(f"Found {len(homes)} Redfin listings.")

    for i, home in enumerate(homes[:20]):  
        try:
            title = home.find_element(By.CSS_SELECTOR, "div.address").text if home.find_elements(By.CSS_SELECTOR, "div.address") else "N/A"
            price = home.find_element(By.CSS_SELECTOR, "span.price").text if home.find_elements(By.CSS_SELECTOR, "span.price") else "N/A"
            link = home.find_element(By.TAG_NAME, "a").get_attribute("href") if home.find_elements(By.TAG_NAME, "a") else "N/A"
            print(f"Redfin Listing #{i+1}: {title} | {price} | {link}")
            listings.append(["Redfin", title, price, link])
        except NoSuchElementException as e:
            print(f"Redfin listing error: {e}")

    driver.quit()
    return listings


def scrape_facebook_marketplace():
    """ Facebook Marketplace requires login. Recommend manual scraping with Selenium. """
    print("Facebook Marketplace scraping requires login and manual browsing.")
    return []


def save_to_csv(data, filename="property_listings.csv"):
    """Saves listings to a CSV file."""
    if not data:
        print("No listings were found. Skipping CSV save.")
        return

    df = pd.DataFrame(data, columns=["Source", "Title", "Price", "Link"])
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"Scraping complete. Data saved to {filename}")


def main():
    """Main function to execute all scraping jobs."""
    all_listings = []

    print("\n=== Scraping Craigslist ===")
    craigslist_data = scrape_craigslist()
    print(f"Craigslist Scraped: {len(craigslist_data)} listings found.")
    all_listings.extend(craigslist_data)

    print("\n=== Scraping Zillow ===")
    time.sleep(2)
    zillow_data = scrape_zillow()
    print(f"Zillow Scraped: {len(zillow_data)} listings found.")
    all_listings.extend(zillow_data)

    print("\n=== Scraping Redfin ===")
    time.sleep(2)
    redfin_data = scrape_redfin()
    print(f"Redfin Scraped: {len(redfin_data)} listings found.")
    all_listings.extend(redfin_data)

    print("\n=== Scraping Facebook Marketplace ===")
    facebook_data = scrape_facebook_marketplace()
    print(f"Facebook Marketplace Scraped: {len(facebook_data)} listings found.")
    all_listings.extend(facebook_data)

    save_to_csv(all_listings)
    print("\nScraping complete.")

if __name__ == "__main__":
    main()
