import json
import os
from urllib.request import urlopen

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

try:
    url = (
        "http://127.0.0.1:3000"
        if os.getenv("CI")
        else "http://[::1]:3000"
    )

    driver.get(url)

    heading = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, "h1"))
    )

    assert heading.text == "Create without limits."
    print("PASS: Homepage heading")

    gallery = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//h2[normalize-space()='Generation Gallery']"
        ))
    )

    assert gallery.is_displayed()
    print("PASS: Generation Gallery")

    with urlopen("http://127.0.0.1:8000/history") as response:
        api_count = json.load(response)["count"]

    def counter_matches_api(d):
        elements = d.find_elements(
            By.XPATH,
            "//*[contains(text(), 'Images generated:')]"
        )
        return any(
            element.text.strip() == f"Images generated: {api_count}"
            for element in elements
        )

    WebDriverWait(driver, 10).until(counter_matches_api)

    print(f"PASS: Gallery counter matches API ({api_count})")
    print("SUCCESS: Selenium smoke test passed!")

finally:
    driver.quit()