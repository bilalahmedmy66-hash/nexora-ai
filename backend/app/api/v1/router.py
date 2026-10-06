from fastapi import APIRouter

from app.api.v1 import audit, auth, users

api_router = APIRouter(prefix="/api/v1")


@api_router.get("/health", tags=["system"])
def health():
    return {"status": "ok"}


api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(audit.router)
