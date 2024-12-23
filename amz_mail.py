from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def web_driver():
    options = Options()
    options.add_argument("--verbose")
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1920,1200")
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Initialize WebDriver
driver = web_driver()

# Default values for product details
product_name = "N/A"
price = "N/A"
url = "https://amzn.in/d/2atlNqL"

try:
    # Navigate to the URL
    driver.get(url)

    # Wait at least 1 minute for the page to fully load
    time.sleep(60)

    # Log the page source for debugging
    print("Page source after 60 seconds:")
    print(driver.page_source)

    # Scrape product details
    product_name = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "span#productTitle"))
    ).text.strip()

    price = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".a-price-whole"))
    ).text.strip()

    print(f"Product: {product_name}")
    print(f"Price: {price}")

except Exception as e:
    # Log the error and handle missing data gracefully
    print(f"An error occurred while scraping: {e}")

finally:
    # Close the browser
    driver.quit()

# Email configuration using environment variables
sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_PASSWORD")
receiver_email = os.getenv("RECEIVER_EMAIL")

if not sender_email or not sender_password or not receiver_email:
    raise ValueError("Email credentials not found in environment variables.")

# Prepare the email content
subject = "Amazon Product Details"
body = f"Product: {product_name}\nPrice: {price}\nDate and Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nLink: {url}"

# Create the email
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))

# Send the email
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Error sending email: {e}")
