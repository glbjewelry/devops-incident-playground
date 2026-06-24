import json
import os
import time

JOBS_FILE = os.getenv("JOBS_FILE", "/tmp/jobs.json")
WORKER_INTERVAL = int(os.getenv("WORKER_INTERVAL", "5"))
WORKER_STATUS_FILE = os.getenv("WORKER_STATUS_FILE", "/tmp/worker-status.json")

def load_jobs():
    if not os.path.exists(JOBS_FILE):
        return []

    with open(JOBS_FILE, "r") as file:
        return json.load(file)

def save_jobs(jobs):
    with open(JOBS_FILE, "w") as file:
        json.dump(jobs, file, indent=2)

def save_worker_status(processed_count):
    status = {
        "status": "running",
        "last_check_at": int(time.time()),
        "processed_count": processed_count
        }

    with open(WORKER_STATUS_FILE, "w") as file:
        json.dump(status, file, indent=2)

def process_jobs():
    jobs = load_jobs()
    changed = False
    processed_count = 0

    for job in jobs:
        if job["status"] == "pending":
            print(f"Processing job {job['id']}")
            job["status"] = "done"
            job["finished_at"] = int(time.time())
            changed = True
            processed_count += 1

    if changed:
        save_jobs(jobs)
    save_worker_status(processed_count)

print("Worker started")

while True:
    process_jobs()
    time.sleep(WORKER_INTERVAL)
