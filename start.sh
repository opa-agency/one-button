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

wait_for_database() {
  local attempts=0
  until python - <<'PY'
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

import django
django.setup()

from django.db import connections

try:
    connections["default"].ensure_connection()
except Exception as exc:  # pragma: no cover
    print(f"waiting for database: {exc}")
    sys.exit(1)

print("database connection ready")
PY
  do
    attempts=$((attempts + 1))
    if [ "$attempts" -ge 60 ]; then
      echo "database was not reachable after ${attempts} attempts; exiting" >&2
      exit 1
    fi
    sleep 2
  done
}

start_payment_simulator() {
  if [ "${SIMULATE_PAYMENTS_ON_START:-0}" != "1" ]; then
    return 0
  fi

  local clear_flag=""
  if [ "${SIMULATE_PAYMENTS_CLEAR:-1}" = "1" ]; then
    clear_flag="--clear"
  fi

  python manage.py simulate_payments --interval "${SIMULATE_PAYMENTS_INTERVAL:-2}" ${clear_flag} &
  echo $! > /tmp/simulate_payments.pid
  echo "started simulate_payments with pid $(cat /tmp/simulate_payments.pid)"
}

wait_for_database
python manage.py migrate --no-input
python manage.py ensure_superuser
if command -v npm >/dev/null 2>&1 || [ -n "${NPM_BIN_PATH:-}" ]; then
  python manage.py tailwind build
else
  echo "npm not available; skipping Tailwind rebuild and continuing with existing static assets" >&2
fi
python manage.py collectstatic --no-input
start_payment_simulator
exec gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8000}
