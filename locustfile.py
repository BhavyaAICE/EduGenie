from locust import HttpUser, task, between

class EduGenieUser(HttpUser):
    # Simulate users taking between 2 to 5 seconds to read/think before next action
    wait_time = between(2, 5)

    @task(3)
    def test_qa_endpoint(self):
        """Scenario 1: Ask a question (Higher weight since it's most common)"""
        payload = {"question": "What is machine learning in simple terms?"}
        with self.client.post("/qa", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status {response.status_code}")

    @task(2)
    def test_explainer_endpoint(self):
        """Scenario 2: Request an explanation"""
        payload = {"topic": "Photosynthesis"}
        with self.client.post("/explain", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status {response.status_code}")

    @task(1)
    def test_quiz_endpoint(self):
        """Scenario 3: Generate a Quiz (Lower weight as it takes longer)"""
        payload = {
            "topic": "Python Programming", 
            "num_questions": 3, 
            "difficulty": "Easy"
        }
        with self.client.post("/quiz", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status {response.status_code}")

    @task(1)
    def test_roadmap_endpoint(self):
        """Scenario 4: Request a Learning Roadmap"""
        payload = {"topic": "Web Development", "level": "beginner"}
        with self.client.post("/learn/recommendations", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status {response.status_code}")
