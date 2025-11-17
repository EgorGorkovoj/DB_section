import datetime
import requests
from abc import ABC
from pathlib import Path
from bs4 import BeautifulSoup


BASE_DIR = Path(__file__).parent

SITE_URL = 'https://spimex.com'
PAGE_URL = f'{SITE_URL}/markets/oil_products/trades/results/'


# TODO: Сделать по Solid, разбить на файлы!
class Parser(ABC):
    """Абстракный класс для парсинга."""
    pass


class ParserBulletin(Parser):

    def __init__(self, parser):
        self.parser = parser
        self.results = []

    def parse_links(self):
        links = self.parser.find_all(
            'a', attrs={
                'class': 'accordeon-inner__item-title link xls'
            }
        )
        return links

    def get_link(
            self, start_date: datetime.date, end_date: datetime.date
    ):
        for link in self.parse_links():
            href = link['href']
            if not href:
                continue
            href = href.split('?')[0]
            if 'upload/reports/oil_xls/oil_xls_' not in href or not href.endswith('.xls'):
                continue
            file_date = self.extract_time(href=href)
            if not self.validate_date_range(file_date, start_date, end_date):
                break
            url_file = href if href.startswith('http') else f'{SITE_URL}{href}'
            self.results.append((url_file, file_date))
        return self.results

    def extract_time(self, href: str) -> datetime.date:
        # Добавить логгер
        try:
            date_in_href = href.split('oil_xls_')[1][:8]
            file_date: datetime.date = datetime.datetime.strptime(
                date_in_href, "%Y%m%d"
            ).date()
        except Exception as e:
            print(f'Не удалось извлечь время из ссылки: {e}')
        return file_date

    def validate_date_range(
        self,
        file_date: datetime.date,
        start_date: datetime.date,
        end_date: datetime.date,
    ) -> bool:
        return start_date <= file_date <= end_date


class LoadPage:

    def get_page(self, url) -> requests.Response:
        return requests.get(url)


class FileLoader(ABC):
    pass


class LoaderXML(FileLoader):

    def __init__(self, data: list, page: LoadPage):
        self.data = data
        self.page = page

    def extract_link(self):
        for link in self.data:
            yield link[0]

    def upload_file(self):

        downloads_dir = BASE_DIR / 'downloads'  # Вынести в константу
        downloads_dir.mkdir(exist_ok=True)

        for link in self.extract_link():
            filename = link.split('reports/oil_xls/')[-1]
            file_path = downloads_dir / filename
            if file_path.exists():
                # Логер инфо
                continue
            response = self.page.get_page(link)
            with open(file_path, 'wb') as f:
                f.write(response.content)
        return (
            f'Все файлы {filename} успешно загружены '
            f'в директорию: {downloads_dir}!'
        )


def main():

    all_results = []

    start_date = datetime.date(2023, 1, 1)
    end_date = datetime.datetime.now().date()

    number_page = 1
    next_url = PAGE_URL
    page = LoadPage()
    while True:
        response = page.get_page(next_url)
        soup = BeautifulSoup(response.text, 'lxml')
        bulletin = ParserBulletin(soup)

        links = bulletin.get_link(start_date, end_date)

        if not links:
            break

        all_results += links

        last_date = links[-1][1]

        if last_date <= start_date:
            break

        number_page += 1
        next_url = PAGE_URL + f'?page=page-{number_page}'
        print(next_url)
    xml = LoaderXML(all_results, page)
    xml.upload_file()


if __name__ == '__main__':
    main()
