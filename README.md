# Domain expiry checker

Django based web application showing an overview of your domains and their expiry date.

## Features

* API for uploading list of domains
* automatically gathers data from whois servers

## Requirements

* Python 3.x (tested on Python 3.5)
* RabbitMQ (or alternative broker supported by [Celery](http://www.celeryproject.org/)

## Setup

Create virtual environment via:

```bash
virtualenv ./env -p python3
```

Migrate (and create if it doesn't exist) the database:

```bash
./env/bin/pyhon manage.py migrate
```

Create user for accessing admin interface via /admin/:

```bash
./env/bin/python manage.py createsuperuser
```

Start celery task queue via:

```bash
./env/bin/celery -A domainexpirychecker worker -l info
```

Start Django app for development:

```bash
./env/bin/python manage.py runserver
```

Start Django app for production:

```bash
source ~/env/bin/activate
pip install gunicorn
./env/bin/gunicorn -w 4 domainexpirychecker.wsgi:application -b 127.0.0.1:8000
```
(you will also need nginx or similar frontend server for serving static files from `./env/lib/python3.5/site-packages/django/contrib/admin/static/admin/` to `/static/admin/`)

## Usage

Login as superuser at http://localhost:8000/admin/.

## Create new Source

Create Source (i.e. source server, for example `dns-server` or `web-hosting-01` server) by click `Add` in `Checker` -> `Sources`:

* `Name`: name of the source that will be displayed next to the domain name
* `Auth key`: API key that will allow access to the API for this source (type whatever you want here; auth key must be unique between the sources)

### API calls

Curl example for uploading domain names (separated by new line character) from file x.txt:
```bash
cat x.txt | curl --header "Auth-Key: someAuthKey" --data-binary @- http://localhost:8000/checker/import-new-lines/
```

Curl example for sending domain names from BIND9 DNS server (only master zones):
```bash
ls -l /var/lib/bind/master/ | awk '{print $9}' | awk 'sub(/.hosts/, "")' | curl --header "Auth-Key: someAuthKey" --data-binary @- http://localhost:8000/checker/import-new-lines/
```

(replace Auth-Key with the one you specified when creating the Source object)
