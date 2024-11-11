import csv
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By


def merge_worker_csvs():
    """Merge and delete the files"""
    for infile in Path(".").iterdir():
        if infile.stem.startswith("scraped_data_worker"):
            # First file: copy headers and data
            if not Path("scraped_data.csv").exists():
                with open(infile, "r", encoding="utf-8") as source:
                    with open("scraped_data.csv", "w", encoding="utf-8") as target:
                        target.write(source.read())
            # Subsequent files: append data without headers
            else:
                with open(infile, "r", encoding="utf-8") as source:
                    next(source)  # Skip header
                    with open("scraped_data.csv", "a", encoding="utf-8") as target:
                        target.write(source.read())
            # Delete the worker file after merging
            infile.unlink()


# Define XPaths
xpaths = {
    "adresse": "//*[@id='main']/section/div/div/h1/span[1]",
    "by_og_zip": "//*[@id='main']/section/div/div/h1/span[2]/span",
    "ejendomsværdi_2024": '//*[@id="main"]/section/div/div/div/div[2]/dl/div[1]/dd',
    "grundværdi_2024": '//*[@id="main"]/section/div/div/div/div[2]/dl/div[2]/dd',
    "ejendomsværdi_2022": '//*[@id="acc__body-accordion-0"]/div/div/div/div/div[2]/dd',
    "grundværdi_2022": '//*[@id="acc__body-accordion-0"]/div/div/div/div/div[3]/dd',
}

# initial clean up

# Load existing property IDs if a combined CSV exists
combined_csv_file = "scraped_data.csv"
existing_ids = set()
if Path(combined_csv_file).exists():
    with open(combined_csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        existing_ids = {int(row["property_id"]) for row in reader}
    print(f"Already scraped: {existing_ids}")


# Define a scraping function for each property
def scrape_property(property_id, worker_id):
    # Skip if already scraped
    if property_id in existing_ids:
        print(f"Skipping property_id {property_id}, already scraped.")
        return

    # Initialize WebDriver
    driver = webdriver.Chrome()
    url = f"https://www.vurderingsportalen.dk/ejerbolig/vurdering/foreloebige-vurderinger-ejendomssoegning/?id={property_id}"
    worker_csv_file = (
        f"scraped_data_worker_{worker_id}.csv"  # Unique file for each worker
    )

    try:
        # Access URL and wait for the page to load
        driver.get(url)
        time.sleep(2)

        # Handle cookie acceptance
        try:
            xpath_cookie_button = '//*[@id="declineButton"]'
            cookie_button = driver.find_element(By.XPATH, xpath_cookie_button)
            if cookie_button.is_displayed():
                cookie_button.click()
                time.sleep(2)
        except Exception:
            print(f"No cookie button for property_id {property_id} or already accepted")

        # Expand additional content
        try:
            xpath_expand_button = '//*[@id="acc__item-accordion-0"]'
            expand_button = driver.find_element(By.XPATH, xpath_expand_button)
            expand_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"No expand button for property_id {property_id}:", e)

        # Scrape data
        result = {"property_id": property_id}
        for key, xpath in xpaths.items():
            try:
                element = driver.find_element(By.XPATH, xpath)
                result[key] = element.text
            except Exception as e:
                result[key] = None
                print(f"Error retrieving {key} for property_id {property_id}: {e}")

        # Write data to the worker's CSV file
        file_exists = Path(worker_csv_file).is_file()
        with open(worker_csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=result.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(result)
        print(f"Successfully scraped property_id {property_id} for worker {worker_id}")

    finally:
        driver.quit()


# Set the number of scrapers
N = 5  # Number of parallel scrapers
property_ids_to_scrape = range(1, 11)  # Adjust range as needed

# Use ThreadPoolExecutor to run scrapers in parallel
with ThreadPoolExecutor(max_workers=N) as executor:
    # Submit tasks with worker_id and property_id
    futures = [
        executor.submit(scrape_property, property_id, i % N)
        for i, property_id in enumerate(property_ids_to_scrape)
    ]

merge_worker_csvs()
