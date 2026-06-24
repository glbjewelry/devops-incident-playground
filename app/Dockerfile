FROM python:3.12-slim

WORKDIR /app

COPY main.py .
COPY worker.py .

ENV APP_VERSION=1.0.0
ENV JOBS_FILE=/data/jobs.json
ENV WORKER_STATUS_FILE=/data/worker-status.json
ENV WORKER_INTERVAL=5

EXPOSE 8000

CMD ["python", "main.py"]

