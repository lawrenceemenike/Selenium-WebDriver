from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class InternetSpeedTwitterBot:
    def __init__(self, promised_down, promised_up, twitter_email, twitter_password):
        self.driver = webdriver.Chrome()
        self.promised_down = promised_down
        self.promised_up = promised_up
        self.twitter_email = twitter_email
        self.twitter_password = twitter_password
        self.up = 0
        self.down = 0

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        try:
            # Wait for and handle the cookie popup
            cookie_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            cookie_button.click()

            # Now wait for and click the speed test button
            go_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".start-button a"))
            )
            go_button.click()

            # Wait for test to complete and results to display
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".result-data-large.number.result-data-value.download-speed"))
            )

            self.down = self.driver.find_element(By.CSS_SELECTOR, ".result-data-large.number.result-data-value.download-speed").text
            self.up = self.driver.find_element(By.CSS_SELECTOR, ".result-data-large.number.result-data-value.upload-speed").text
        except TimeoutException:
            print("Timed out waiting for speed test results")
        except NoSuchElementException:
            print("Could not find expected elements on the page")

    def tweet_at_provider(self):
        self.driver.get("https://twitter.com/login")
        try:
            email = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@autocomplete="username"]'))
            )
            email.send_keys(self.twitter_email)
            email.send_keys(Keys.ENTER)

            password = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@autocomplete="current-password"]'))
            )
            password.send_keys(self.twitter_password)
            password.send_keys(Keys.ENTER)

            tweet_compose = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="tweetTextarea_0"]'))
            )

            tweet = f"Hey Internet Provider, why is my internet speed {self.down}down/{self.up}up when I pay for {self.promised_down}down/{self.promised_up}up?"
            tweet_compose.send_keys(tweet)

            tweet_button = self.driver.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetButtonInline"]')
            tweet_button.click()

        except TimeoutException:
            print("Timed out waiting for Twitter elements")

    def run(self):
        self.get_internet_speed()
        if float(self.down) < self.promised_down or float(self.up) < self.promised_up:
            self.tweet_at_provider()
        self.driver.quit()

# Usage
bot = InternetSpeedTwitterBot(150, 10, "your_email@example.com", "your_password")
bot.run()