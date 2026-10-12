FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PORT=5000
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
# 1 worker + threads: the SQLite<->Supabase sync keeps per-process state (see README).
CMD ["sh", "-c", "gunicorn run:app --bind 0.0.0.0:${PORT} --workers 1 --threads 8 --timeout 120"]
