from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import time
import uuid

APP_VERSION = os.getenv("APP_VERSION", "dev")
JOBS_FILE = os.getenv("JOBS_FILE", "/tmp/jobs.json")
WORKER_STATUS_FILE = os.getenv("WORKER_STATUS_FILE", "/tmp/worker-status.json")
START_TIME = time.time()

def load_jobs():
    if not os.path.exists(JOBS_FILE):
        return []
    with open(JOBS_FILE, "r") as file:
        return json.load(file)

def load_worker_status():
    if not os.path.exists(WORKER_STATUS_FILE):
        return {"status": "unknown"}

    with open(WORKER_STATUS_FILE, "r") as file:
        return json.load(file)

def save_jobs(jobs):
    with open(JOBS_FILE, "w") as file:
        return json.dump(jobs, file, indent=2)

class Handler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        body = (json.dumps(data) + "\n").encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            self._send_json({
                "service": "devops-incident-playground",
                "message": "background automation lab"
            })
        elif self.path == "/health":
            self._send_json({"status": "ok"})
        elif self.path == "/version":
            self._send_json({"version": APP_VERSION})
        elif self.path == "/uptime":
            self._send_json({"uptime_seconds": int(time.time() - START_TIME)})
        elif self.path == "/jobs":
            self._send_json({"jobs": load_jobs()})
        elif self.path == "/worker-status":
            self._send_json(load_worker_status())
        else:
            self._send_json({"error": "not found"}, 404)
    def do_POST(self):
        if self.path == "/jobs":
            jobs = load_jobs()
            job = {
                "id": str(uuid.uuid4()),
                "status": "pending",
                "created_at": int(time.time()),
                "finished_at": None
            }
            jobs.append(job)
            save_jobs(jobs)
            self._send_json(job, 201)
        else:
            self._send_json({"error": "not found"}, 404)

server = HTTPServer(("0.0.0.0", 8000), Handler)
print("API running on port 8000")
server.serve_forever()
