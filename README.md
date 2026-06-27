# DevOps Incident Playground Background

A small DevOps portfolio project with a Python API, background worker, Docker Compose, Nginx reverse proxy, shared Docker volume, and job processing automation.

## Architecture

```text
                         GitHub Actions CI
                                |
                                v
                    build image + start compose stack
                                |
                                v
  client -> localhost:8098 -> nginx -> app:8000
                                |
                                v
                         jobs-data volume
                                ^
                                |
                             worker

    


app:/metrics -> prometheus:9090 -> grafana:3000 -> alerts
```

## services:
app      Python API service
worker   background job processor
nginx    reverse proxy exposed on localhost:8098
prometheus   metrics collector scraping app:/metrics
grafana      dashboards and alerting UI exposed on localhost:3000

## CI/CD:

GitHub Actions pipeline:
1. checks Python syntax
2. builds Docker image
3. starts Docker Compose stack
4. waits for /health
5. runs API smoke tests
6. prints container status
7. stops Docker Compose stack

##endpoints: 
GET  /                service info
GET  /health          API health check
GET  /version         app version
GET  /uptime          app uptime
GET  /jobs            list jobs
POST /jobs            create a pending job
GET  /worker-status   worker heartbeat/status

## HOW TO RUN/DOWN?
sudo docker-compose up -d --build
sudo docker-compose down

## TEST ON CURLS:
curl http://localhost:8098/health
curl http://localhost:8098/worker-status
curl -X POST http://localhost:8098/jobs
sleep 6
curl http://localhost:8098/jobs

or (use curle.exe in WPS)

