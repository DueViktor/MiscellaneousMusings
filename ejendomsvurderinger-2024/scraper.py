# Your existing xpaths
xpaths = {
    "adresse": "//*[@id='main']/section/div/div/h1/span[1]",
    "by_og_zip": "//*[@id='main']/section/div/div/h1/span[2]/span",
    "ejendomsværdi_2024": '//*[@id="main"]/section/div/div/div/div[2]/dl/div[1]/dd',
    "grundværdi_2024": '//*[@id="main"]/section/div/div/div/div[2]/dl/div[2]/dd',
    "ejendomsværdi_2022": '//*[@id="acc__body-accordion-0"]/div/div/div/div/div[2]/dd',
    "grundværdi_2022": '//*[@id="acc__body-accordion-0"]/div/div/div/div/div[3]/dd',
}
import csv
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By

path = "scraped_data.csv"
if Path(path).exists():
    existing_ids = set()
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        existing_ids = {int(row["property_id"]) for row in reader}
        print(f"already scraped: {existing_ids}")
else:
    existing_ids = set()

driver = webdriver.Chrome()

while True:

    property_id = 1

    if property_id in existing_ids:
        property_id += 1
        continue

    # URL to scrape
    url = f"https://www.vurderingsportalen.dk/ejerbolig/vurdering/foreloebige-vurderinger-ejendomssoegning/?id={property_id}"

    # Open the page
    driver.get(url)

    # Wait for page to load (adjust time if necessary)
    time.sleep(2)

    try:
        # Check if cookie button exists and is visible
        xpath_cookie_button = '//*[@id="declineButton"]'
        cookie_button = driver.find_element(By.XPATH, xpath_cookie_button)
        if cookie_button.is_displayed():
            cookie_button.click()
            time.sleep(2)
    except Exception:
        print("No cookie button found or already accepted")

    try:
        # expand this button
        xpath_expand_button = '//*[@id="acc__item-accordion-0"]'
        expand_button = driver.find_element(By.XPATH, xpath_expand_button)
        expand_button.click()
    except Exception as e:
        print("No expand button", e)

    time.sleep(2)

    result = {"property_id": property_id}

    for k, v in xpaths.items():

        try:
            element_1 = driver.find_element(By.XPATH, v)
            result[k] = element_1.text
        except Exception as e:
            print("An error occurred:", e)

    if property_id % 2:
        # save to csv
        import csv
        import os

        # Create or append to CSV file
        csv_file = "scraped_data.csv"
        file_exists = os.path.isfile(csv_file)

        with open(csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=result.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(result)

    property_id += 1

    if property_id == 10:
        break

# Close the driver
driver.quit()
