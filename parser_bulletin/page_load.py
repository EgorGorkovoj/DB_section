from abc import ABC, abstractmethod

import requests


class PageLoader(ABC):
    @abstractmethod
    def get_page(self, url: str) -> requests.Response:
        pass


class RequestPageLoader(PageLoader):

    def get_page(self, url: str) -> requests.Response:
        return requests.get(url=url)
