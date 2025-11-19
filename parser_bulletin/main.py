import datetime
from parser import BulletinLinkExtractor

from collector import BulletinCollector
from core.config import DOWNLOADS_DIR, url
from core.db_depends import SessionLocal
from file_loader import XMLFileDownloader
from page_load import RequestPageLoader
from services.importer_db import SpimexImporter
from xml_extract.xml_data import MetricTonTableExtractor


def main():

    start_date = datetime.date(2023, 1, 1)
    end_date = datetime.datetime.now().date()

    response = RequestPageLoader()
    extractor = BulletinLinkExtractor(url.SITE_URL)
    collector = BulletinCollector(
        url.PAGE_URL, response, extractor, start_date, end_date
    )
    links = collector.collect()
    print(links)
    downloader = XMLFileDownloader(DOWNLOADS_DIR, response)
    downloaded_files = []
    for link, date in links:
        filename = link.split('reports/oil_xls/')[-1]
        file_path = downloader.download(link, filename)
        downloaded_files.append((file_path, date))

    with SessionLocal() as session:
        importer = SpimexImporter(session)
        for file_path, file_date in downloaded_files:
            print(file_path)
            extractor = MetricTonTableExtractor(file_path)
            df = extractor.extract()
            importer.save_table_bulk(df, file_date=file_date)


if __name__ == '__main__':
    main()
