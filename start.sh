#!/usr/bin/env bash
set -euo pipefail

python manage.py migrate --no-input
gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8000}
