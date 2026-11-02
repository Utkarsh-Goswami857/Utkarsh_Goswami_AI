from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1400,1000")
options.add_argument("--user-data-dir=/tmp/chrome_report_profile")
driver = webdriver.Chrome(options=options)
driver.get("http://localhost:8501")
time.sleep(3)

# click generate button
btn = driver.find_element(By.XPATH, "//button[contains(., 'Generate')]")
btn.click()
time.sleep(6)

elems = driver.find_elements(By.XPATH, "//*[contains(text(), 'Analysis') or contains(text(), 'Weekly Timetable') or contains(text(), 'Algorithm Comparison')]")
for e in elems:
    print("Tag:", e.tag_name, "| Class:", e.get_attribute("class"), "| Role:", e.get_attribute("role"), "| Text:", e.text)

driver.quit()
