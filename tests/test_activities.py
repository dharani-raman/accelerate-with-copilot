import pytest


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert payload
    for details in payload.values():
        assert expected_fields <= details.keys()


@pytest.mark.parametrize("field", ["description", "schedule"])
def test_get_activities_returns_non_empty_text_fields(client, field):
    # Arrange
    endpoint = "/activities"

    # Act
    response = client.get(endpoint)

    # Assert
    assert response.status_code == 200
    assert all(details[field].strip() for details in response.json().values())


def test_get_activities_participants_within_capacity(client):
    # Arrange
    endpoint = "/activities"

    # Act
    response = client.get(endpoint)

    # Assert
    assert response.status_code == 200
    for details in response.json().values():
        assert len(details["participants"]) <= details["max_participants"]


def test_root_redirects_to_static_index(client):
    # Arrange
    endpoint = "/"

    # Act
    response = client.get(endpoint, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"
