from src.app import activities


def test_unregister_registered_email_returns_200_and_removes_participant(
    client, sample_activity, registered_email
):
    # Arrange
    assert registered_email in activities[sample_activity]["participants"]

    # Act
    response = client.delete(
        f"/activities/{sample_activity}/signup", params={"email": registered_email}
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {registered_email} from {sample_activity}"
    assert registered_email not in activities[sample_activity]["participants"]


def test_unregister_email_not_signed_up_returns_404(client, sample_activity):
    # Arrange
    email = "stranger@mergington.edu"
    participants_before = list(activities[sample_activity]["participants"])

    # Act
    response = client.delete(f"/activities/{sample_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
    assert activities[sample_activity]["participants"] == participants_before


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    unknown_activity = "Underwater Basket Weaving"

    # Act
    response = client.delete(
        f"/activities/{unknown_activity}/signup", params={"email": "student@mergington.edu"}
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_then_signup_again_succeeds(client, sample_activity, registered_email):
    # Arrange
    client.delete(f"/activities/{sample_activity}/signup", params={"email": registered_email})

    # Act
    response = client.post(
        f"/activities/{sample_activity}/signup", params={"email": registered_email}
    )

    # Assert
    assert response.status_code == 200
    assert activities[sample_activity]["participants"].count(registered_email) == 1
