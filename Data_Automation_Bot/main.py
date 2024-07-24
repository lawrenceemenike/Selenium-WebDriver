from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Part 1 = Scrape the links, addresses, and prices of the rental properties

header = {'Connection': 'keep-alive', 'Content-Length': '22018', 'Server': 'GitHub.com', 'Content-Type': 'text/html; charset=utf-8', 'permissions-policy': 'interest-cohort=()', 'Last-Modified': 'Thu, 11 Jul 2024 09:45:06 GMT', 'Access-Control-Allow-Origin': '*', 'Strict-Transport-Security': 'max-age=31556952', 'ETag': 'W/"668fa9a2-5660e"', 'expires': 'Wed, 24 Jul 2024 11:38:59 GMT', 'Cache-Control': 'max-age=600', 'Content-Encoding': 'gzip', 'x-hosts-log-append': 'pages_hosts_ips:{ [1] = 10.0.18.179,[2] = 10.0.3.168,[3] = 10.0.34.204,}', 'x-proxy-cache': 'MISS', 'X-GitHub-Request-Id': 'CC5C:1FFA4A:3E9D3:5B134:66A0E57A', 'Accept-Ranges': 'bytes', 'Age': '0', 'Date': 'Wed, 24 Jul 2024 11:44:51 GMT', 'Via': '1.1 varnish', 'X-Served-By': 'cache-cpt13825-CPT', 'X-Cache': 'HIT', 'X-Cache-Hits': '0', 'X-Timer': 'S1721821491.358800,VS0,VE281', 'Vary': 'Accept-Encoding', 'X-Fastly-Request-ID': '69b13124a06ac711656bb9bb3fd40fd6c814a227'}

# Use zillow clone site
response = requests.get("https://appbrewery.github.io/Zillow-Clone/", headers=header)

data = response.text
soup = BeautifulSoup(data, 'html.parser')

# Create a list of all the links on the page using a CSS Selector
all_link_elements = soup.select(".StyledPropertyCardDataWrapper a")
# Python list comprehension
all_links = [link["href"] for link in all_link_elements]
print(f"There are {len(all_links)} links to individual listings in total: \n")
print(all_links)

# Create a list of all the addresses on the pafe using a CSS Selector
# Remove newlines \n, pipe symbols |, and whitespaces to clean up the address data
all_address_elements = soup.select(".StyledPropertyCardWrapper address")
all_addresses = [address.get_text().replace(" | ", " ").strip() for address in all_address_elements]
print(f"\n After having been cleaned up, the {len(all_addresses)} addresses now look like this: \n")
print(all_addresses)

# Create a list of all the proces on the page using a CSS Selector
# Get a clean dollar price and strip off any "+" symbols and "per month" /mo abbrebreviation
all_price_elements = soup.select(".PropertyCardWrapper span")
all_prices = [price.get_text().replace("/mo", "").split("+")[0] for price in all_price_elements if "$" in price.text]
print(f"\n After having been cleaned up, the {len(all_prices)} prices now look like this: \n")
print(all_prices)

# Part 2 - Fill the Google Form using selenium
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

for n in range(len(all_links)):
    driver.get("https://forms.gle/BdVWJKHJ2ue1sJF96")
    time.sleep(2)
    
    # Use the xpath to select the "short answer" fields in your Google form.
    # Note, your xpath might be different if you created a different form.
    
    address = driver.find_element(by=By.XPATH, 
                        value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element(by=By.XPATH, 
                        value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(by=By.XPATH, 
                        value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(by=By.XPATH, 
                        value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    
    address.send_keys(all_addresses[n])
    price.send_keys(all_prices[n])
    link.send_keys(all_links[n])
    submit_button.click()