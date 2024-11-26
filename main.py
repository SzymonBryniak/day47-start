from bs4 import BeautifulSoup
import requests
import smtplib

response = requests.get("https://appbrewery.github.io/instant_pot/")
amazon_page = response.text
soup = BeautifulSoup(amazon_page, "html.parser")

def find_price():
  print(soup.find("p", class_="a-spacing-none a-text-left a-size-mini twisterSwatchPrice").text.strip()[1:])
  message = float(soup.find("p", class_="a-spacing-none a-text-left a-size-mini twisterSwatchPrice").text.strip()[1:])
  return message

def product_name():
  title = soup.find(id="title").text
  return "product name"


def check_price(price):
  check = price < 100
  with smtplib.SMTP("smtp.gmail.com") as connection:
    if check:
      connection.starttls()
      connection.login(user="szymonbryniakproject@gmail.com", password="bjmm fcxz zojn vdju")
      connection.sendmail(msg='Subject: {}\n\n{}'.format("Amazon Price Alert!", str(product_name()) + f" is now ${price}"),to_addrs="oneplusszymonbryniak@gmail.com", from_addr="szymonbryniakproject@gmail.com")

check_price(find_price())



