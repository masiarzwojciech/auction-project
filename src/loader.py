from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from parser import CsvAuctionParser
from models import Auction


class AuctionLoader:
    def __init__(self, parser: CsvAuctionParser):
        self.parser = parser

    def load(self, paths: list[Path]) -> list[Auction]:
        with ThreadPoolExecutor() as ex:
            return [
                auction
                for auctions in ex.map(self.parser.parse_file, paths)
                for auction in auctions
            ]
