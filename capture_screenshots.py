import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

os.makedirs("report_screenshots", exist_ok=True)

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1440,1100")
options.add_argument("--user-data-dir=/tmp/chrome_report_profile")

driver = webdriver.Chrome(options=options)

try:
    print("Navigating to http://localhost:8501 ...")
    driver.get("http://localhost:8501")
    time.sleep(4)

    # 1. Initial dashboard
    driver.save_screenshot("report_screenshots/01_dashboard_metrics.png")
    print("Saved 01_dashboard_metrics.png")

    # 2. Click Generate Optimized Timetable button
    print("Clicking Generate...")
    btn = driver.find_element(By.XPATH, "//button[contains(., 'Generate')]")
    btn.click()
    time.sleep(7)

    # 3. Weekly Timetable view
    driver.save_screenshot("report_screenshots/02_weekly_timetable.png")
    print("Saved 02_weekly_timetable.png")

    # 4. Click 'AI Analysis' tab
    analysis_tab = driver.find_element(By.XPATH, "//p[contains(text(), 'AI Analysis')]")
    analysis_tab.click()
    time.sleep(4)
    driver.save_screenshot("report_screenshots/03_ai_analysis.png")
    print("Saved 03_ai_analysis.png")

    # 5. Click 'Algorithm Comparison' tab
    comp_tab = driver.find_element(By.XPATH, "//p[contains(text(), 'Algorithm Comparison')]")
    comp_tab.click()
    time.sleep(4)
    driver.save_screenshot("report_screenshots/04_algorithm_comparison.png")
    print("Saved 04_algorithm_comparison.png")

finally:
    driver.quit()
    print("Done capturing screenshots.")
