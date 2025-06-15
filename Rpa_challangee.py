import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load data
data = pd.read_excel("challenge.xlsx")
data.columns = [col.strip() for col in data.columns]

# Setup WebDriver options
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
# options.add_argument("--headless=new")  # Optional for speed

driver = webdriver.Chrome(options=options)
driver.get("https://rpachallenge.com")

# Start the challenge
try:
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.TAG_NAME, "button"))
    ).click()
except Exception as e:
    print(f"❌ Failed to start challenge: {e}")
    driver.quit()
    exit()

# Pre-cache XPath expressions for fields
field_xpaths = {
    field: f"//label[contains(text(), '{field}')]/following-sibling::input"
    for field in data.columns
}

# Main form-filling loop
for index, row in data.iterrows():
    for field, xpath in field_xpaths.items():
        try:
            input_element = driver.find_element(By.XPATH, xpath)
            input_element.clear()
            input_element.send_keys(str(row[field]))
        except Exception as e:
            print(f"❌ Field '{field}' failed at row {index + 1}: {e}")

    try:
        driver.find_element(By.XPATH, "//input[@type='submit']").click()
    except Exception as e:
        print(f"❌ Submit failed at row {index + 1}: {e}")

print("\n✅ Challenge completed.")
time.sleep(3)  # Reduce this if needed
driver.quit()
