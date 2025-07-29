from fastapi import APIRouter
from schemas import UserCreate, Token,UserOut
from auth.utils import create_user, authenticate_user, create_access_token, get_all_users

router = APIRouter(prefix="/auth")

# Creates user and returns an access token.
@router.post("/signup", response_model=Token)
async def signup(user: UserCreate):
    res = await create_user(user)
    return res

# Authenticates user and returns an access token.
@router.post("/token", response_model=Token)
async def login(user: UserCreate):
    return await authenticate_user(user)

#TODO: remove this endpoint
@router.get("/users", response_model=list[UserOut])
async def get_users():
    # This endpoint is for testing purposes only, should be removed in production
    users = await get_all_users()
    return users
