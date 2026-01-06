from fastapi import APIRouter, HTTPException
from bson import ObjectId

from app.database import user_collection
from app.schemas import UserCreate, UserResponse
from app.models import user_helper

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    result = await user_collection.insert_one(user.dict())
    new_user = await user_collection.find_one({"_id": result.inserted_id})
    return user_helper(new_user)


@router.get("/", response_model=list[UserResponse])
async def get_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_helper(user)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user: UserCreate):
    await user_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": user.dict()}
    )
    updated = await user_collection.find_one({"_id": ObjectId(user_id)})
    return user_helper(updated)


@router.delete("/{user_id}")
async def delete_user(user_id: str):
    result = await user_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
