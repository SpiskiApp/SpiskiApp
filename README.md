# Spiski App
Helps you find your unlucky friend, when it gets arrested on protest. [Read more](https://github.com/unrealsolver/spiski_app/blob/master/ABOUT.md).

# Contributing
[Read more](https://github.com/unrealsolver/spiski_app/blob/master/CONTRIBUTING.md)

# Start up
## Local
```sh
cd spiski-app/
# Run DB
docker-compose up -d db

# Set up venv
python3.8 -m venv venv
. venv/bin/activate.sh

cd app/
pip install -r requirements/base.txt
env $(cat ../.env.dev) python manage.py migrate
env $(cat ../.env.dev) python manage.py runserver
xdg-open http://localhost:8000
```

## Lint

    cd app
    pip install -r requirements/base.txt -r requirements/dev.txt
    mypy .
    black --check --diff .

## Docker
```sh
cd spiski-app/
docker-compose up -d
xdg-open http://localhost:8000
```

# Shut down
```sh
docker-compose down
```

# Test

    env $(cat ../.env.dev) python manage.py test cage
