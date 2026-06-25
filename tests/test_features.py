from fastapi.testclient import TestClient


def test_create_feature(client: TestClient) -> None:
    response = client.post(
        "/features",
        json={"title": "Draft idea", "description": "Capture a new workflow idea."},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["title"] == "Draft idea"
    assert body["description"] == "Capture a new workflow idea."
    assert body["status"] == "idea"
    assert "created_at" in body
    assert "updated_at" in body


def test_list_features(client: TestClient) -> None:
    client.post(
        "/features",
        json={"title": "One", "description": "First feature."},
    )
    client.post(
        "/features",
        json={"title": "Two", "description": "Second feature."},
    )

    response = client.get("/features")

    assert response.status_code == 200
    assert [feature["title"] for feature in response.json()] == ["One", "Two"]


def test_get_one_feature(client: TestClient) -> None:
    created = client.post(
        "/features",
        json={"title": "Readable", "description": "Fetch by id."},
    ).json()

    response = client.get(f"/features/{created['id']}")

    assert response.status_code == 200
    assert response.json()["title"] == "Readable"


def test_update_feature_status(client: TestClient) -> None:
    created = client.post(
        "/features",
        json={"title": "Move status", "description": "Change feature status."},
    ).json()

    response = client.patch(
        f"/features/{created['id']}/status",
        json={"status": "spec_ready"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "spec_ready"


def test_invalid_feature_status_rejected(client: TestClient) -> None:
    created = client.post(
        "/features",
        json={"title": "Reject invalid", "description": "Keep status bounded."},
    ).json()

    response = client.patch(
        f"/features/{created['id']}/status",
        json={"status": "nonsense"},
    )

    assert response.status_code == 422

