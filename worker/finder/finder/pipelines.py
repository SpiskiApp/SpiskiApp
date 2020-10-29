from scrapy.crawler import Crawler
import logging
import requests

logger = logging.getLogger()


class PostAppPipeline:

    def __init__(self, url: str) -> None:
        self.url = url

    def process_item(self, list_info, spider):
        payload = {
            'items': [],
            'text': spider.page_url,
            'origin': list_info['origin'],
            'date': list_info['date'].isoformat(),
        }
        for item in list_info['items']:
            item_payload = {
                'first_name': item.get('first_name', 'Unknown'),
                'last_name': item['last_name'],
                'patronymic': item.get('patronymic', 'Unknown'),
                'birth_date': item.get('birth_date', '2020-01-01'),
                'metadata': {},
            }
            if 'city' in item:
                item_payload['metadata']['city'] = item['city']
            if 'place' in item:
                item_payload['metadata']['place'] = item['place']
            if 'comments' in item:
                item_payload['metadata']['comments'] = item['comments']

            payload['items'].append(item_payload)

        response = requests.post(self.url, json=payload, headers={'Content-Type': 'application/json'})

        if not response.ok:
            msg = response.reason
            if response.headers['content-type'] == 'application/json':
                msg += str(response.json())
            logger.error(msg)
        else:
            logger.info(f'Set the list {payload} to app: {response.status_code} {response.reason}')

        return list_info

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> 'PostAppPipeline':
        return cls(
            url=crawler.settings.get('APP_POST_URL'),
        )
