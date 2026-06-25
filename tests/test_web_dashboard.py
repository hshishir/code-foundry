from fastapi.testclient import TestClient


HTML_HEADERS = {"accept": "text/html"}


def test_dashboard_home_returns_200(client: TestClient) -> None:
    response = client.get("/", headers=HTML_HEADERS)

    assert response.status_code == 200
    assert "Feature workflow dashboard" in response.text


def test_sessions_page_returns_200(client: TestClient) -> None:
    response = client.get("/sessions", headers=HTML_HEADERS)

    assert response.status_code == 200
    assert "Session inventory" in response.text


def test_feature_detail_page_returns_200_for_existing_feature(
    client: TestClient,
) -> None:
    feature = client.post(
        "/features",
        json={"title": "Render detail", "description": "Show detail page."},
    ).json()

    response = client.get(f"/features/{feature['id']}/view", headers=HTML_HEADERS)

    assert response.status_code == 200
    assert "Render detail" in response.text


def test_dashboard_includes_created_feature_title(client: TestClient) -> None:
    client.post(
        "/features",
        json={"title": "Visible roadmap item", "description": "Appears in table."},
    )

    response = client.get("/", headers=HTML_HEADERS)

    assert response.status_code == 200
    assert "Visible roadmap item" in response.text


def test_sessions_page_includes_created_session_persona_and_status(
    client: TestClient,
) -> None:
    feature = client.post(
        "/features",
        json={"title": "Session parent", "description": "Feature for session."},
    ).json()
    session = client.post(
        "/sessions",
        json={"feature_id": feature["id"], "persona": "reviewer"},
    ).json()
    client.patch(
        f"/sessions/{session['id']}/status",
        json={"status": "running"},
    )

    response = client.get("/sessions", headers=HTML_HEADERS)

    assert response.status_code == 200
    assert "reviewer" in response.text
    assert "running" in response.text

