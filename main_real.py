from bs4 import BeautifulSoup
import requests
import smtplib
import re
import functools
import operator
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

headers = {
  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
  "Accept-Encoding": "gzip, deflate, br, zstd",
  "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
  "Priority": "u=0, i",
  "Sec-Ch-Ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
  "Sec-Ch-Ua-Mobile": "?0",
  "Sec-Ch-Ua-Platform": "Windows",
  "Sec-Fetch-Dest": "document",
  "Sec-Fetch-Mode": "navigate",
  "Sec-Fetch-Site": "cross-site",
  "Sec-Fetch-User": "?1",
  "Upgrade-Insecure-Requests": "1",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
}


response = requests.get("https://appbrewery.github.io/instant_pot/", headers=headers)
response.raise_for_status
response.encoding = 'utf-8'
amazon_page = response.text
soup = BeautifulSoup(amazon_page, "html.parser")
sender_email = "szymonbryniakproject@gmail.com"
recipient_email = "oneplusszymonbryniak@gmail.com"
app_password = "bjmm fcxz zojn vdju"



def find_price():
  print(soup.find(id="corePriceDisplay_desktop_feature_div").text.strip()[1:5])
  message = float(soup.find(id="corePriceDisplay_desktop_feature_div").text.strip()[1:5])
  return message

def product_name():
  content = soup.find(id="title").text
  content_re = re.split("\s", content)
  no_spaces = list(filter(lambda x: x != "", content_re))
  with_spaces = " ".join(no_spaces)
  # concatenate_no_spaces = functools.reduce(operator.add, no_spaces)

  return with_spaces

def check_price(price):
  check = price < 100
  with smtplib.SMTP("smtp.gmail.com") as connection:
    if check:
      connection.starttls()
      connection.login(user="szymonbryniakproject@gmail.com", password="bjmm fcxz zojn vdju")
      connection.sendmail(msg='Subject: {}\n\n{}'.format("Amazon Price Alert!", str(product_name()) + f" is now ${price}"),to_addrs="oneplusszymonbryniak@gmail.com", from_addr="szymonbryniakproject@gmail.com")

def check_price_mime(price):
    check = price < 100

    if check:
      body = product_name()
      try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = "Amazon Price Alert!"
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                    connection.starttls()  # Secure the connection
                    connection.login(user=sender_email, password=app_password)
                    connection.sendmail(
                        from_addr=sender_email,
                        to_addrs=recipient_email,
                        msg=msg.as_string()
                    )
                    print("Email sent successfully!")
      except Exception as e:
        print(f"Failed to send email: {e}")

check_price_mime(find_price())




