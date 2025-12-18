"""
Pytest configuration and fixtures
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities database before each test"""
    # Store original state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball training and games",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": []
        },
        "Tennis Club": {
            "description": "Tennis instruction and practice matches",
            "schedule": "Wednesdays and Saturdays, 4:00 PM - 5:00 PM",
            "max_participants": 10,
            "participants": []
        },
        "Debate Club": {
            "description": "Develop public speaking and critical thinking skills",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 4:30 PM",
            "max_participants": 16,
            "participants": []
        },
        "Science Club": {
            "description": "Explore scientific concepts through experiments and projects",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": []
        },
        "Painting Studio": {
            "description": "Learn various painting techniques and artistic expression",
            "schedule": "Tuesdays and Saturdays, 4:00 PM - 5:30 PM",
            "max_participants": 12,
            "participants": []
        },
        "Theater Production": {
            "description": "Perform in school plays and develop acting skills",
            "schedule": "Thursdays and Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": []
        }
    }
    
    # Reset activities to original state
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # Clean up after test
    activities.clear()
    activities.update(original_activities)
