#!/bin/sh
set -eu

role="${APP_ROLE:-web}"

if [ -z "${APP_KEY:-}" ]; then
  echo "APP_KEY is required" >&2
  exit 64
fi

wait_for_migrations() {
  attempt=1
  while [ "$attempt" -le 60 ]; do
    if php artisan migrate:status --no-interaction --no-ansi >/dev/null 2>&1; then
      return 0
    fi
    attempt=$((attempt + 1))
    sleep 2
  done
  echo "Database migrations were not ready after 120 seconds" >&2
  return 1
}

case "$role" in
  web)
    attempt=1
    until php artisan migrate --force --no-interaction; do
      if [ "$attempt" -ge 60 ]; then
        echo "Database migration failed after 60 attempts" >&2
        exit 1
      fi
      attempt=$((attempt + 1))
      sleep 2
    done
    php artisan config:cache
    exec php artisan serve --host=0.0.0.0 --port="${PORT:-8080}"
    ;;
  worker)
    wait_for_migrations
    php artisan config:cache
    exec php artisan queue:work --sleep=3 --tries=3 --timeout=90 --no-interaction
    ;;
  scheduler)
    wait_for_migrations
    php artisan config:cache
    while true; do
      php artisan schedule:run --no-interaction --no-ansi
      sleep 60
    done
    ;;
  *)
    echo "APP_ROLE must be web, worker, or scheduler" >&2
    exit 64
    ;;
esac

