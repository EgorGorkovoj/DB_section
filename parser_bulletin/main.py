import datetime
import os
import requests
from abc import ABC
from pathlib import Path
from bs4 import BeautifulSoup


BASE_DIR = Path(__file__).parent

SITE_URL = 'https://spimex.com'
PAGE_URL = f'{SITE_URL}/markets/oil_products/trades/results/'
page = requests.get(PAGE_URL)


soup = BeautifulSoup(page.text, features='lxml')
results = []
links = soup.find_all(
    'a', attrs={
        'class': 'accordeon-inner__item-title link xls'
    }
)
for link in links:
    href = link['href']
    if not href:
        continue
    href = href.split('?')[0]
    if 'upload/reports/oil_xls/oil_xls_' not in href or not href.endswith('.xls'):
        continue
    print(href)
    date = href.split('oil_xls_')[1][:8]
    file_date = datetime.datetime.now().date()
    print(file_date)
    url_file = href if href.startswith("http") else f'{SITE_URL}{href}'
    results.append((url_file, file_date))
print(results)

# TODOсделать на классах, спарсить все файлы, подключиться плюс проверка по времени
def upload_file(results):
    link = results[0][0]
    filename = link.split('reports/oil_xls/')[-1]
    print(filename)
    response = requests.get(link)
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    file_path = os.path.join(downloads_dir, filename)
    with open(file_path, "wb") as f:
        f.write(response.content)

    return file_path


print(upload_file(results=results))






class Parser(ABC):
    """Абстракный класс для парсинга."""
    pass


class ParserBulletin(Parser):
    pass


class LoadPage:
    pass
