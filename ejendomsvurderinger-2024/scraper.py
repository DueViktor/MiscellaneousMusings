import csv
import os
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By

# Define XPaths
xpaths = {
    "adresse": "//*[@id='main']/section/div/div/h1/span[1]",
    "by_og_zip": "//*[@id='main']/section/div/div/h1/span[2]/span",
    "ejendomsværdi_2024": '//*[@id="main"]/section/div/div/div/div[2]/dl/div[1]/dd',
    "grundværdi_2024": '//*[@id="main"]/section/div/div/div/div[2]/dl/div[2]/dd',
    "ejendomsværdi_2022": '//*[@id="acc__body-accordion-0"]/div/div/div/div/div[2]/dd',
    "grundværdi_2022": '//*[@id="acc__body-accordion-0"]/div/div/div/div/div[3]/dd',
}

# File and path settings
csv_file = "scraped_data.csv"
path = Path(csv_file)

# Check if CSV exists and load existing property IDs
existing_ids = set()
if path.exists():
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        existing_ids = {int(row["property_id"]) for row in reader}
    print(f"Already scraped: {existing_ids}")

# Initialize WebDriver
driver = webdriver.Chrome()

try:
    property_id = 1
    while property_id < 20:  # Scrape up to property_id 10 for this run

        # Skip already scraped property IDs
        if property_id in existing_ids:
            property_id += 1
            continue

        # Access URL
        url = f"https://www.vurderingsportalen.dk/ejerbolig/vurdering/foreloebige-vurderinger-ejendomssoegning/?id={property_id}"
        driver.get(url)
        time.sleep(2)  # Wait for page load

        # Handle cookie acceptance
        try:
            xpath_cookie_button = '//*[@id="declineButton"]'
            cookie_button = driver.find_element(By.XPATH, xpath_cookie_button)
            if cookie_button.is_displayed():
                cookie_button.click()
                time.sleep(2)
        except Exception:
            print("No cookie button found or already accepted")

        # Expand additional content
        try:
            xpath_expand_button = '//*[@id="acc__item-accordion-0"]'
            expand_button = driver.find_element(By.XPATH, xpath_expand_button)
            expand_button.click()
            time.sleep(2)
        except Exception as e:
            print("No expand button found:", e)

        # Scrape data
        result = {"property_id": property_id}
        for key, xpath in xpaths.items():
            try:
                element = driver.find_element(By.XPATH, xpath)
                result[key] = element.text
            except Exception as e:
                result[key] = None
                print(f"Error retrieving {key}: {e}")

        # Save data every other property
        file_exists = os.path.isfile(csv_file)
        with open(csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=result.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(result)

        property_id += 1

finally:
    driver.quit()
