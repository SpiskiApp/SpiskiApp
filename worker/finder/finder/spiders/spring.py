import scrapy
from collections import namedtuple
from scrapy.http import Request, Response
from finder.items import HumanInfo


ItemArgs = namedtuple('ItemArgs', ['full_name', 'city', 'place', 'comments'])


class SpringSpider(scrapy.Spider):
    name = 'viasna'
    allowed_domains = ['spring96.org', 'docs.google.com']
    start_urls = ['http://spring96.org/ru/news/99708']

    def parse(self, response: Response, **kwargs):
        if response.url.startswith('https://docs.google.com'):
            yield from self.parse_gsheet_content(response)
        else:
            gsheet_full_url = response.xpath('//iframe')[0].attrib['src']

            # these properties throw an error querying with wrong user-agent
            gsheet_url = (
                gsheet_full_url
                .replace('&headers=true', '')
                .replace('headers=true', '')
                .replace('&single=true', '')
                .replace('single=true', '')
                .replace('&widget=true', '')
                .replace('widget=true', '')
            )
            self.logger.info(gsheet_url)

            yield Request(url=gsheet_url)

    def parse_gsheet_content(self, response: Response) -> scrapy.Item:
        for table in response.xpath('//table'):
            rows = table.xpath('tbody//tr')

            thead = table.xpath('thead/tr')[0]
            # it can be (<>, id, full name, city, place, comments) or (<>, full name, city, place, comments)
            if len(thead.xpath('th')) == 6:
                should_skip_id = True
            else:
                should_skip_id = False

            for row in rows:
                row_cells = [attr for attr in row.xpath('td')]
                if should_skip_id:
                    row_cells = row_cells[1:]

                row_values = [cell.xpath('text()').get() or '' for cell in row_cells]

                if len(row_values) != len(ItemArgs._fields):
                    self.logger.warn(f'Values mismatch: {row_values}')
                    continue

                if not ''.join(row_values):
                    continue

                attrs = ItemArgs._make(row_values)

                item = HumanInfo()
                if not attrs.full_name:
                    self.logger.warn(f'Empty full name {attrs}')
                    continue

                item['last_name'] = attrs.full_name.split()[0]
                if len(attrs.full_name.split()) > 1:
                    item['first_name'] = attrs.full_name.split()[1]
                if len(attrs.full_name.split()) > 2:
                    item['patronymic'] = attrs.full_name.split()[2]
                if attrs.city:
                    item['city'] = attrs.city
                if attrs.place:
                    item['place'] = attrs.place
                if attrs.comments:
                    item['comments'] = attrs.comments

                yield item
