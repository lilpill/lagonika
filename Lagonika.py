import requests
from bs4 import BeautifulSoup
import time
import datetime

URL = "https://www.lagonika.gr/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}

def check_product():
    html = requests.get(URL, headers=headers)

    # Parse the HTML
    global previous_click
    soup = BeautifulSoup(html.text, 'lxml')

    # Find the first product element
    product = soup.find('div', id='wpv-view-layout-262648')
    # product = soup.find('div', class_='post-1208517 prosfores type-prosfores status-publish has-post-thumbnail hentry category-moda katastima-sportsfactorygr types-151 no-featured-image-padding lagonika-neutralrating lagonika-expired lagonika-listview la-expired-offer')

    click = product.find('div',class_='la-des-prosfora-btn').find('a')['href']
    if str(click) != str(previous_click):
        # The image has changed, send a message to the Discord webhook
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
    webhook_url = "https://discord.com/api/webhooks/956189847784161290/Q79UQDKHS2P3i3oJslQhN_dKKk_UUH_B-mFUqbdi6iSYhnrtjNyhCPZ4XMS1eRGRl2uw"

    # Create the payload for the Discord webhook
    payload = {
        "embeds": [{
            "author":
            {
                "name": 'LilPill#1001',
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
