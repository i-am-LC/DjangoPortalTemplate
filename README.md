# Django Portal Template

GitHub Copilot: Sure, here's a description for your Django project:

Django Portal Template is a web application built using Django Cookiecutter that provides secure user authentication and login verification using OTP (one-time password) and static device setup (such as Google 2FA). The project also includes a feature that allows users to view their login records.

The project is designed to be hosted on AWS (Amazon Web Services) and uses AWS email service for email verification. With its robust security features and user-friendly interface, Django Portal Template is an ideal solution for businesses and organizations that require a secure and reliable user portal.

Django Portal Template at is core is aimed to streamline the deployment of secure, access restricted websites.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Built for AWS](https://img.shields.io/badge/built%20for-AWS-orange?logo=amazon-aws)](https://aws.amazon.com/)
[![OTP Login Verification](https://img.shields.io/badge/OTP-login%20verification-green)](https://en.wikipedia.org/wiki/Time-based_One-time_Password_algorithm)
[![Built with Bootstrap](https://img.shields.io/badge/built%20with-Bootstrap-563d7c?logo=bootstrap)](https://getbootstrap.com/)
[![Built with PostgreSQL](https://img.shields.io/badge/built%20with-PostgreSQL-336791?logo=postgresql)](https://www.postgresql.org/)

License: MIT

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Docker

This project utilises Docker. See detailed docker instructions:
- [Run locally](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally-docker.html).
- [Deployment](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).



### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ docker compose -f local.yml run --rm django python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy django_portal_template

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ docker compose -f local.yml run --rm django coverage run -m pytest
    $ docker compose -f local.yml run --rm django coverage report
    $ docker compose -f local.yml run --rm django coverage html

#### Running tests with pytest

    $ docker compose -f local.yml run --rm django pytest

### Celery

This app comes with Celery.

To run a celery worker:

```bash
cd django_portal_template
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

```bash
cd django_portal_template
celery -A config.celery_app beat
```

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

```bash
cd django_portal_template
celery -A config.celery_app worker -B -l info
```

### Sentry

Sentry is an error logging aggregator service. You can sign up for a free account at <https://sentry.io/signup/?code=cookiecutter> or download and host it yourself.
The system is set up with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.

## Deployment

The following details how to deploy this application.
