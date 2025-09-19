# app/routers/posts_router.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..database import post_collection
from ..auth import get_current_user
from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/posts", tags=["Community Posts"])

class PostCreate(BaseModel):
    content: str

class PostOut(BaseModel):
    id: str = Field(alias="_id")
    content: str
    author_email: str
    upvotes: int
    downvotes: int
    created_at: datetime

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

@router.post("/", status_code=201)
async def create_post(post: PostCreate, current_user: dict = Depends(get_current_user)):
    post_dict = post.dict()
    post_dict["author_email"] = current_user["email"]
    post_dict["upvotes"] = 0
    post_dict["downvotes"] = 0
    post_dict["created_at"] = datetime.now()
    
    result = await post_collection.insert_one(post_dict)
    return {"message": "Post created", "post_id": str(result.inserted_id)}

@router.get("/", response_model=List[PostOut])
async def get_all_posts():
    posts_cursor = post_collection.find().sort("created_at", -1)
    posts = await posts_cursor.to_list(100)
    return posts

@router.post("/{post_id}/upvote")
async def upvote_post(post_id: str, current_user: dict = Depends(get_current_user)):
    try:
        obj_id = ObjectId(post_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid post ID format")
        
    result = await post_collection.update_one({"_id": obj_id}, {"$inc": {"upvotes": 1}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"status": "upvoted"}