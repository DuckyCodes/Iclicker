import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from setup import EMAIL, PASSWORD, CLASS_NAME, CLASS_URL, POLL_RATE, WAIT_JOIN

import os
from selenium import webdriver


current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the chromedriver
driver_path = os.path.join(current_dir, 'chromedriver')

# Create a Service object with the path to the ChromeDriver
service = Service(driver_path)

# Initialize the Chrome WebDriver with the Service object
driver = webdriver.Chrome(service=service)

# Log in to iClicker
driver.get('https://student.iclicker.com/#/login')

# Enter email
search = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.ID, "input-email"))
)
search.send_keys(EMAIL)
search.submit()

# Enter password
search = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "input-password"))
)
search.send_keys(PASSWORD)
search.submit()

# Click sign-in button
search = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "sign-in-button"))
)
search.click()

# Click on the class name
search = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[text()="'+CLASS_NAME+'"]'))
)
search.click()

# Attempt to find and click the Join button
button_found = False
retry_interval = 5
retries = 0

# Attempt to click the Join button with indefinite retries
while not button_found:
    try:
        search = WebDriverWait(driver, WAIT_JOIN).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="btnJoin"]'))
        )
        search.click()
        button_found = True  # Button clicked successfully
        print("Clicked Join button.")
    except Exception as e:
        print("Join button not found, retrying...")
        retries += 1
        time.sleep(retry_interval)

# Delay before polling
time.sleep(7)

# Polling loop for multiple choice A
previous_poll_detected = False  # Track if we detected a previous poll

while True:
    print("While loop working")
    print(f"Current URL: {driver.current_url}")
    # Check if the current URL is for a poll
    if '/poll' in driver.current_url:
        if not previous_poll_detected:  # If we haven't handled a poll yet
            clicked = False
            print("Poll URL detected, entering retry loop for Multiple Choice A")

            # Indefinite retry loop until clicked
            while not clicked:
                try:
                    # Wait for the option to be clickable
                    multiple_choice_a = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, 'multiple-choice-a'))
                    )
                    multiple_choice_a.click()  # Attempt to click using Selenium
                    clicked = True  # Mark as clicked if successful
                    print("Clicked on Multiple Choice A.")
                except Exception as e:
                    print(f"Click failed: {e}, retrying...")
                    time.sleep(1)  # Wait before retrying
                    print("Re-checking Multiple Choice A...")

            previous_poll_detected = True  # Mark that we've handled this poll
        else:
            print("Already handled the current poll, waiting for a new one...")
    else:
        previous_poll_detected = False  # Reset if not on a poll page

    time.sleep(POLL_RATE)  # Wait before the next check


print("Ended")

# Cleanup
driver.quit()