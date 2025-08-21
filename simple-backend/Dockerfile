FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=dictyexpress_backend.settings

# Entrypoint will handle migrate + seed at runtime
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

# Let compose override CMD; keep default for dev
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
