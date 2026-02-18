import urllib.parse

from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # basic sanity: known activity present
    assert "Basketball Team" in data


def test_signup_and_remove_participant():
    activity = "Basketball Team"
    email = "test.student@mergington.edu"

    # Ensure clean state before test
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    signup_url = f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"
    resp = client.post(signup_url)
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Duplicate signup should be rejected
    resp_dup = client.post(signup_url)
    assert resp_dup.status_code == 400

    # Now remove the participant
    delete_url = f"/activities/{urllib.parse.quote(activity)}/participants?email={urllib.parse.quote(email)}"
    resp_del = client.delete(delete_url)
    assert resp_del.status_code == 200
    assert email not in activities[activity]["participants"]
