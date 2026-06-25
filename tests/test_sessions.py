from fastapi.testclient import TestClient


def create_feature(client: TestClient) -> dict:
    return client.post(
        "/features",
        json={"title": "Agent flow", "description": "Feature for sessions."},
    ).json()


def test_create_session_for_feature(client: TestClient) -> None:
    feature = create_feature(client)

    response = client.post(
        "/sessions",
        json={
            "feature_id": feature["id"],
            "persona": "coder",
            "notes": "Start implementation shell.",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["feature_id"] == feature["id"]
    assert body["persona"] == "coder"
    assert body["status"] == "pending"
    assert body["notes"] == "Start implementation shell."


def test_list_sessions(client: TestClient) -> None:
    feature = create_feature(client)
    client.post(
        "/sessions",
        json={"feature_id": feature["id"], "persona": "designer"},
    )
    client.post(
        "/sessions",
        json={"feature_id": feature["id"], "persona": "reviewer"},
    )

    response = client.get("/sessions")

    assert response.status_code == 200
    assert [session["persona"] for session in response.json()] == [
        "designer",
        "reviewer",
    ]


def test_get_one_session(client: TestClient) -> None:
    feature = create_feature(client)
    created = client.post(
        "/sessions",
        json={"feature_id": feature["id"], "persona": "coder"},
    ).json()

    response = client.get(f"/sessions/{created['id']}")

    assert response.status_code == 200
    assert response.json()["persona"] == "coder"


def test_update_session_status(client: TestClient) -> None:
    feature = create_feature(client)
    created = client.post(
        "/sessions",
        json={"feature_id": feature["id"], "persona": "coder"},
    ).json()

    response = client.patch(
        f"/sessions/{created['id']}/status",
        json={"status": "running"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_invalid_session_status_rejected(client: TestClient) -> None:
    feature = create_feature(client)
    created = client.post(
        "/sessions",
        json={"feature_id": feature["id"], "persona": "coder"},
    ).json()

    response = client.patch(
        f"/sessions/{created['id']}/status",
        json={"status": "paused"},
    )

    assert response.status_code == 422

