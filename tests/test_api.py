import json
import urllib.request


BASE_URL = "http://localhost:8098"


def get_json(path):
    with urllib.request.urlopen(BASE_URL + path, timeout=5) as response:
        assert response.status == 200
        return json.loads(response.read().decode("utf-8"))


def test_health():
    data = get_json("/health")
    assert data["status"] == "ok"


def test_version():
    data = get_json("/version")
    assert "version" in data


def test_jobs_list():
    data = get_json("/jobs")
    assert "jobs" in data
    assert isinstance(data["jobs"], list)


def test_metrics():
    with urllib.request.urlopen(BASE_URL + "/metrics", timeout=5) as response:
        body = response.read().decode("utf-8")

    assert response.status == 200
    assert "incident_jobs_total" in body
    assert "incident_worker_last_check_timestamp" in body

if __name__ == "__main__":
    test_health()
    test_version()
    test_jobs_list()
    test_metrics()
    print("API Tests PASSED CONGRATULATIONS")
