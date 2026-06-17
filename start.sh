#!/usr/bin/env bash
set -euo pipefail

MANAGE_DIR=""

if [ -f "manage.py" ]; then
  MANAGE_DIR="."
elif [ -f "src/manage.py" ]; then
  MANAGE_DIR="src"
else
  echo "manage.py not found" >&2
  exit 1
fi

cd "$MANAGE_DIR"

TAILWIND_CSS="staticfiles/css/dist/styles.css"
COLLECTED_TAILWIND_CSS="local-cdn/css/dist/styles.css"

python manage.py migrate --no-input
python manage.py ensure_superuser
if command -v npm >/dev/null 2>&1 || [ -n "${NPM_BIN_PATH:-}" ]; then
  python manage.py tailwind build
elif [ -f "$TAILWIND_CSS" ]; then
  echo "npm not available; using prebuilt Tailwind CSS at $TAILWIND_CSS"
elif [ -f "$COLLECTED_TAILWIND_CSS" ]; then
  echo "npm not available; using collected Tailwind CSS at $COLLECTED_TAILWIND_CSS"
  exec gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8000}
else
  echo "npm not available and neither $TAILWIND_CSS nor $COLLECTED_TAILWIND_CSS exists; cannot serve Tailwind CSS" >&2
  exit 1
fi
python manage.py collectstatic --no-input
exec gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8000}
