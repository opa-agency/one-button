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

retry_command() {
  local description="$1"
  shift

  local attempts=0
  until "$@"; do
    attempts=$((attempts + 1))
    echo "${description} failed (attempt ${attempts}); retrying in 2s" >&2
    sleep 2
  done
}

if [ "${DJANGO_DEBUG:-False}" = "True" ]; then
  python manage.py migrate --no-input
else
  retry_command "migrate" python manage.py migrate --no-input
fi
python manage.py ensure_superuser
if command -v npm >/dev/null 2>&1 || [ -n "${NPM_BIN_PATH:-}" ]; then
  python manage.py tailwind build
else
  echo "npm not available; skipping Tailwind rebuild and continuing with existing static assets" >&2
fi
python manage.py collectstatic --no-input
exec gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8000}
