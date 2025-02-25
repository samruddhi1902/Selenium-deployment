import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Function to scrape the webpage
def scrape_website(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run without UI
    chrome_options.add_argument("--no-sandbox")  # Required for Streamlit Cloud
    chrome_options.add_argument("--disable-dev-shm-usage")  # Prevent resource issues
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        time.sleep(5)  # Allow time for page to load

        # Scroll to the bottom to load dynamic content
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Extract full page text safely
        body_element = driver.find_element(By.TAG_NAME, "body")
        if body_element:
            page_text = body_element.text.strip()  # Ensuring no NoneType error
        else:
            page_text = "⚠️ Could not find the page body. The website may have blocked automation."

    except Exception as e:
        page_text = f"❌ Error: {e}"

    finally:
        driver.quit()

    return page_text if page_text else "⚠️ No content extracted. Try another website."

# Streamlit UI
st.title("🔍 Web Scraper with Selenium")
st.write("Enter a URL to scrape its visible content.")

# Input field for URL
url = st.text_input("Enter URL:", "https://www.geeksforgeeks.org/git-introduction/")

# Scrape button
if st.button("Scrape"):
    with st.spinner("Scraping... Please wait ⏳"):
        content = scrape_website(url)

    if content:
        st.success("Scraping completed! 🎉")
        st.text_area("Scraped Data", content, height=400)
    else:
        st.error("⚠️ Failed to extract content. Try a different website!")
