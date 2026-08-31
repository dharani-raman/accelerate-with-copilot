from src.app import activities


def test_signup_new_email_returns_200_and_adds_participant(client, sample_activity):
    # Arrange
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{sample_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {sample_activity}"
    assert email in activities[sample_activity]["participants"]


def test_signup_duplicate_email_returns_400(client, sample_activity, registered_email):
    # Arrange
    participants_before = list(activities[sample_activity]["participants"])

    # Act
    response = client.post(
        f"/activities/{sample_activity}/signup", params={"email": registered_email}
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
    assert activities[sample_activity]["participants"] == participants_before


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    unknown_activity = "Underwater Basket Weaving"

    # Act
    response = client.post(
        f"/activities/{unknown_activity}/signup", params={"email": "student@mergington.edu"}
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_activity_name_with_space_is_resolved(client):
    # Arrange
    activity_with_space = "Math Olympiad"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_with_space}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in activities[activity_with_space]["participants"]


def test_signup_missing_email_returns_422(client, sample_activity):
    # Arrange
    endpoint = f"/activities/{sample_activity}/signup"

    # Act
    response = client.post(endpoint)

    # Assert
    assert response.status_code == 422
