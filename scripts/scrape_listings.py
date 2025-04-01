import requests
import csv
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
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
    """ Uses Selenium to scrape Zillow real estate listings. """
    listings = []
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (no UI)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(URLS["zillow"])
    time.sleep(5)  # Allow JavaScript to load the page

    homes = driver.find_elements(By.CSS_SELECTOR, "li.ListItem-c11n-8-84-3")  # Update if necessary
    for home in homes[:20]:  # Limit to 20 listings
        try:
            title = home.find_element(By.CSS_SELECTOR, "address").text
            price = home.find_element(By.CSS_SELECTOR, "span[data-test='property-card-price']").text
            link = home.find_element(By.TAG_NAME, "a").get_attribute("href")
            listings.append(["Zillow", title, price, link])
        except:
            continue

    driver.quit()
    return listings


def scrape_redfin():
    """ Uses Selenium to scrape Redfin real estate listings. """
    listings = []
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(URLS["redfin"])
    time.sleep(5)  # Allow JavaScript to load

    homes = driver.find_elements(By.CSS_SELECTOR, "div.HomeCardContainer")
    for home in homes[:20]:  # Limit to 20 listings
        try:
            title = home.find_element(By.CSS_SELECTOR, "div.address").text
            price = home.find_element(By.CSS_SELECTOR, "span.price").text
            link = home.find_element(By.TAG_NAME, "a").get_attribute("href")
            listings.append(["Redfin", title, price, link])
        except:
            continue

    driver.quit()
    return listings


def scrape_facebook_marketplace():
    """ Facebook Marketplace requires login. Recommend manual scraping with Selenium. """
    print("Facebook Marketplace scraping requires login and manual browsing.")
    return []


def save_to_csv(data, filename="property_listings.csv"):
    df = pd.DataFrame(data, columns=["Source", "Title", "Price", "Link"])
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"Scraping complete. Data saved to {filename}")


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
    print("Scraping complete.")

if __name__ == "__main__":
    main()
