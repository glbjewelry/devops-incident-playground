# DevOps Incident Playground Background

A small DevOps portfolio project with a Python API, background worker, Docker Compose, Nginx reverse proxy, shared Docker volume, and job processing automation.

## Architecture

```text
client -> localhost:8098 -> nginx -> app:8000
                                  
                                  |
                                  v
                            
                            jobs-data volume
                                  
                                  ^
                                  |
                               worker
```

## descript:
app      Python API service
worker   background job processor
nginx    reverse proxy exposed on localhost:8098

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

