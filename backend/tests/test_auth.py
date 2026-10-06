from app.core.security import create_access_token, create_refresh_token
from tests.conftest import PASSWORD


def test_health(client):
    assert client.get("/api/v1/health").json() == {"status": "ok"}


def test_login_success_and_me(client, admin):
    r = client.post("/api/v1/auth/login", json={"email": "ADMIN@example.com", "password": PASSWORD})
    assert r.status_code == 200
    body = r.json()
    assert body["token_type"] == "bearer"
    me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {body['access_token']}"})
    assert me.status_code == 200
    assert me.json()["email"] == "admin@example.com"
    assert "users:write" in me.json()["permissions"]
    assert "hashed_password" not in me.json()


def test_login_wrong_password_and_unknown_email_look_identical(client, admin):
    a = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@example.com", "password": "wrong-pass-1"},
    )
    b = client.post(
        "/api/v1/auth/login",
        json={"email": "nobody@example.com", "password": "wrong-pass-1"},
    )
    assert a.status_code == b.status_code == 401
    assert a.json() == b.json()
    assert a.json()["error"]["code"] == "invalid_credentials"


def test_inactive_user_cannot_login(client, admin_h, make_user):
    u = make_user("gone@example.com")
    client.delete(f"/api/v1/users/{u.id}", headers=admin_h)
    r = client.post("/api/v1/auth/login", json={"email": "gone@example.com", "password": PASSWORD})
    assert r.status_code == 401


def test_me_requires_token(client):
    r = client.get("/api/v1/auth/me")
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "unauthorized"


def test_garbage_token_rejected(client):
    r = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer not.a.token"})
    assert r.status_code == 401


def test_refresh_token_cannot_be_used_as_access_token(client, admin):
    r = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {create_refresh_token(admin.id)}"},
    )
    assert r.status_code == 401


def test_refresh_flow(client, admin):
    ok = client.post("/api/v1/auth/refresh", json={"refresh_token": create_refresh_token(admin.id)})
    assert ok.status_code == 200
    bad = client.post("/api/v1/auth/refresh", json={"refresh_token": create_access_token(admin.id)})
    assert bad.status_code == 401


def test_login_validation_error_shape(client):
    r = client.post("/api/v1/auth/login", json={"email": "not-an-email", "password": "x"})
    assert r.status_code == 422
    err = r.json()["error"]
    assert err["code"] == "validation_error"
    assert err["details"][0]["field"] == "email"
