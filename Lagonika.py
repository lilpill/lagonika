import requests
from bs4 import BeautifulSoup
import time

URL = "https://www.lagonika.gr"

# Put your own Webhook here
webhook_url = "YOUR_WEBHOOK_URL"

# Headers to make the site think that you are browsing and not using bot.
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Funciton to check the product
def check_product():
    # A global variable to keep the previous item
    global previous_site
    try:
        # Make the request
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
        
        # Using BeautifulSoup to find the items that we want
        soup = BeautifulSoup(response.content, 'lxml')
        site = soup.find('a', class_='linkTag')
        print(site.text)
        
        # If statement so the script will not print the same as the previous
        if str(site['href']) != str(previous_site):
            name = site.text
            send_to_discord(name, "https://lagonika.gr" + site['href'])
            previous_site = site['href']
    except Exception as e:
        print(f"Error occurred: {e}")

# Function to make a request to Discord Webhook
def send_to_discord(name, site):
    try:
        requests.post(webhook_url, json={'content': f"[{name}]({site})"})
    except Exception as e:
        print(f"Error sending to Discord: {e}")

previous_site = ""

# Every 60 seconds will check for new product. You can change the value if you want.
while True:
    check_product()
    time.sleep(60)
