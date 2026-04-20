FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DOCKER=true

CMD [
  "gunicorn",
  "-k", "uvicorn.workers.UvicornWorker",
  "--workers", "2",
  "--timeout", "120",
  "--bind", "0.0.0.0:8000",
  "app:app"
]