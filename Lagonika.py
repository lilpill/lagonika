import requests
from bs4 import BeautifulSoup
import time
import datetime

URL = "https://www.lagonika.gr/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}

def check_product():
    
    # Creating the previous string to check if this change
    global previous_click

    # Request Page Source
    html = requests.get(URL, headers=headers)

    # Parse the HTML
    soup = BeautifulSoup(html.text, 'lxml')

    # Find the first product that shows in the site
    product = soup.find('div', id='wpv-view-layout-262648')

    # Find the click of the product
    click = product.find('div',class_='la-des-prosfora-btn').find('a')['href']
    
    # Check if the click button of the product is different from the previous product
    if str(click) != str(previous_click):
        
        # The click button has changed, find the details of the product
        name = product.find('h3', class_='la-listview-title')
        site = name.find('a')['href']
        name = name.text

        subtitle = product.find('div', class_='la-listview-subtitle')
        if subtitle.find('div',class_='la-listview-store'):
            shop = subtitle.find('div',class_='la-listview-store').text
        else:
            shop = "None"
        if subtitle.find('span',class_='la-listview-StartStop').text.strip():
            expire = subtitle.find('span',class_='la-listview-StartStop').text
        else:
            expire = "None"

        description = product.find('div', class_='la-listview-content').text

        discount = product.find('div', class_='la-listview-info').find('div',class_='la-offer-price').text
        if not discount.strip():
            discount = "None"

        coupon = product.find('div',class_='la-listview-info')
        if coupon.find('span', class_='la-listview-coupon-value'):
            coupon = coupon.find('span',class_='la-listview-coupon-value').text
        else:
            coupon = "None"

        time = product.find('div', class_='la-prin-apo').text
        
        image = product.find('div', class_='lagonika-listview-offer-top-image').find('img')['src']
        
        name = name.strip()
        send_to_discord(name, shop, expire, description,discount, coupon, time, site, image, click)
        previous_click = click
        

        print("Found Item #" +str() + name + "\n")
    
def send_to_discord(name, shop, expire, description, discount, coupon, time, site, image, click):
    webhook_url = "INSERT YOUR URL"
    # Create the payload for the Discord webhook
    payload = {
        "embeds": [{
            "author":
            {
                "name": 'LilPill',
                "icon_url": 'https://cdn.discordapp.com/avatars/234011025286889475/0ddc1715f7278b595d81c637f0fcb620.png',
            },
            "thumbnail":
            {
                "url": image
            },
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "fields": [
                {
                    "name" : "**[Title]** ✏️",
                    "value" : f"[{name}]({site})",
                    "inline" : False,
                },
                {
                    "name": "**[Description]** 📝",
                    "value": description,
                    "inline" : False
                },
                {
                    "name": "**[Click]** 🖱️",
                    "value": f"[Click Me]({click})",
                    "inline": True,
                },
                {
                    "name": "**[Shop]** ❤️",
                    "value": shop,
                    "inline": True,

                },
                {
                    "name": "**[Coupon]** 🏷️",
                    "value": coupon,
                    "inline": True,
                },
                {
                    "name": "**[Discount]** 💰",
                    "value": discount,
                    "inline": True,
                },
                {
                    "name": "**[Time]** ⏰",
                    "value": time,
                    "inline": True,
                },
                {
                    "name": "**[Expire]** 🕰️",
                    "value": expire,
                    "inline": True,
                }]
        }]
    }
    # Send the request to the Discord webhook
    requests.post(webhook_url, json=payload)


# Initialize the previous image URL to an empty string
previous_click = ""

while True:
    check_product()
    time.sleep(5)
