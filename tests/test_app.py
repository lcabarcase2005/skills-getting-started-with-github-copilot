"""
Tests for the Mergington High School API
"""
import pytest


def test_root_redirects_to_index(client):
    """Test that root path redirects to static index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) == 9
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Basketball Team" in activities


def test_get_activities_structure(client):
    """Test that activities have the correct structure"""
    response = client.get("/activities")
    activities = response.json()
    
    # Check Chess Club structure
    chess_club = activities["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert chess_club["max_participants"] == 12
    assert len(chess_club["participants"]) == 2


def test_signup_for_activity_success(client):
    """Test successful signup for an activity"""
    response = client.post(
        "/activities/Basketball Team/signup?email=test@mergington.edu"
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "test@mergington.edu" in data["message"]
    assert "Basketball Team" in data["message"]
    
    # Verify participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "test@mergington.edu" in activities["Basketball Team"]["participants"]


def test_signup_for_nonexistent_activity(client):
    """Test signup for an activity that doesn't exist"""
    response = client.post(
        "/activities/Nonexistent Club/signup?email=test@mergington.edu"
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_registration(client):
    """Test that duplicate registration is prevented"""
    email = "duplicate@mergington.edu"
    
    # First signup should succeed
    response1 = client.post(
        f"/activities/Tennis Club/signup?email={email}"
    )
    assert response1.status_code == 200
    
    # Second signup should fail
    response2 = client.post(
        f"/activities/Tennis Club/signup?email={email}"
    )
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"].lower()


def test_unregister_from_activity_success(client):
    """Test successful unregistration from an activity"""
    # First, sign up
    client.post("/activities/Science Club/signup?email=test@mergington.edu")
    
    # Then unregister
    response = client.delete(
        "/activities/Science Club/unregister?email=test@mergington.edu"
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "Unregistered" in data["message"]
    assert "test@mergington.edu" in data["message"]
    
    # Verify participant was removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "test@mergington.edu" not in activities["Science Club"]["participants"]


def test_unregister_from_nonexistent_activity(client):
    """Test unregistration from an activity that doesn't exist"""
    response = client.delete(
        "/activities/Fake Club/unregister?email=test@mergington.edu"
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_not_registered_student(client):
    """Test unregistering a student who is not registered"""
    response = client.delete(
        "/activities/Debate Club/unregister?email=notregistered@mergington.edu"
    )
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"].lower()


def test_unregister_existing_participant(client):
    """Test unregistering an existing participant"""
    # Chess Club has michael@mergington.edu as a participant
    response = client.delete(
        "/activities/Chess Club/unregister?email=michael@mergington.edu"
    )
    assert response.status_code == 200
    
    # Verify removal
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in activities["Chess Club"]["participants"]


def test_multiple_signups_different_activities(client):
    """Test that a student can sign up for multiple different activities"""
    email = "multisport@mergington.edu"
    
    # Sign up for Basketball
    response1 = client.post(f"/activities/Basketball Team/signup?email={email}")
    assert response1.status_code == 200
    
    # Sign up for Tennis
    response2 = client.post(f"/activities/Tennis Club/signup?email={email}")
    assert response2.status_code == 200
    
    # Verify both registrations
    activities = client.get("/activities").json()
    assert email in activities["Basketball Team"]["participants"]
    assert email in activities["Tennis Club"]["participants"]


def test_activity_url_encoding(client):
    """Test that activity names with spaces are properly handled"""
    response = client.post(
        "/activities/Chess%20Club/signup?email=encoded@mergington.edu"
    )
    assert response.status_code == 200
    
    activities = client.get("/activities").json()
    assert "encoded@mergington.edu" in activities["Chess Club"]["participants"]
