from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
import requests

def get_soup(url, headers={}, cookies={}, json={}, data={}, params={}):
    response = requests.get(url, headers=headers, cookies=cookies, json=json, data=data, params=params)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

def get_html(url, headers={}, cookies={}, json={}, data={}, params={}):
    response = requests.get(url, headers=headers, cookies=cookies, json=json, data=data, params=params)
    return response.text

def post_soup(url, headers={}, cookies={}, json={}, data={}, params={}):
    response = requests.post(url, headers=headers, cookies=cookies, json=json, data=data, params=params)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

def post_html(url, headers={}, cookies={}, json={}, data={}, params={}):
    response = requests.post(url, headers=headers, cookies=cookies, json=json, data=data, params=params)
    return response.text


def auth_soup(url, user, password):
    basic = HTTPBasicAuth(user, password)
    response = requests.get(url, auth=basic)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

def auth_html(url, user, password):
    basic = HTTPBasicAuth(user, password)
    response = requests.get(url, auth=basic)
    return response.text

