#!/bin/sh
set -e

# Use provided DATABASE_URL or default to sqlite in /data
DATABASE_URL=${DATABASE_URL:-sqlite:///data/notes.db}
export DATABASE_URL

echo "[entrypoint] Using DATABASE_URL=${DATABASE_URL}"

# Ensure target directory exists (helps with mounted volumes)
# If DB points to sqlite:///data/notes.db we create /data
mkdir -p /data || true

# Run DB init (idempotent). Continue even if it returns non-zero so logs show.
python init_db.py || echo "[entrypoint] init_db.py returned non-zero; continuing to start"

# Start the app (quote the callable to avoid shell parsing problems)
exec gunicorn -w 2 -b 0.0.0.0:5000 "app:create_app()"
