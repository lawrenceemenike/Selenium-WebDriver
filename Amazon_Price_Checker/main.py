from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# email configureation
YOUR_EMAIL = "clen.emenike@gmail.com"
YOUR_PASSWORD = "Nneka@86"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
subject = []


practice_url = "https://appbrewery.github.io/instant_pot"
target_price = 100.00

# headers for the request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "DNT": "1",
}



def send_email(subjecgt, body):
    msg = MIMEMultipart()
    msg['From'] = YOUR_EMAIL
    msg['To'] = YOUR_EMAIL
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(YOUR_EMAIL, YOUR_PASSWORD)
        server.send_message(msg)
        
def check_price():
    response = requests.get(practice_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Try to find tge price element
    price_element = soup.find(class_="a-offscreen")
    
    if price_element:
        price = price_element.get_text()
        print("Found price:", price)
        
        # Remove the dollar sign and convert to float
        price_as_float = float(price.replace("$", "").strip())
        
        # Find the product title
        title_element = soup.find("span", id="priductTitle")
        title = title_element.get_text().strip() if title_element else "Unknown Product"
        
        print(f"Product: {title}")
        print(f"Current price: ${price_as_float}")
        
        if price_as_float < target_price:
            subject = f"Price Alert: {title} is now ${price_as_float}"
            body = f"""
            The orice of {title} has dropped below your target price of ${target_price}.
            
            Current price: ${price_as_float}
            
            Buy now {practice_url}
            """
            
            send_email(subject, body)
            print("Email alert sent!")
        else:
            print(f"Price is still above target, No alert sent.")
    else:
        print("Could not find price element with class 'a-offscreen'")
        
        # Let's try to find any element that might contain the price
        possible_price_elements = soup.find_all(text=lambda text: "$" in text)
        print("Possible price element found:", possible_price_elements)
        
        
if __name__ == "__main__":
    check_price()
        
        