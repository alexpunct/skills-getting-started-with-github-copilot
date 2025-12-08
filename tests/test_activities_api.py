from fastapi.testclient import TestClient
import urllib.parse

from src.app import app, activities


client = TestClient(app)


def test_get_activities_returns_200_and_structure():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    # should be a dict with known activity keys
    assert isinstance(data, dict)
    assert "Chess Club" in data
    chess = data["Chess Club"]
    assert "participants" in chess


def test_signup_and_unregister_flow():
    email = "pytest_user@mergington.edu"
    activity = "Chess Club"

    # Ensure email not present initially
    assert email not in activities[activity]["participants"]

    # Sign up
    signup_res = client.post(f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}")
    assert signup_res.status_code == 200
    assert email in activities[activity]["participants"]

    # Duplicate signup should return 400
    dup = client.post(f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}")
    assert dup.status_code == 400

    # Unregister
    del_res = client.delete(f"/activities/{urllib.parse.quote(activity)}/participants?email={urllib.parse.quote(email)}")
    assert del_res.status_code == 200
    assert email not in activities[activity]["participants"]
