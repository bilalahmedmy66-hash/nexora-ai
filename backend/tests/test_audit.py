from app.core.permissions import Role
from tests.conftest import PASSWORD


def _actions(client, headers, **params):
    r = client.get("/api/v1/audit-logs", headers=headers, params=params)
    assert r.status_code == 200
    return [e["action"] for e in r.json()["items"]], r.json()


def test_audit_requires_permission(client, make_user, auth_headers):
    assert client.get("/api/v1/audit-logs").status_code == 401
    make_user("mgr@example.com", Role.MANAGER)
    assert client.get("/api/v1/audit-logs", headers=auth_headers("mgr@example.com")).status_code == 403


def test_events_are_recorded(client, admin_h, make_user):
    client.post(
        "/api/v1/auth/login",
        json={"email": "admin@example.com", "password": "bad-password-1"},
    )
    u = client.post(
        "/api/v1/users",
        json={
            "email": "x@example.com",
            "full_name": "X",
            "password": PASSWORD,
            "role": "member",
        },
        headers=admin_h,
    ).json()
    client.patch(f"/api/v1/users/{u['id']}", json={"role": "viewer"}, headers=admin_h)
    client.delete(f"/api/v1/users/{u['id']}", headers=admin_h)

    actions, body = _actions(client, admin_h)
    for expected in (
        "auth.login",
        "auth.login_failed",
        "user.created",
        "user.updated",
        "user.deactivated",
    ):
        assert expected in actions
    assert body["items"][0]["created_at"] >= body["items"][-1]["created_at"]


def test_audit_never_stores_passwords(client, admin_h):
    secret = "Zebra-Pass-12345"
    r = client.post(
        "/api/v1/users",
        json={
            "email": "y@example.com",
            "full_name": "Y",
            "password": secret,
            "role": "member",
        },
        headers=admin_h,
    ).json()
    client.patch(
        f"/api/v1/users/{r['id']}",
        json={"password": "Another-Pass-6789"},
        headers=admin_h,
    )
    raw = client.get("/api/v1/audit-logs", headers=admin_h).text
    assert secret not in raw and "Another-Pass-6789" not in raw


def test_audit_filter_by_action(client, admin_h):
    actions, body = _actions(client, admin_h, action="auth.login")
    assert set(actions) == {"auth.login"}
    assert body["total"] == len(actions)
