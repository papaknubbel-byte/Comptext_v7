from locust import HttpUser, task, between

class CompTextUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(3)
    def analyze_incident(self):
        self.client.post("/analyze", json={
            "text": "XENTRY Diagnosis - P0300 Random Misfire Detected on Cylinder 1. Brake force normal.",
            "quelle": "LoadTest"
        })

    @task(1)
    def compress_log(self):
        self.client.post("/compress", json={
            "text": "--- SOURCE: MO360 ---\\nLINE_D: EMERGENCY_STOP | REASON: THERMAL_OVERLOAD"
        })

    @task(1)
    def copilot_preview(self):
        self.client.post("/v1/copilot/preview", json={
            "text": "SAP-MM PO_4500112233: MATERIAL: CYLINDER-HEAD | STATUS: DELAYED",
            "quelle": "LoadTest"
        })
