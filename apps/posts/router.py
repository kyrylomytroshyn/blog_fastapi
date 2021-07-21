from fastapi import APIRouter, Depends

from .dependencies import get_post_repository, PostRepository
from .models import CreatePostParams, Post, PostInfo, UpdatePost
from typing import List

router = APIRouter()


@router.get("/", response_model=List[Post], tags=["posts"])
async def list_posts(repository: PostRepository = Depends(get_post_repository)):
    users = await repository.list_posts()
    return users


@router.post("/", response_model=Post, status_code=201, tags=["posts"])
async def create_post(
        params: CreatePostParams,
        repository: PostRepository = Depends(get_post_repository)
):
    post = await repository.create_post(params)
    return post


@router.put("/{post_id}", response_model=UpdatePost, status_code=200, tags=["posts"])
async def update_post(
        post_id: int,
        params: UpdatePost,
        repository: PostRepository = Depends(get_post_repository)
):
    post = await repository.update_post(params, post_id)
    return post


@router.get("/{post_id}", response_model=PostInfo, tags=["posts"])
async def post_details(
        post_id: int,
        repository: PostRepository = Depends(get_post_repository)
):
    post = await repository.post_details(post_id)
    return post
