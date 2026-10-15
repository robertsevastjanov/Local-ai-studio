import json
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Launch Chrome.
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

try:
    # Open the Local AI Studio gallery.
    driver.get("http://127.0.0.1:3000")

    # Find the gallery heading.
    heading = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, "h1"))
    )
    # Show the actual heading text for debugging.
    print("Actual heading:", repr(heading.text))
    # Check that the heading contains the expected text.
    assert heading.text == "Create without limits."    
    print("PASS: Gallery heading is correct")
    # Wait until the gallery heading becomes visible.
    gallery_heading = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//h2[normalize-space()='Generation Gallery']")
        )
    )

    # Verify that the gallery section is displayed.
    assert gallery_heading.is_displayed()

    print("PASS: Generation Gallery is visible")
    # Wait for the generation counter to appear.
    generation_counter = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Images generated:')]")
        )
    )

    # Check that the counter contains a number.
    counter_text = generation_counter.text

    assert "Images generated:" in counter_text
    assert counter_text.split(":")[-1].strip().isdigit()

    print("PASS: Generation counter is visible:", counter_text)
    # Request the generation history from FastAPI.
    with urlopen("http://127.0.0.1:8000/history") as response:
        api_data = json.load(response)

    # Extract the generation counts.
    api_count = api_data["count"]
    frontend_count = int(counter_text.split(":")[-1].strip())

    # Compare the frontend counter with the backend response.
    assert frontend_count == api_count, (
        f"Count mismatch: frontend={frontend_count}, API={api_count}"
    )

    print(f"PASS: Frontend and API counts match ({api_count})")
    # Find all images inside the gallery.
    # Wait for images only when the API contains generations.
    if api_count > 0:
        WebDriverWait(driver, 10).until(
            lambda d: (
                len(d.find_elements(By.CSS_SELECTOR, "img"))
                + len(d.find_elements(
                    By.XPATH, "//*[normalize-space()='Image unavailable']"
                ))
            ) >= api_count
        )

    # Collect images after the gallery has finished rendering.
    images = driver.find_elements(By.CSS_SELECTOR, "img")

    # Count successfully loaded images.
    loaded_images = 0

    for image in images:
        # Check whether the browser loaded the image successfully.
        is_loaded = driver.execute_script(
            "return arguments[0].complete && arguments[0].naturalWidth > 0;",
            image
        )

        if is_loaded:
            loaded_images += 1

    print(f"Loaded images: {loaded_images} / {len(images)}")
    # Verify that every displayed image loaded successfully.
    assert loaded_images == len(images), (
        f"Some images failed to load: {loaded_images}/{len(images)}"
    )

    print("PASS: All displayed images loaded successfully")
    
finally:
    # Always close the browser, even if the test fails.
    driver.quit()