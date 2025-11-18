from dataclasses import dataclass
from pathlib import Path

BASE_DIR: Path = Path(__file__).parent


@dataclass
class URLData:
    SITE_URL: str = 'https://spimex.com'
    PAGE_URL: str = f'{SITE_URL}/markets/oil_products/trades/results/'


url = URLData()
