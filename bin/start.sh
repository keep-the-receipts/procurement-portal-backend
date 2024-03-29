#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


python manage.py collectstatic --noinput
gunicorn  --worker-class gevent procurement_portal.wsgi:application --log-file - --bind 0.0.0.0:${PORT:-5000} --timeout 600
