# Railway deployment checklist — Power Consumption Prediction API

## 1. Prerequisites

- [ ] **Root directory**: Railway runs from the **backend** folder (where `manage.py`, `Procfile`, `requirements.txt` live). If your repo root is the monorepo root, set **Root Directory** to `backend` in Railway.
- [ ] **Procfile**: `web: gunicorn config.wsgi` (this repo uses the `config` project package; if yours is named `power_consumption`, use `web: gunicorn power_consumption.wsgi`).
- [ ] **runtime.txt**: `python-3.11.9`.

---

## 2. Railway project setup

1. [ ] Create a new project on [Railway](https://railway.app).
2. [ ] **Deploy from GitHub**: connect repo and select branch.
3. [ ] Set **Root Directory** to `backend` (if repo root is not the Django app root).
4. [ ] Add **MongoDB** via Railway’s MongoDB plugin (one-click). Railway will set **MONGO_URL** automatically.

---

## 3. Environment variables (Railway dashboard → Variables)

| Variable        | Required | Example / notes |
|----------------|----------|------------------|
| `MONGO_URL`    | Yes*     | Set by Railway when you add MongoDB plugin. |
| `SECRET_KEY`   | Yes      | Long random string (e.g. `openssl rand -base64 50`). |
| `DEBUG`        | No       | Set to `0` or `False` in production. |
| `ALLOWED_HOSTS`| No       | Default includes `.railway.app`. Optional: `yourapp.up.railway.app`. |
| `MONGODB_NAME` | No       | Default: `power_consumption_db`. |

\* If you use Railway’s MongoDB plugin, `MONGO_URL` is provided automatically.

---

## 4. Build and run

- [ ] Railway will run:
  - **Build**: `pip install -r requirements.txt` (from Root Directory).
  - **Start**: `gunicorn config.wsgi` (from Procfile).
- [ ] If you use **./vendor/djongo-patched**: ensure the `vendor/djongo-patched` folder is committed. If not, in `requirements.txt` replace `./vendor/djongo-patched` with `djongo`.

---

## 5. After first deploy

- [ ] **Migrations** (if you use Django migrations with Djongo): run in Railway shell or one-off:
  ```bash
  python manage.py migrate
  ```
- [ ] **Static files**:
  ```bash
  python manage.py collectstatic --noinput
  ```
  (WhiteNoise will serve them; collectstatic is often run in a build step or one-off.)

---

## 6. Optional: reduce cold starts (free tier)

- [ ] ML models (`.pkl`) are loaded **once per worker** via `apps.consumption.ml_loader` (no load on every request).
- [ ] MongoDB client is **cached per process** in `mongo_utils` (avoids connection storm).
- [ ] Consider **1 Gunicorn worker** on free tier to save memory: in Procfile you can use:
  ```bash
  web: gunicorn config.wsgi --workers 1 --threads 2
  ```

---

## 7. Verify

- [ ] Open `https://<your-app>.up.railway.app` (or the URL Railway shows).
- [ ] Check health/API endpoint; confirm MongoDB and static files work.

---

## Summary of project changes

| Item | Change |
|------|--------|
| **MongoDB** | Uses `MONGO_URL` (Railway) or `MONGODB_URI`; connection timeouts in URI for stability. |
| **ALLOWED_HOSTS** | Default includes `.railway.app`; override with `ALLOWED_HOSTS` env. |
| **DEBUG** | Default `False`; set via `DEBUG` env. |
| **SECRET_KEY** | From env (required in production). |
| **WhiteNoise** | `STATICFILES_STORAGE` and `STATIC_ROOT` set for production. |
| **ML models** | Loaded once per process in `apps.consumption.ml_loader`. |
| **Mongo client** | Single cached client per process in `apps.consumption.mongo_utils`. |
| **Procfile** | `web: gunicorn config.wsgi` |
| **runtime.txt** | `python-3.11.9` |
