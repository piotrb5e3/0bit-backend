# 0bit-backend

Backend for the 0bit app

## Prerequisites

You will need the following things properly installed on your computer.

* Git
* Python 3 (with pip)
* PostgreSQL

## Installation

* `cd 0bit-backend`
* `pip install -r requirements.txt`
* For running coverage tests with nose: `pip install django-nose coverage`

## Configuration
* `cd backend`
* `cp settings.local settings.py`
* Adjust configuration

### DB setup
* `python manage.py migrate`

## Running / Development

* `python manage.py runserver`

### Running Tests

* `python manage.py test`

### Updating dependencies
* adjust `requirements.in`
* `pip install pip-tools`
* `pip-compile requirements.in > requirements.txt`

### Deploying

* Create a `secretkey.txt` file in `backend` directory
* [Deploy with apache `mod_wsgi`](https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
)
* Don't forget to add `WSGIPassAuthorization On`

