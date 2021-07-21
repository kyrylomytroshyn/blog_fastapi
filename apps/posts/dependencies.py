import asyncio

from .models import Post, PostInfo, UpdatePost, CreatePostParams
from ..users.models import User

from typing import List, Dict, Any
import aiohttp


class PostRepository:

    async def list_posts(self) -> List[User]:
        pass

    async def create_post(self, params: CreatePostParams) -> Post:
        pass

    async def post_details(self, post_id: int) -> PostInfo:
        pass

    async def update_post(self, params: UpdatePost, post_id: int) -> Dict[str, Any]:
        pass


class JSONPlaceholderPostRepository(PostRepository):

    def __init__(self):
        self._endpoint_for_posts = "http://jsonplaceholder.typicode.com/posts"
        self._endpoint_for_comments = "http://jsonplaceholder.typicode.com/comments"
        self._endpoint_for_users = "http://jsonplaceholder.typicode.com/users"

    async def list_posts(self) -> List[Post]:
        raw_posts = await self._list_posts()
        return [self._convert_post(raw_post) for raw_post in raw_posts]

    async def _list_posts(self) -> List[Post]:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(self._endpoint_for_posts)
            raw_posts = await resp.json()
            await self._combine_authors_posts(raw_posts)
            return raw_posts

    async def _combine_authors_posts(self, raw_post: list) -> None:
        async with aiohttp.ClientSession() as session:
            user = await session.get(self._endpoint_for_users)
            raw_users = await user.json()
            for raw_p in raw_post:
                tmp_user = await self._user_by_id(raw_p["userId"])
                raw_p['author'] = tmp_user

    async def _user_by_id(self, user_id: int) -> Dict[int, Any] or None:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(self._endpoint_for_users)
            users = await resp.json()
            for user in users:
                if user_id == user["id"]:
                    return user

            return None

    async def post_details(self, post_id: int) -> PostInfo:
        raw_post = await self._post_details(post_id)
        result = PostInfo(**raw_post)
        return result

    async def _post_details(self, post_id: int) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(self._endpoint_for_posts + f"/{post_id}")
            raw_post = await resp.json()
            raw_post["author"] = await self._get_user_by_id(raw_post["userId"])
            raw_post["comments"] = await self._get_comments(post_id)
            return raw_post

    async def _get_user_by_id(self, user_id: int) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(self._endpoint_for_users + f"/{user_id}")
            raw_user = await resp.json()
            return raw_user

    async def _get_comments(self, post_id: int) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(self._endpoint_for_comments + "?postId=" + str(post_id))
            raw_comments = await resp.json()
            return raw_comments

    async def create_post(self, params: CreatePostParams) -> Post:
        raw_post = await self._create_post(params)
        return self._convert_post(raw_post)

    async def _create_post(self, params: CreatePostParams) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            resp = await session.post(self._endpoint_for_posts, json=params.dict())
            raw_post = await resp.json()
            raw_post["author"] = await self._user_by_id(raw_post['userId'])
            return raw_post

    async def update_post(self, params: UpdatePost, post_id: int) -> Dict[str, Any]:
        post = await self._update_post(params, post_id)
        return post

    async def _update_post(self, params: UpdatePost, post_id: int) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            resp = await session.put(self._endpoint_for_posts + f'/{post_id}', json=params.dict())
            raw_post = await resp.json()
            return raw_post

    def _convert_post(self, raw_post: Dict[str, Any]) -> Post:
        return Post(**raw_post)


class PostRepositoryFactory:
    def __init__(self):
        self._repo = None

    def __call__(self) -> PostRepository:
        if self._repo is None:
            self._repo = JSONPlaceholderPostRepository()
        return self._repo


get_post_repository = PostRepositoryFactory()
