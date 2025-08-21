#!/usr/bin/env sh
set -e

# Wait for DB (DATABASE_URL or split vars)
python - <<'PY'
import os, time
import psycopg
dsn = os.environ.get("DATABASE_URL")
if not dsn:
    user = os.environ.get("DATABASE_USER", "postgres")
    pwd  = os.environ.get("DATABASE_PASSWORD", "")
    host = os.environ.get("DATABASE_HOST", "postgres")
    port = os.environ.get("DATABASE_PORT", "5432")
    name = os.environ.get("DATABASE_NAME", "postgres")
    dsn  = f"postgresql://{user}:{pwd}@{host}:{port}/{name}"
for _ in range(60):
    try:
        psycopg.connect(dsn, connect_timeout=3).close()
        print("Database is reachable.")
        break
    except Exception:
        time.sleep(1)
else:
    raise SystemExit("Database did not become ready in time.")
PY

# Only this container runs migrations if RUN_MIGRATIONS=1
if [ "${RUN_MIGRATIONS:-0}" = "1" ]; then
  python manage.py migrate --noinput
  if [ "${SEED:-0}" = "1" ]; then
    python - <<'PY'
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE","dictyexpress_backend.settings")
django.setup()
from django.contrib.auth.models import User
from resolwe.flow.models import Data
if (not User.objects.filter(username="data_admin").exists()) or (Data.objects.count() == 0):
    print("Seeding initial data...")
    from populate_resolwe_data import main
    main()
else:
    print("Seed skipped: data already present.")
PY
  else
    echo "SEED not enabled; skipping data population."
  fi
else
  echo "RUN_MIGRATIONS not enabled; skipping migrate/seed."
fi

exec "$@"
