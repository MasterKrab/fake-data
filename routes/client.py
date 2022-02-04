from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from lightdb import LightDB
import random
import json

router = APIRouter()
templates = Jinja2Templates(directory="templates")

database = LightDB("data.json")


def get_origin(request):
    return "/".join(str(request.url).split("/")[0:3])


def get_examples(key):
    data = database.get(key)

    return [random.choice(data) for i in range(3)], len(data)


def get_total_items_length():
    len_users = len(database.get("users"))
    len_todos = len(database.get("todos"))
    len_posts = len(database.get("posts"))
    len_comments = len(database.get("comments"))
    len_photos = len(database.get("photos"))

    return len_users + len_todos + len_posts + len_comments + len_photos


def get_id(item):
    return item["id"]


def get_user_id(item):
    return item["userId"]


@router.get("/")
async def index(request: Request):
    user = random.choice(database.get("users"))
    return templates.TemplateResponse("index.html", {"request": request, "user": user, "json_data": json.dumps(user)})


@router.get("/about")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@router.get("/docs")
async def docs(request: Request):
    len_users = len(database.get("users"))
    len_todos = len(database.get("todos"))
    len_posts = len(database.get("posts"))
    len_comments = len(database.get("comments"))
    len_photos = len(database.get("photos"))

    total_items = len_users + len_todos + len_posts + len_comments + len_photos

    resources = [
        {"label": "Users", "slug": "users", "amount": len_users},
        {"label": "Todos", "slug": "todos", "amount": len_todos},
        {"label": "Posts", "slug": "posts", "amount": len_posts},
        {"label": "Comments", "slug": "comments", "amount": len_comments},
        {"label": "Photos", "slug": "photos", "amount": len_photos},
        {"label": "Random", "slug": "random"},
        {"label": "All database", "slug": "all", "amount": total_items}
    ]
    return templates.TemplateResponse("docs/index.html", {"request": request, "resources": resources})


@router.get("/docs/users")
async def docs_users(request: Request):
    example_users, length = get_examples("users")
    examples_users_ids = map(get_id, example_users)

    return templates.TemplateResponse("docs/users.html", {"request": request, "length": length, "examples": examples_users_ids})


@router.get("/docs/todos")
async def docs_todos(request: Request):
    examples_todos, length = get_examples("todos")
    example_todos_ids = map(get_id, examples_todos)
    example_users_todos = map(get_user_id, examples_todos)

    return templates.TemplateResponse("docs/todos.html",
                                      {"request": request, "length": length, "examples": example_todos_ids, "examples_users": example_users_todos})


@router.get("/docs/posts")
async def docs_posts(request: Request):
    examples_posts, length = get_examples("posts")
    example_posts_ids = map(lambda item: item["slug"], examples_posts)
    example_users_posts = map(get_user_id, examples_posts)

    return templates.TemplateResponse("docs/posts.html",
                                      {"request": request, "length": length, "examples": example_posts_ids, "examples_users": example_users_posts})


@router.get("/docs/comments")
async def docs_comments(request: Request):
    example_comments, length = get_examples("comments")
    example_comments_id = map(get_id, example_comments)
    examples_user_comments = map(get_user_id, example_comments)

    return templates.TemplateResponse("docs/comments.html",
                                      {"request": request, "length": length, "examples": example_comments_id, "examples_users":
                                          examples_user_comments})


@router.get("/docs/photos")
async def docs_photos(request: Request):
    example_comments, length = get_examples("photos")
    example_comments_id = map(get_id, example_comments)
    examples_user_comments = map(get_user_id, example_comments)

    return templates.TemplateResponse("docs/photos.html",
                                      {"request": request, "length": length, "examples": example_comments_id, "examples_users":
                                          examples_user_comments})


@router.get("/docs/random")
async def docs_random(request: Request):
    return templates.TemplateResponse("docs/random.html", {"request": request, "length": get_total_items_length()})


@router.get("/docs/all")
async def docs_all(request: Request):
    return templates.TemplateResponse("docs/all.html", {"request": request, "length": get_total_items_length()})


@router.get("/playground")
async def playground(request: Request):
    return templates.TemplateResponse("playground.html", {"request": request, "origin": get_origin(request)})
