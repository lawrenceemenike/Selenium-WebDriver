from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
import time

# Replace with your actual LinkedIn credentials
EMAIL = "clen.gmail.com"
PASSWORD = "M6"

# Job search URL
JOB_SEARCH_URL = "https://www.linkedin.com/jobs/search/?f_LF=f_AL&geoId=102257491&keywords=python%20developer&location=London%2C%20England%2C%20United%20Kingdom&redirect=false&position=1&pageNum=0"

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Initialize the webdriver
driver = webdriver.Chrome(options=chrome_options)

def wait_and_click(by, value, timeout=10):
    element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))
    element.click()

try:
    # Open LinkedIn
    driver.get("https://www.linkedin.com")
    print("Opened LinkedIn")

    # Reject cookies if the button is present
    try:
        wait_and_click(By.CSS_SELECTOR, 'button[action-type="DENY"]')
        print("Rejected cookies")
    except TimeoutException:
        print("No cookie rejection needed")

    # Click Sign in Button
    wait_and_click(By.LINK_TEXT, "Sign in")
    print("Clicked Sign in button")

    # Sign in
    email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
    email_field.send_keys(EMAIL)
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(PASSWORD)
    password_field.send_keys(Keys.ENTER)
    print("Entered login credentials")

    # Wait for potential CAPTCHA
    input("Press Enter when you have solved the Captcha (if presented)")

    # Navigate to the job search URL
    driver.get(JOB_SEARCH_URL)
    print("Navigated to job search page")

    # Wait for job listings to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "job-card-container")))

    # Click on the first job listing
    first_job = driver.find_element(By.CLASS_NAME, "job-card-container")
    first_job.click()
    print("Clicked on first job listing")

    # Wait for the job details to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "jobs-save-button")))

    # Save the job
    save_button = driver.find_element(By.CLASS_NAME, "jobs-save-button")
    save_button.click()
    print("Saved the job")

    # Follow the company
    try:
        follow_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.follow"))
        )
        follow_button.click()
        print("Followed the company")
    except (TimeoutException, NoSuchElementException):
        print("Couldn't find follow button or already following the company")

except TimeoutException:
    print("Timeout occurred: Page took too long to load")
except NoSuchElementException as e:
    print(f"Element not found: {e}")
except ElementClickInterceptedException as e:
    print(f"Element click was intercepted: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

finally:
    # Keep the browser open
    input("Press Enter to close the browser...")
    driver.quit()
