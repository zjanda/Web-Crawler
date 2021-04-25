# This file is for algorithm testing only. The program is to be run from launch.py
# import time as tm     # for delaying the program
from time import time   # for speed checking algorithms
import requests
from bs4 import BeautifulSoup


def is_valid_URL(URL):
    return True     # change later


def print_time(string, start):
    print(f'{string}{time() - start}')
    return time()


def defragment(URL):
    return URL.split('#')[0] if '#' in URL else URL


# Download the HTML document
link = ['https://dataquestio.github.io/web-scraping-pages/simple.html', 'https://forecast.weather.gov/#12309182']
knil = [1, 2, 3]

a = set(link)
b = set(knil)
print(bool())
print(bool(a & b))
URL = link[1]
URL = defragment(URL)
if is_valid_URL(URL):
    # Downloading the webpage
    response = requests.get(URL)
    if response.status_code == 200:
        # Extracting the source code of the page
        data = response.content     # can use .content (contents in bytes) or .text (contents in unicode)
        # Creating BeautifulSoup Object
        soup = BeautifulSoup(data, 'html.parser')
        # Extract all <a> tags
        tags = soup.find_all('a')

        # Extracting urls from the attribute href in <a> tags.
        for tag in tags:
            print(tag.get('href'))