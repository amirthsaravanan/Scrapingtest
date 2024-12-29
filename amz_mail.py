from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import random
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def web_driver():
    options = Options()
    options.add_argument("--headless=new")  # Updated headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--window-size=1920,1200")
    options.add_argument(
        f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    )
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Initialize WebDriver
driver = web_driver()

# Default values for product details
product_name = "N/A"
price = "N/A"
url = "https://pricehistoryapp.com/product/buyerzone-digital-smart-alarm-clock-for-students-heavy-sleepers-with-sensor-date-clock"

try:
    # Navigate to the URL with a random delay
    print("Navigating to the URL...")
    driver.get(url)
    time.sleep(random.uniform(10, 20))  # Random delay for human-like behavior

    # Log the page source for debugging
    print("Page source:")
    print(driver.page_source)
    
    
except Exception as e:
    # Log the error and handle missing data gracefully
    print(f"An error occurred while scraping: {e}")

finally:
    # Close the browser
    driver.quit()
