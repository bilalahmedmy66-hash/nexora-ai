"""Command-line helpers. Run from the backend folder:

python -m app.cli create-admin --email you@example.com --name "Your Name"
"""

import argparse
import getpass
import sys

from pydantic import ValidationError

from app.core.errors import AppError
from app.core.permissions import Role
from app.db.session import SessionLocal
from app.schemas.user import UserCreate
from app.services import user_service


def create_admin(email: str, name: str) -> int:
    password = getpass.getpass("Password (min 10 chars, letters + numbers): ")
    if password != getpass.getpass("Repeat password: "):
        print("Passwords do not match.")
        return 1
    try:
        data = UserCreate(email=email, full_name=name, password=password, role=Role.ADMIN)
    except ValidationError as e:
        print("Invalid input:", "; ".join(err["msg"] for err in e.errors()))
        return 1
    with SessionLocal() as db:
        try:
            user = user_service.create_user(db, data, actor=None)
        except AppError as e:
            print(e.message)
            return 1
    print(f"Created admin {user.email} (id {user.id}).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="app.cli")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("create-admin", help="Create an admin user")
    p.add_argument("--email", required=True)
    p.add_argument("--name", required=True)
    args = parser.parse_args()
    if args.command == "create-admin":
        return create_admin(args.email, args.name)
    return 1


if __name__ == "__main__":
    sys.exit(main())
