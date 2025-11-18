import datetime
from parser import BulletinLinkExtractor

from collector import BulletinCollector
from config import BASE_DIR, url
from file_loader import XMLFileDownloader
from page_load import RequestPageLoader


def main():

    start_date = datetime.date(2023, 1, 1)
    end_date = datetime.datetime.now().date()

    response = RequestPageLoader()
    extractor = BulletinLinkExtractor(url.SITE_URL)
    collector = BulletinCollector(url.PAGE_URL, response, extractor, start_date, end_date)
    links = collector.collect()
    print(links)
    downloader = XMLFileDownloader(BASE_DIR, response)

    for link, date in links:
        filename = link.split('reports/oil_xls/')[-1]
        downloader.download(link, filename)


if __name__ == '__main__':
    main()
