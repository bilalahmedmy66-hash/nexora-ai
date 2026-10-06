from app.core.permissions import Role
from tests.conftest import PASSWORD

NEW = {
    "email": "New.Person@example.com",
    "full_name": "New Person",
    "password": PASSWORD,
    "role": "member",
}


def test_requires_auth(client):
    assert client.get("/api/v1/users").status_code == 401


def test_member_and_viewer_forbidden(client, make_user, auth_headers):
    make_user("m@example.com", Role.MEMBER)
    make_user("v@example.com", Role.VIEWER)
    for email in ("m@example.com", "v@example.com"):
        r = client.get("/api/v1/users", headers=auth_headers(email))
        assert r.status_code == 403
        assert r.json()["error"]["code"] == "forbidden"


def test_manager_can_read_but_not_write(client, make_user, auth_headers):
    make_user("mgr@example.com", Role.MANAGER)
    h = auth_headers("mgr@example.com")
    assert client.get("/api/v1/users", headers=h).status_code == 200
    assert client.post("/api/v1/users", json=NEW, headers=h).status_code == 403


def test_admin_creates_user_email_normalized(client, admin_h):
    r = client.post("/api/v1/users", json=NEW, headers=admin_h)
    assert r.status_code == 201
    assert r.json()["email"] == "new.person@example.com"
    assert "password" not in r.json() and "hashed_password" not in r.json()


def test_duplicate_email_conflict(client, admin_h):
    client.post("/api/v1/users", json=NEW, headers=admin_h)
    r = client.post(
        "/api/v1/users",
        json={**NEW, "email": "new.person@example.com"},
        headers=admin_h,
    )
    assert r.status_code == 409
    assert r.json()["error"]["code"] == "email_taken"


def test_weak_passwords_rejected(client, admin_h):
    for pw in ("short1", "alllettersnonumber", "1234567890123"):
        r = client.post("/api/v1/users", json={**NEW, "password": pw}, headers=admin_h)
        assert r.status_code == 422, pw


def test_invalid_role_rejected(client, admin_h):
    r = client.post("/api/v1/users", json={**NEW, "role": "superuser"}, headers=admin_h)
    assert r.status_code == 422


def test_list_search_filter_sort_paginate(client, admin_h, make_user):
    make_user("alice@example.com", Role.MEMBER, "Alice Smith")
    make_user("bob@example.com", Role.MANAGER, "Bob Jones")
    make_user("carol@example.com", Role.MEMBER, "Carol Smith")

    r = client.get("/api/v1/users?q=smith&sort=email", headers=admin_h)
    assert [u["email"] for u in r.json()["items"]] == [
        "alice@example.com",
        "carol@example.com",
    ]
    assert r.json()["total"] == 2

    r = client.get("/api/v1/users?role=manager", headers=admin_h)
    assert [u["email"] for u in r.json()["items"]] == ["bob@example.com"]

    r = client.get("/api/v1/users?sort=-email&page=1&page_size=2", headers=admin_h)
    body = r.json()
    assert body["total"] == 4 and len(body["items"]) == 2
    assert body["items"][0]["email"] == "carol@example.com"

    r = client.get("/api/v1/users?sort=-email&page=2&page_size=2", headers=admin_h)
    assert len(r.json()["items"]) == 2


def test_invalid_sort_and_page_size(client, admin_h):
    assert client.get("/api/v1/users?sort=password", headers=admin_h).status_code == 422
    assert client.get("/api/v1/users?page_size=1000", headers=admin_h).status_code == 422


def test_get_missing_user_404(client, admin_h):
    r = client.get("/api/v1/users/9999", headers=admin_h)
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "user_not_found"


def test_update_user(client, admin_h, make_user):
    u = make_user("edit@example.com")
    r = client.patch(
        f"/api/v1/users/{u.id}",
        json={"full_name": "Renamed", "role": "manager"},
        headers=admin_h,
    )
    assert r.status_code == 200
    assert r.json()["full_name"] == "Renamed" and r.json()["role"] == "manager"


def test_admin_password_reset_works(client, admin_h, make_user):
    u = make_user("reset@example.com")
    new_pw = "Brand-New-Pass-42"
    assert (
        client.patch(f"/api/v1/users/{u.id}", json={"password": new_pw}, headers=admin_h).status_code == 200
    )
    assert (
        client.post(
            "/api/v1/auth/login",
            json={"email": "reset@example.com", "password": new_pw},
        ).status_code
        == 200
    )
    assert (
        client.post(
            "/api/v1/auth/login",
            json={"email": "reset@example.com", "password": PASSWORD},
        ).status_code
        == 401
    )


def test_admin_cannot_demote_or_deactivate_self(client, admin, admin_h):
    r = client.patch(f"/api/v1/users/{admin.id}", json={"role": "member"}, headers=admin_h)
    assert r.status_code == 400 and r.json()["error"]["code"] == "cannot_modify_self"
    r = client.delete(f"/api/v1/users/{admin.id}", headers=admin_h)
    assert r.status_code == 400


def test_second_admin_can_be_demoted_by_first(client, admin_h, make_user):
    second = make_user("admin2@example.com", Role.ADMIN)
    r = client.patch(f"/api/v1/users/{second.id}", json={"role": "member"}, headers=admin_h)
    assert r.status_code == 200


def test_service_refuses_to_remove_last_active_admin(db_session, admin, make_user):
    import pytest

    from app.core.errors import AppError
    from app.services import user_service

    other = make_user("someone@example.com", Role.MANAGER)  # a different actor
    with pytest.raises(AppError) as exc:
        user_service.deactivate_user(db_session, admin, other)
    assert exc.value.code == "last_admin"


def test_deactivated_user_token_stops_working(client, admin_h, make_user, auth_headers):
    u = make_user("temp@example.com")
    h = auth_headers("temp@example.com")
    assert client.get("/api/v1/auth/me", headers=h).status_code == 200
    client.delete(f"/api/v1/users/{u.id}", headers=admin_h)
    assert client.get("/api/v1/auth/me", headers=h).status_code == 401
