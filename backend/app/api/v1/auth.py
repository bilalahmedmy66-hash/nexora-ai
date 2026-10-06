from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.deps import client_ip, get_current_user
from app.core.permissions import permissions_for
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, RefreshRequest, TokenPair
from app.schemas.user import MeOut, UserOut
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenPair)
def login(body: LoginRequest, request: Request, db: Session = Depends(get_db)):
    return auth_service.login(db, body.email, body.password, client_ip(request))


@router.post("/refresh", response_model=TokenPair)
def refresh(body: RefreshRequest, db: Session = Depends(get_db)):
    return auth_service.refresh(db, body.refresh_token)


@router.get("/me", response_model=MeOut)
def me(user: User = Depends(get_current_user)):
    base = UserOut.model_validate(user).model_dump()
    return MeOut(**base, permissions=permissions_for(user.role))
