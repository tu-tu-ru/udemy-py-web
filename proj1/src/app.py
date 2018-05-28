# coding=utf-8
import requests
import BeautifulSoup
from requests import *
from BeautifulSoup import *
from bs4 import BeautifulSoup


req = requests.get("https://www.johnlewis.com/alienware-aw2518h-gaming-monitor-24-5-inch/p3275103")
content = req.content
soup = BeautifulSoup(content, "html.parser")
element = soup.find("p", {"class": "price price--large"})  # type: web element

price_string = element.text
# 可以在 element.text 之后加一个 strip() 把后边的空格都去掉

price_without_symbol = float(price_string[1:])

print(price_without_symbol)

if price_without_symbol<200:
    print("Buy it!")
else:
    print("For more.")