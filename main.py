"""
Automated Amazon Price Tracker

Author: Alan
Date: October 4th 2024

This project looks for the product name and price of an Amazon page and emails you if there's a sale or discount of the product.
"""

from requests import get
from bs4 import BeautifulSoup
from smtplib import SMTP
from os import environ
from dotenv import load_dotenv
import lxml

load_dotenv()

# Fill with your link and regular price
URL = "https://a.co/d/2orOzVv"
REGULAR_PRICE = 1000

# Fill the data with your environment variables
EMAIL = environ["EMAIL"]
PASSWORD = environ["PASSWORD"]
HOST = environ["HOST"]
PORT = int(environ["PORT"])

def get_amazon_product():
    """
    Get the product and price
    :return: String with the name of the product; String with the price of the product
    """

    # Gets the data of the headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Accept-Language": "es-419,es;q=0.9",
    }

    # Gets the page code
    webpage = get(
        url=URL,
        headers=headers
    ).text

    # New BeautifulSoup object
    soup = BeautifulSoup(webpage, "lxml")

    # Gets the product's name
    product_name = soup.find(name="span", id="productTitle").getText().strip()

    # Gets the product's price
    product_price = soup.find(name="span", class_="a-price-whole").getText()

    return product_name, product_price

def send_email(product_name, product_price):
    """
    Sends a letter to the email.
    :return:
    """
    with SMTP(host=HOST, port=PORT) as connection:
        # Starts the connection
        connection.starttls()

        # Login the account
        connection.login(
            user=EMAIL,
            password=PASSWORD
        )

        message = f"Subject:Price offer alert!\n\nThe {product_name} has gone lower on sales, it's now affordable at ${product_price}\n\n{URL}"

        # Send the message
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=EMAIL,
            msg=message.encode('utf-8')
        )

# Gets the product name and its price
product, price = get_amazon_product()

# Formats the price to an integer
formatted_price = int(price.replace(",", "").replace(".", ""))

# If the formatted price is less than the regular price, sends an email
if formatted_price < REGULAR_PRICE:

    send_email(product, price)
