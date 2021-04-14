from urllib.request import urlopen
from bs4 import BeautifulSoup


def fetch_pun(url: str=None):
    soup = BeautifulSoup(urlopen(url), 'html.parser')
    return soup.find('ul', class_="puns single") \
        .find('li') \
        .find(text=True, recursive=False)
