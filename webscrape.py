from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # Open webpage
    url = "https://www.geeksforgeeks.org/git-introduction/"  # Change this URL
    driver.get(url)

    # Wait for page to load
    # time.sleep(3)  

    # Scroll down to load all dynamic content
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)  # Scroll to bottom
        time.sleep(2)  # Wait for content to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:  # Stop when no more content loads
            break
        last_height = new_height

    # Extract full page text
    page_text = driver.find_element(By.TAG_NAME, "body").text
    print("Full Page Content:\n", page_text)  # Printing first 2000 characters for readability

finally:
    driver.quit()
