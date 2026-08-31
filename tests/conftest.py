import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    # activities is module-level mutable state shared by every request.
    snapshot = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(snapshot))


@pytest.fixture
def sample_activity():
    return "Chess Club"


@pytest.fixture
def registered_email(client, sample_activity):
    email = "newstudent@mergington.edu"
    client.post(f"/activities/{sample_activity}/signup", params={"email": email})
    return email
