import csv
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By


def merge_worker_csvs():
    """Merge and delete the worker files"""
    combined_csv_file = "scraped_data.csv"
    for infile in Path(".").iterdir():
        if infile.stem.startswith("scraped_data_worker"):
            if not Path(combined_csv_file).exists():
                with open(infile, "r", encoding="utf-8") as source, open(
                    combined_csv_file, "w", encoding="utf-8"
                ) as target:
                    target.write(source.read())
            else:
                with open(infile, "r", encoding="utf-8") as source:
                    next(source)  # Skip header
                    with open(combined_csv_file, "a", encoding="utf-8") as target:
                        target.write(source.read())
            infile.unlink()


merge_worker_csvs()


xpaths = {
    "adresse": "//*[@id='main']/section/div/div/h1/span[1]",
    "by_og_zip": "//*[@id='main']/section/div/div/h1/span[2]/span",
    "ejendomsværdi_2024": '//*[@id="main"]/section/div/div/div/div[2]/dl/div[1]/dd',
    "grundværdi_2024": '//*[@id="main"]/section/div/div/div/div[2]/dl/div[2]/dd',
    "ejendomsværdi_2022": '//*[@id="acc__body-accordion-0"]/div/div/div/div/div[2]/dd',
    "grundværdi_2022": '//*[@id="acc__body-accordion-0"]/div/div/div/div/div[3]/dd',
}

combined_csv_file = "scraped_data.csv"
existing_ids = set()
if Path(combined_csv_file).exists():
    with open(combined_csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        existing_ids = {int(row["property_id"]) for row in reader}
    print(f"Already scraped: {existing_ids}")


def scrape_property(driver, property_id, worker_id):
    if property_id in existing_ids:
        print(f"Skipping property_id {property_id}, already scraped.")
        return

    url = f"https://www.vurderingsportalen.dk/ejerbolig/vurdering/foreloebige-vurderinger-ejendomssoegning/?id={property_id}"
    worker_csv_file = f"scraped_data_worker_{worker_id}.csv"

    try:
        driver.get(url)
        time.sleep(2)

        try:
            xpath_cookie_button = '//*[@id="declineButton"]'
            cookie_button = driver.find_element(By.XPATH, xpath_cookie_button)
            if cookie_button.is_displayed():
                cookie_button.click()
                time.sleep(2)
        except Exception:
            print(f"No cookie button for property_id {property_id} or already accepted")

        try:
            xpath_expand_button = '//*[@id="acc__item-accordion-0"]'
            expand_button = driver.find_element(By.XPATH, xpath_expand_button)
            expand_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"No expand button for property_id {property_id}: {e}")

        result = {"property_id": property_id}
        for key, xpath in xpaths.items():
            try:
                element = driver.find_element(By.XPATH, xpath)
                result[key] = element.text
            except Exception:
                result[key] = None
                print(f"Error retrieving {key} for property_id {property_id}")

        file_exists = Path(worker_csv_file).is_file()
        with open(worker_csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=result.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(result)
        print(f"Successfully scraped property_id {property_id} for worker {worker_id}")

    except Exception as e:
        print(f"Error processing property_id {property_id}: {e}")


def scrape_list_of_ids(properties: List[int], worker_id):
    driver = webdriver.Chrome()
    try:
        for property_id in properties:
            scrape_property(driver, property_id, worker_id)
    finally:
        driver.quit()


N = 15
property_ids_to_scrape = range(1, 10000)
property_ids_to_scrape = list(set(property_ids_to_scrape) - existing_ids)

chunk_size = (len(property_ids_to_scrape) + N - 1) // N
chunks = [
    property_ids_to_scrape[i : i + chunk_size]
    for i in range(0, len(property_ids_to_scrape), chunk_size)
]

with ThreadPoolExecutor(max_workers=N) as executor:
    futures = [
        executor.submit(scrape_list_of_ids, chunk, i % N)
        for i, chunk in enumerate(chunks)
    ]

merge_worker_csvs()
