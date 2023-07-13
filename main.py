import requests
import json
from bs4 import BeautifulSoup

def scrape_quotes_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = []
    
    quote_divs = soup.find_all('div', class_='quote')
    
    for quote_div in quote_divs:
        text = quote_div.find('span', class_='text').text
        author = quote_div.find('small', class_='author').text
        quotes.append({'text': text, 'author': author})
    
    return quotes

def get_next_page_url(soup):
    next_page_link = soup.find('li', class_='next')
    if next_page_link:
        return next_page_link.find('a')['href']
    return None

all_quotes = []
url = 'http://quotes.toscrape.com'
while url:
    quotes = scrape_quotes_page(url)
    all_quotes.extend(quotes)
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    url = get_next_page_url(soup)

with open('quotes.json', 'w') as f:
    json.dump(all_quotes, f)

authors = list(set(quote['author'] for quote in all_quotes))
with open('authors.json', 'w') as f:
    json.dump(authors, f)
