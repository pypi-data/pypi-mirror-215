import cloudscraper
from bs4 import BeautifulSoup

def get_soup(url, headers={}, cookies={}, json={}, data={}, params={}):
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url, headers=headers, cookies=cookies, json=json, data=data, params=params)
    soup = BeautifulSoup(response.content, "lxml")
    return soup

def get_html(url, headers={}, cookies={}, json={}, data={}, params={}):
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url, headers=headers, cookies=cookies, json=json, data=data, params=params)
    return response.content

def post_soup(url, headers={}, cookies={}, json={}, data={}, params={}):
    scraper = cloudscraper.create_scraper()
    response = scraper.post(url, headers=headers, cookies=cookies, json=json, data=data, params=params)
    soup = BeautifulSoup(response.content, "lxml")
    return soup

def post_html(url, headers={}, cookies={}, json={}, data={}, params={}):
    scraper = cloudscraper.create_scraper()
    response = scraper.post(url, headers=headers, cookies=cookies, json=json, data=data, params=params)
    return response.content
