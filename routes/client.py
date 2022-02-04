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

    return [random.choice(data) for i in range(3)]


len_users = len(database.get("users"))
len_todos = len(database.get("todos"))
len_posts = len(database.get("posts"))
len_comments = len(database.get("comments"))
len_photos = len(database.get("photos"))

total_items = len_users + len_todos + len_posts + len_comments + len_photos


def get_ids(data):
    return list(map(lambda item: item["id"], data))


def get_user_ids(data):
    return list(map(lambda item: item["userId"], data))


@router.get("/")
async def index(request: Request):
    user = random.choice(database.get("users"))
    return templates.TemplateResponse("index.html", {"request": request, "user": user, "json_data": json.dumps(user)})


@router.get("/about")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


resources = [
    {"label": "Users", "slug": "users", "amount": len_users},
    {"label": "Todos", "slug": "todos", "amount": len_todos},
    {"label": "Posts", "slug": "posts", "amount": len_posts},
    {"label": "Comments", "slug": "comments", "amount": len_comments},
    {"label": "Photos", "slug": "photos", "amount": len_photos},
    {"label": "Random", "slug": "random"},
    {"label": "All database", "slug": "all", "amount": total_items}
]


@router.get("/docs")
async def docs(request: Request):
    return templates.TemplateResponse("docs/index.html", {"request": request, "resources": resources})


example_users = get_examples("users")
examples_users_ids = get_ids(example_users)


@router.get("/docs/users")
async def docs_users(request: Request):
    return templates.TemplateResponse("docs/users.html", {"request": request, "length": len_users, "examples": examples_users_ids})


examples_todos = get_examples("todos")
example_todos_ids = get_ids(examples_todos)
example_users_todos = get_user_ids(examples_todos)


@router.get("/docs/todos")
async def docs_todos(request: Request):
    return templates.TemplateResponse("docs/todos.html",
                                      {"request": request, "length": len_todos, "examples": example_todos_ids, "examples_users": example_users_todos})


examples_posts = get_examples("posts")
example_posts_ids = list(map(lambda item: item["slug"], examples_posts))
example_users_posts = get_user_ids(examples_posts)


@router.get("/docs/posts")
async def docs_posts(request: Request):
    return templates.TemplateResponse("docs/posts.html",
                                      {"request": request, "length": len_posts, "examples": example_posts_ids, "examples_users": example_users_posts})


example_comments = get_examples("comments")
example_comments_id = get_ids(example_comments)
examples_user_comments = get_user_ids(example_comments)


@router.get("/docs/comments")
async def docs_comments(request: Request):
    return templates.TemplateResponse("docs/comments.html",
                                      {"request": request, "length": len_comments, "examples": example_comments_id, "examples_users":
                                          examples_user_comments})


example_photos = get_examples("photos")
example_photos_id = get_ids(example_photos)
examples_user_photos = get_user_ids(example_photos)


@router.get("/docs/photos")
async def docs_photos(request: Request):
    return templates.TemplateResponse("docs/photos.html",
                                      {"request": request, "length": len_photos, "examples": example_photos_id, "examples_users":
                                          examples_user_photos})


@router.get("/docs/random")
async def docs_random(request: Request):
    return templates.TemplateResponse("docs/random.html", {"request": request, "length": total_items})


@router.get("/docs/all")
async def docs_all(request: Request):
    return templates.TemplateResponse("docs/all.html", {"request": request, "length": total_items})


@router.get("/playground")
async def playground(request: Request):
    return templates.TemplateResponse("playground.html", {"request": request, "origin": get_origin(request)})
