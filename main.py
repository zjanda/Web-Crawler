from time import time
import requests
from bs4 import BeautifulSoup


def is_scrapable(URL):
    pass


def print_time(string, start):
    print(f'{string}{time() - start}')
    return time()


# Download the HTML document
link = ['https://dataquestio.github.io/web-scraping-pages/simple.html', 'https://forecast.weather.gov/']
page = requests.get(link[0])

soup = BeautifulSoup(page.content, 'html.parser')

p = soup.find_all('p')

for para in p:
    print(para.get_text())
