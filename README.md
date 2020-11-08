[![codecov](https://codecov.io/gh/keep-the-receipts/procurement-portal-backend/branch/master/graph/badge.svg)](https://codecov.io/gh/keep-the-receipts/procurement-portal-backend/)
[![Build Status](https://travis-ci.com/keep-the-receipts/procurement-portal-backend.png)](https://travis-ci.com/keep-the-receipts/procurement-portal-backend)

Procurement portal backend
===============================


Project Layout
--------------

### Django

Apps go in the project directory `procurement_portal`


### Python

Dependencies are managed via pyproject.toml in the docker container.

Add and lock dependencies in a temporary container:

    docker-compose run --rm web poetry add pkgname==1.2.3

Rebuild the image to contain the new dependencies:

    docker-compose build web

Make sure to commit updates to Pipfile and Pipfile.lock to git


Development setup
-----------------

On Linux, you probably want to set the environment variables `USER_ID=$(id -u)`
and `GROUP_ID=$(id -g)` where you run docker-compose so that the container
shares your UID and GID. This is important for the container to have permission
to modify files owned by your host user (e.g. for python-black) and your host
user to modify files created by the container (e.g. migrations).

If you will be developing on the django frontend

    docker-compose run --rm web yarn
    docker-compose run --rm web yarn dev
    docker-compose run --rm web python manage.py collectstatic

To  initialise and run the django app

    docker-compose run --rm web bin/wait-for-postgres.sh
    docker-compose run --rm web python manage.py migrate
    docker-compose up


### Demo data

You can seed the database with demo data using

    docker-compose run --rm web python manage.py loaddata demodata

This installs a superuser with username `admin` and password `password`.


### Resetting the development environment data

If you need to destroy and recreate your dev setup, e.g. if you've messed up your
database data or want to switch to a branch with an incompatible database schema,
you can destroy all volumes and recreate them by running the following, and running
the above again:

    docker-compose down --volumes


Running tests
-------------

Make sure you have prepared static files and have the db running and ready

    docker-compose run --rm web yarn
    docker-compose run --rm web yarn build
    docker-compose run --rm web python manage.py collectstatic
    docker-compose run --rm web bin/wait-for-postgres.sh

Each time you'd like to run tests

    docker-compose run --rm web python manage.py test

Settings
--------

Undefined settings result in exceptions at startup to let you know they are not configured properly. It's one this way so that the defaults don't accidentally let bad things happen like forgetting analytics or connecting to the prod DB in development.


| Key | Default | Type | Description |
|-----|---------|------|-------------|
| `DATABASE_URL` | undefined | String | `postgresql://user:password@hostname/dbname` style URL |
| `DJANGO_DEBUG_TOOLBAR` | False | Boolean | Set to `True` to enable the Django Debug toolbar NOT ON A PUBLIC SERVER! |
| `DJANGO_SECRET_KEY` | undefined | String | Set this to something secret and unguessable in production. The security of your cookies and other crypto stuff in django depends on it. |
| `TAG_MANAGER_CONTAINER_ID` | undefined | String | [Google Tag Manager](tagmanager.google.com) Container ID. [Use this to set up Google Analytics.](https://support.google.com/tagmanager/answer/6107124?hl=en). Requried unless `TAG_MANAGER_ENABLED` is set to `False` |
| `TAG_MANAGER_ENABLED` | `True` | Boolean | Use this to disable the Tag Manager snippets, e.g. in dev or sandbox. |
