from abc import ABC, abstractmethod
from pathlib import Path

from page_load import PageLoader
from core.logger import logger


class FileDownloader(ABC):
    @abstractmethod
    def download(self, url: str, file_name: str) -> Path | None:
        pass


class XMLFileDownloader(FileDownloader):

    def __init__(self, base_dir: Path, page_loader: PageLoader):
        self.base_dir = base_dir
        self.page_loader = page_loader

    def download(self, url: str, file_name: str) -> Path | None:

        self.base_dir.mkdir(parents=True, exist_ok=True)

        file_path = self.base_dir / file_name

        if file_path.exists():
            logger.info(f'Файл {file_name} уже существует!')
            return file_path

        content = self.page_loader.get_page(url).content
        with open(file_path, 'wb') as f:
            f.write(content)
        return file_path
