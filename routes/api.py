from fastapi import APIRouter, HTTPException
from lightdb import LightDB
import random
import json

router = APIRouter()

database = LightDB("data.json")


def get_by_attribute(key, value, attribute="id"):
    for item in database.get(key):
        if item[attribute] == value:
            return item

    raise HTTPException(status_code=404, detail="Item not found")


def filter_by_user_id(array, user_id):
    return list(filter(lambda item: item["userId"] == user_id, array))


@router.get("/users")
async def get_users():
    return database.get("users")


@router.get("/users/{id}")
async def get_user(id: str):
    return get_by_attribute("users", id)


@router.get("/todos")
async def get_todos(user_id: str = None):
    todos = database.get("todos")

    if user_id:
        todos = filter_by_user_id(todos, user_id)

    return todos


@router.get("/todos/{id}")
async def get_todo(id: str):
    return get_by_attribute("todos", id)


@router.get("/posts")
async def get_posts(user_id: str = None):
    posts = database.get("posts")

    if user_id:
        posts = filter_by_user_id(posts, user_id)

    return posts


@router.get("/posts/{slug}")
async def get_post(slug: str):
    return get_by_attribute("posts", slug, "slug")


@router.get("/posts/{slug}/comments")
async def get_posts_comments(slug: str):
    post = get_by_attribute("posts", slug, "slug")

    return list(filter(lambda item: item["postSlug"] == post["slug"], database.get("comments")))


@router.get("/comments")
async def get_comments(user_id: str = None):
    comments = database.get("comments")

    if user_id:
        comments = filter_by_user_id(comments, user_id)

    return comments


@router.get("/comments/{id}")
async def get_comment(id: str):
    return get_by_attribute("comments", id)


@router.get("/photos")
async def get_photos(user_id: str = None):
    photos = database.get("photos")

    if user_id:
        photos = filter_by_user_id(photos, user_id)

    return photos


@router.get("/photos/{id}")
async def get_photo(id: str):
    return get_by_attribute("photos", id)


resources = ("users", "todos", "posts", "comments", "photos")


@router.get("/random")
async def get_random_resource():
    return random.choice(database.get(random.choice(resources)))


@router.get("/random/{key}")
async def get_random(key: str):
    try:
        data = database.get(f"{key}s")

        return random.choice(data)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"{key} not found")


@router.get("/all")
async def get_all():
    with open("data.json", "r") as file:
        return json.load(file)
