import datetime
from parser import LinkExtractor

from page_load import PageLoader


class BulletinCollector:

    def __init__(
            self, page_url: str,
            loader: PageLoader,
            extractor: LinkExtractor,
            start_date: datetime.date,
            end_date: datetime.date
    ):
        self.page_url = page_url
        self.loader = loader
        self.extractor = extractor
        self.start_date = start_date
        self.end_date = end_date

    def collect(self) -> list[tuple[str, datetime.date]]:
        results = []
        page_number = 1
        next_page_url = self.page_url

        while True:
            html = self.loader.get_page(next_page_url).text

            stop_all = False

            for file_url, file_date in self.extractor.extract(html):

                if file_date > self.end_date:
                    continue

                if self._validate_time(file_date):
                    stop_all = True
                    break

                results.append((file_url, file_date))

            if stop_all:
                break

            page_number += 1
            next_page_url = self.page_url + f'?page=page-{page_number}'
            print(next_page_url)

        return results

    def _validate_time(self, file_date):
        return file_date < self.start_date
