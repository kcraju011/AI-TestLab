from locust import HttpUser, task, between


class AITestLabUser(HttpUser):

    wait_time = between(1, 3)

    @task(3)
    def health_check(self):
        self.client.get("/health")

    @task(2)
    def run_reliability_test(self):
        self.client.post(
            "/api/v1/reliability/run",
            json={
                "total_requests": 3,
                "simulated_delay_ms": 10,
                "failure_every": 0
            }
        )

    @task(1)
    def home(self):
        self.client.get("/")