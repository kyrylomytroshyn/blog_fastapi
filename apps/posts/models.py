from pydantic import BaseModel, EmailStr
from ..users.models import User


class Post(BaseModel):
    id: int
    title: str
    body: str
    author: User


class CreatePostParams(BaseModel):
    title: str
    body: str
    userId: int


class PostInfo(Post):
    comments: list


class UpdatePost(BaseModel):
    title: str
    body: str
