from bs4 import BeautifulSoup
import requests
import smtplib
import re
import functools
import operator
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

response = requests.get("https://appbrewery.github.io/instant_pot/")
response.encoding = 'utf-8'
amazon_page = response.text
soup = BeautifulSoup(amazon_page, "html.parser")
sender_email = "szymonbryniakproject@gmail.com"
recipient_email = "oneplusszymonbryniak@gmail.com"
app_password = "bjmm fcxz zojn vdju"

def find_price():
  print(soup.find("p", class_="a-spacing-none a-text-left a-size-mini twisterSwatchPrice").text.strip()[1:])
  message = float(soup.find("p", class_="a-spacing-none a-text-left a-size-mini twisterSwatchPrice").text.strip()[1:])
  return message

def reduce_function():
  pass

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




