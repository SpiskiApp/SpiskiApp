# Automated crawler

## Set up

### Env

    python3.8 -m venv venv
    . venv/bin/activate.sh
    
### Install requirements
    
    pip install -r requirements.txt
    
## Run

Supported crawlers: `viasna`.

    scrapy crawl viasna -s APP_POST_URL=<app_host>/api/v1/cage/inmates/
