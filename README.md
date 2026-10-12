# Kayange API (backend)

Flask JSON API. No HTML is served from here any more; the UI lives in `../frontend`.

## Run locally
    cp .env.example .env        # fill SECRET_KEY, JWT_SECRET_KEY; set COOKIE_SECURE=0
    pip install -r requirements.txt
    FRONTEND_ORIGINS=http://localhost:8788 python run.py   # http://localhost:5000/health

## Deploy (Render / Railway / Fly)
- Start command: `gunicorn run:app --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 120` (see `Procfile`/`Dockerfile`)
- Health check path: `/health`
- Environment variables: everything in `.env.example`. The app refuses to start without `SECRET_KEY` and `JWT_SECRET_KEY`.
- Put it on a subdomain of the same domain as the UI (e.g. `api.yourdomain.com`), and set `FRONTEND_ORIGINS=https://app.yourdomain.com`.

## Known limitation (unchanged from your code)
SQLite is still the primary database with a background sync to Supabase. That is why two instances can disagree,
and why a restart can lose recent rows. Run ONE instance until the app reads/writes Postgres directly.
