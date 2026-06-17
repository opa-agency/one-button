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

start_payment_simulator() {
  if [ "${SIMULATE_PAYMENTS_ON_START:-0}" != "1" ]; then
    return 0
  fi

  if [ "${DJANGO_DEBUG:-False}" = "True" ]; then
    return 0
  fi

  local clear_flag=""
  if [ "${SIMULATE_PAYMENTS_CLEAR:-1}" = "1" ]; then
    clear_flag="--clear"
  fi

  (
    while true; do
      if python manage.py simulate_payments --interval "${SIMULATE_PAYMENTS_INTERVAL:-2}" ${clear_flag}; then
        break
      fi
      echo "simulate_payments stopped unexpectedly; restarting in 5s" >&2
      sleep 5
    done
  ) &
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
start_payment_simulator
exec gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8000}
