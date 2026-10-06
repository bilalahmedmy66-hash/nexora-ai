import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.permissions import Role
from app.db.base import Base
from app.db.session import get_db
from app.main import create_app
from app.schemas.user import UserCreate
from app.services import user_service

PASSWORD = "Sup3rSecret99"


@pytest.fixture
def db_session():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    with Session() as session:
        yield session
    engine.dispose()


@pytest.fixture
def client(db_session):
    app = create_app()
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as c:
        yield c


@pytest.fixture
def make_user(db_session):
    def _make(email: str, role: Role = Role.MEMBER, name: str = "Test User"):
        return user_service.create_user(
            db_session,
            UserCreate(email=email, full_name=name, password=PASSWORD, role=role),
            None,
        )

    return _make


@pytest.fixture
def auth_headers(client):
    def _headers(email: str) -> dict:
        r = client.post("/api/v1/auth/login", json={"email": email, "password": PASSWORD})
        assert r.status_code == 200, r.text
        return {"Authorization": f"Bearer {r.json()['access_token']}"}

    return _headers


@pytest.fixture
def admin(make_user):
    return make_user("admin@example.com", Role.ADMIN, "Admin")


@pytest.fixture
def admin_h(admin, auth_headers):
    return auth_headers("admin@example.com")
