from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

SIMILAR_ACCOUNT = ""
USERNAME = ""
PASSWORD = ""

class InstaFollower:
    
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        
    def login(self):
        self.driver.get("https://www.instagram.com/login")
        time.sleep()
        
        # check if the cookie waring is present on the page
        decline_cookies_xpath = "/html/body/div[6]/div[1]/div[2]/div/div/div/div/div[2]/div/button[2]"
        cookie_warning = self.driver.find_elements(By.XPATH, decline_cookies_xpath)
        if cookie_warning:
            # Dismiss the cookie warning by clicking an element or button
            cookie_warning[0].click()
        
        username_input = self.driver.find_element(By.Name, "username")
        password_input = self.driver.find_element(By.Name, "password")
        
        username_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)
        
        time.sleep(2.1)
        password_input.send_keys(Keys.ENTER)
        
        time.sleep(5)
        
        # Click 'not now' on notification prompt
        notifications_prompt = self.driver.find_element(by=By.XPATH, value="//button[contains(text(), 'Not Now)]")
        if notifications_prompt:
            notifications_prompt.click()
    
    
    def find_followers(self):
         self.driver.get(f"https://www.instagram.com/{SIMILAR_ACCOUNT}/")
         time.sleep(3)
         
         followers_link = self.driver.find_element(By.XPATH, "//a[contains(@href,'/followers/')]")
         followers_link.click()
         
         time.sleep(3)
         
         followers_modal = self.driver.find_elements(By.XPATH, "//div[@role='dialog]/div/div[2]")
         for _ in range(10):
             self.driver.execute_script("arguments[0].scrollTop = arguments[0].scorollHeight", followers_modal)
             time.sleep(2)
     
    def follow(self):
        followers_button = self.driver.find_elements(By.XPATH, "//button[text()='Follow]")
        
        for button in followers_button:
            try:
                button.click()
                time.sleep(1)
            except ElementClickInterceptedException:
                cancel_button = self.driver.find_element(by=By.XPATH, value="//button[Contains(text(), 'cancel')]")
                cancel_button.click()
    
bot = InstaFollower()
bot.login()
bot.find_followers()
bot.follow()