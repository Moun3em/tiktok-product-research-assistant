
import os
import time
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Set up Google Sheets API credentials
SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
CREDS = ServiceAccountCredentials.from_json_keyfile_name('path/to/your/credentials.json', SCOPES)
client = gspread.authorize(CREDS)
sheet = client.open("TikTok Product Research").sheet1

# Set up Selenium webdriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run Chrome in headless mode (without GUI)
driver = webdriver.Chrome(options=options)

# Log in to TikTok account
driver.get("https://www.tiktok.com/login")
# Add your TikTok login credentials here
username_field = driver.find_element(By.NAME, "username")
username_field.send_keys("your_tiktok_username")
password_field = driver.find_element(By.NAME, "password")
password_field.send_keys("your_tiktok_password")
password_field.send_keys(Keys.RETURN)

# Scroll through TikTok videos and save links to Google Sheet
video_count = 0
while video_count < 50:  # Adjust the target video count as needed
    driver.execute_script("window.scrollBy(0,500)")
    time.sleep(random.uniform(2, 5))  # Wait for videos to load
    
    videos = driver.find_elements(By.CSS_SELECTOR, "a.video-feed-item-wrapper")
    for video in videos:
        video_link = video.get_attribute("href")
        if video_link.startswith("https://www.tiktok.com/@") and video_link.endswith("/video/"):
            # Check if video meets your criteria (e.g., views, likes)
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(video_link)
            
            view_count = int(driver.find_element(By.CSS_SELECTOR, "strong.video-count").text.replace(",", ""))
            like_count = int(driver.find_element(By.CSS_SELECTOR, "strong.like-count").text.replace(",", ""))
            if view_count > 100000 and like_count > 10000:
                sheet.append_row([video_link])
                video_count += 1
            
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

driver.quit()
