import os
import time
import json
import logging
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# Logging setup (professional)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def scrape_state(state_name: str, save_folder: str, age_min: int, age_max: int):
    """
    NamUs Missing Persons Scraper (Educational OSINT Automation)

    Scrapes publicly available missing persons listings from NamUs
    filtered by:
    - State
    - Age Range

    Saves:
    - Structured JSON results
    - Downloaded case images
    """

    url = "https://namus.gov/MissingPersons/Search"

    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    wait = WebDriverWait(driver, 20)
    results = []

    try:
        logging.info("Opening NamUs search page...")
        driver.get(url)

        # Open Circumstances tab
        wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Circumstances']"))
        ).click()

        # Select State
        logging.info(f"Applying state filter: {state_name}")
        state_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//label[text()='State']/following-sibling::div//input")
            )
        )
        state_input.send_keys(state_name)
        time.sleep(1)
        state_input.send_keys(Keys.ENTER)

        # Open Demographics tab
        driver.find_element(By.XPATH, "//span[text()='Demographics']").click()

        # Apply Age Range
        logging.info(f"Filtering ages between {age_min} and {age_max}")
        between_dropdown = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//label[contains(text(),'Age')]/following::select[1]")
            )
        )
        between_dropdown.send_keys("Between")

        driver.find_element(By.XPATH, "//input[@aria-label='Age From']").send_keys(str(age_min))
        driver.find_element(By.XPATH, "//input[@aria-label='Age To']").send_keys(str(age_max))

        # Click Search
        driver.find_element(By.XPATH, "//button[.='Search']").click()
        time.sleep(5)

        # Output folders
        os.makedirs(save_folder, exist_ok=True)
        images_folder = os.path.join(save_folder, f"{state_name}_images")
        os.makedirs(images_folder, exist_ok=True)

        page = 1
        result_index = 1

        # Scrape pagination
        while True:
            logging.info(f"Scraping page {page}...")

            soup = BeautifulSoup(driver.page_source, "html.parser")
            cards = soup.find_all("div", class_="card-body")

            if not cards:
                break

            for card in cards:
                text = card.get_text(" ", strip=True)

                entry = {
                    "result_number": result_index,
                    "state": state_name,
                    "raw_text": text
                }

                # Download image if available
                img_tag = card.find("img")
                if img_tag and "src" in img_tag.attrs:
                    img_url = urljoin(url, img_tag["src"])
                    img_path = os.path.join(images_folder, f"case_{result_index}.jpg")

                    try:
                        img_data = requests.get(img_url, timeout=10).content
                        with open(img_path, "wb") as img_file:
                            img_file.write(img_data)

                        entry["image_file"] = img_path
                    except Exception:
                        entry["image_file"] = None

                results.append(entry)
                result_index += 1

            # Next page
            try:
                next_button = driver.find_element(By.XPATH, "//a[@aria-label='Next']")
                if "disabled" in next_button.get_attribute("class"):
                    break
                next_button.click()
                time.sleep(4)
                page += 1
            except:
                break

        # Save JSON output
        json_path = os.path.join(save_folder, f"{state_name}_results.json")
        with open(json_path, "w", encoding="utf-8") as jf:
            json.dump(results, jf, indent=4)

        logging.info(f"Saved {len(results)} results to {json_path}")
        logging.info(f"Images saved in {images_folder}")

    except Exception as e:
        logging.error(f"Scraping failed: {e}")

    finally:
        driver.quit()
