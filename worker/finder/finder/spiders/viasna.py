import scrapy
from collections import namedtuple
from datetime import date as datetime_date
from scrapy.http import Request, Response
from finder.items import HumanInfo, ListInfo


ItemArgs = namedtuple('ItemArgs', ['full_name', 'city', 'place', 'comments'])


class SpringSpider(scrapy.Spider):
    name = 'viasna'
    allowed_domains = ['spring96.org', 'docs.google.com']

    def __init__(self, *args, url: str, date: str, sheet_id: str, **kwargs):
        super().__init__(*args, **kwargs)

        self.page_url = url
        self.sheet_id = sheet_id

        day, month, year = map(int, date.split('.'))
        self.date = datetime_date(year=year, month=month, day=day)

    def start_requests(self):
        list_info = ListInfo(
            origin=self.page_url,
            date=self.date,
        )

        yield Request(self.page_url, dont_filter=True, cb_kwargs={'list_info': list_info})

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
            self.logger.info(f'Google sheet url: {gsheet_url}')

            yield Request(url=gsheet_url, cb_kwargs=response.cb_kwargs)

    def _get_table_columns_map(self, table):
        header_row = table.xpath('tbody/tr')[0].xpath('td')
        header_map = {
            'name': None,
            'city': None,
            'place': None,
            'comments': None,
        }

        for idx, header in enumerate(header_row):
            header_value = ''.join(t.get() for t in header.xpath('descendant-or-self::*/text()'))

            if 'фио' in header_value.lower():
                header_map['name'] = idx
                continue

            if 'город' in header_value.lower():
                header_map['city'] = idx
                continue

            if 'где' in header_value.lower():
                header_map['place'] = idx
                continue

            if 'комментарии' in header_value.lower():
                header_map['comments'] = idx
                continue

        return header_map

    def parse_gsheet_content(self, response: Response) -> scrapy.Item:
        doc_viewport = response.xpath("//div[@id='sheets-viewport']")[0]
        table_div = doc_viewport.xpath(f"div[@id='{self.sheet_id}']")[0]

        for table in table_div.xpath('descendant::table'):
            rows = table.xpath('tbody//tr')
            columns_map = self._get_table_columns_map(table)
            self.logger.info(f'Columns map: {columns_map}')

            items = []
            for row in rows:
                row_cells = [attr for attr in row.xpath('td')]

                # due to colspan=N
                row_values = [cell.xpath('text()').get() or '' for cell in row_cells] + [''] * 5

                if not ''.join(row_values):
                    continue

                attrs = ItemArgs(
                    full_name=row_values[columns_map['name']],
                    city=row_values[columns_map['city']],
                    place=row_values[columns_map['place']],
                    comments=row_values[columns_map['comments']],
                )

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

                items.append(item)

            list_info = response.cb_kwargs['list_info']
            list_info['items'] = items

            yield list_info
