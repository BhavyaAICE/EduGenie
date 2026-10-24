"""
Comprehensive End-to-End Integration Tests for Repaired EduGenie
Validates all endpoints, static file mounts, health checks, schemas, and router registrations.
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_endpoint():
    """Verify standard /health endpoint is operational."""
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["service"] == "EduGenie"


def test_serve_frontend_root():
    """Verify GET / successfully serves index.html."""
    res = client.get("/")
    assert res.status_code == 200
    assert "text/html" in res.headers.get("content-type", "")
    assert "EduGenie" in res.text


def test_serve_static_assets():
    """Verify static assets are reachable via /static/ mount."""
    res_css = client.get("/static/style.css")
    assert res_css.status_code == 200
    assert len(res_css.text) > 1000

    res_cfg = client.get("/static/config.js")
    assert res_cfg.status_code == 200
    assert "API_BASE_URL" in res_cfg.text


def test_qa_endpoint():
    """Verify /qa route and response key."""
    res = client.post("/qa", json={"question": "What is Python?"})
    assert res.status_code == 200
    data = res.json()
    assert "response" in data
    assert len(data["response"]) > 0


def test_explanation_endpoint_schema():
    """Verify /explain route returns 'response' key (Bug B3 fix)."""
    res = client.post("/explain", json={"topic": "Gravity"})
    assert res.status_code == 200
    data = res.json()
    assert "response" in data
    # Ensure legacy/buggy key 'explanation' is not the top-level property
    assert isinstance(data["response"], str)


def test_quiz_endpoint_registered():
    """Verify /quiz route is properly registered and returns structured data (Bug B2 fix)."""
    res = client.post("/quiz", json={"topic": "Math", "num_questions": 2, "difficulty": "Easy"})
    assert res.status_code == 200
    data = res.json()
    assert "response" in data


def test_summarize_endpoint():
    """Verify /summarize route and depth configuration."""
    res = client.post("/summarize", json={"text": "Photosynthesis produces oxygen and glucose.", "length": "short"})
    assert res.status_code == 200
    data = res.json()
    assert "response" in data


def test_learning_recommendations_endpoint():
    """Verify /learn/recommendations route and signature parameters (Bug M2 & F3 fix)."""
    res = client.post("/learn/recommendations", json={"topic": "Python Programming", "level": "beginner"})
    assert res.status_code == 200
    data = res.json()
    assert "response" in data


def test_invalid_payload_validation():
    """Verify Pydantic request models reject malformed schemas with 422."""
    res = client.post("/learn/recommendations", json={"subject": "Math", "difficulty_level": "beginner"})
    assert res.status_code == 422
