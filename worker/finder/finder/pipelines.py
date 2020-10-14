from scrapy.crawler import Crawler
import logging
import requests

logger = logging.getLogger()


class PostAppPipeline:

    def __init__(self, url: str) -> None:
        self.url = url

    def process_item(self, item, spider):
        payload = {
            'first_name': item.get('first_name', 'Unknown'),
            'last_name': item['last_name'],
            'patronymic': item.get('patronymic', 'Unknown'),
            'birth_date': item.get('birth_date', '2020-01-01'),
            'metadata': {},
        }
        if 'city' in item:
            payload['metadata']['city'] = item['city']
        if 'place' in item:
            payload['metadata']['place'] = item['place']
        if 'comments' in item:
            payload['metadata']['comments'] = item['comments']

        response = requests.post(self.url, json=[payload], headers={'Content-Type': 'application/json'})

        logger.info(f'Set item {item} to app: {response.status_code} {response.reason}')

        return item

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> 'PostAppPipeline':
        return cls(
            url=crawler.settings.get('APP_POST_URL'),
        )
