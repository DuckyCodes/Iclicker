import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from setup import EMAIL, PASSWORD, CLASS_NAME, CLASS_URL, POLL_RATE, WAIT_JOIN

s = Service(r"C:\Users\Jing\Desktop\Projects\Auto-iClicker\src\chromedriver.exe")

driver = webdriver.Chrome(service=s)

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
max_retries = 10
retry_interval = 5
retries = 0

# Attempt to click the Join button with retries
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
while driver.current_url != CLASS_URL:
    if driver.current_url == 'https://student.iclicker.com/#/polling':
        clicked = False

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
                print("Click failed, retrying...")
                time.sleep(1)  # Wait before retrying
                print("Re-checking Multiple Choice A...")

    time.sleep(POLL_RATE)  # Wait before the next polling

# Cleanup
driver.quit()
