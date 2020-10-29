# Automated crawler

## Set up

### Env

    python3.8 -m venv venv
    . venv/bin/activate.sh
    
### Install requirements
    
    pip install -r requirements.txt
    
## Run

Supported crawlers: `viasna`.

    scrapy crawl viasna -s APP_POST_URL=<app_host>/api/v1/cage/lists/ -a url=http://spring96.org/ru/news/99708 -a date=09.08.2020 -a sheet_id=1234567

Here `APP_POST_URL` is endpoint of the web to import the whole list. `url` - source of the content. `date` - date the list corresponds to. `sheet_id` - #id of the sheet in the whole table which corresponds to the right date.
