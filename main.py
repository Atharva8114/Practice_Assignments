from fastapi import FastAPI, HTTPException
from database import collection
from schemas import UserCreate, UserUpdate
from models import user_helper
from bson import ObjectId

app = FastAPI()


@app.post("/users")
async def create_user(user: UserCreate):
    result = await collection.insert_one(user.dict())
    new_user = await collection.find_one({"_id": result.inserted_id})
    return user_helper(new_user)


@app.get("/users")
async def get_all_users():
    users = []
    async for user in collection.find():
        users.append(user_helper(user))
    return users


@app.get("/users/{user_id}")
async def get_user(user_id: str):
    try:
        user = await collection.find_one({"_id": ObjectId(user_id)})
        if user:
            return user_helper(user)
        raise HTTPException(status_code=404, detail="User not found")
    except:
        raise HTTPException(status_code=400, detail="Invalid user ID")


@app.put("/users/{user_id}")
async def update_user(user_id: str, user: UserUpdate):
    try:
        update_data = {k: v for k, v in user.dict().items() if v is not None}

        if len(update_data) == 0:
            raise HTTPException(status_code=400, detail="No data to update")

        result = await collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )

        if result.modified_count == 1:
            updated_user = await collection.find_one({"_id": ObjectId(user_id)})
            return user_helper(updated_user)

        raise HTTPException(status_code=404, detail="User not found")
    except:
        raise HTTPException(status_code=400, detail="Invalid user ID")


@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    try:
        result = await collection.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count == 1:
            return {"message": "User deleted successfully"}
        raise HTTPException(status_code=404, detail="User not found")
    except:
        raise HTTPException(status_code=400, detail="Invalid user ID")
