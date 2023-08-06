# MultiScraper
MultiScraper is a set of tools for fast and easy parsing. It includes methods for extracting html and soup objects from modules such as: requests, cloudscraper, Selenium, http.client, Aiohttp, urllib3. It also has 2 assistants. The first one is Regular, it contains ready-made, useful for parsing regular expressions. The second one is ResponseHandler, will help you figure out what the status code means to you. The most important thing is Lxmlsoup. This is an analogue of BeautifulSoup containing the most basic and necessary methods. Its speed exceeds bs4 by 2 times. The syntax is the same.

```
0.7749056816101074 - LxmlSoup
1.4368107318878174 - BeautifulSoup
```
## Installation

MultiScraper requires Python >= 3.7

Install with `pip` from PyPI:

```
pip install MultiScraper
```

### Examples

```python
from MultiScraper import Requests, LxmlSoup

html = Requests.get_html('https://sunlight.net/catalog')
soup = LxmlSoup.LxmlSoup(html)

links = soup.find_all('a', class_='cl-item-link js-cl-item-link js-cl-item-root-link')
for link in links:
    print(link.text(), link.get('href'))
```

```python
from MultiScraper import Aiohttp, LxmlSoup
import asyncio

async def main():
    url = "https://example.com"  
    html = await Aiohttp.get_html(url)
    soup = LxmlSoup.LxmlSoup(html)  
    title = soup.find('h1').text()
    print(title)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```
