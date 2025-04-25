from fastapi import APIRouter

router = APIRouter(prefix="/users")

@router.get("/")
def get_users():
    return {"msg": "List of users"}
