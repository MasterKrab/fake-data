from utils.avatar import create_avatar
from mimesis import Generic
from mimesis.locales import Locale
from utils.random_utils import random_boolean
from utils.read import get_read_time
from nanoid import generate
from slugify import slugify
from lightdb import LightDB
from datetime import datetime
import random
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")
IMAGES_URL = os.getenv("IMAGES_URL")

generic = Generic(locale=Locale.EN)


def create_user():
    name = generic.person.full_name()

    return {
        'id': generate(size=10),
        'name': name,
        "username": generic.person.username(),
        "avatar": create_avatar(name),
        'email': generic.person.email(),
        "gender": generic.person.gender(),
        'phone': generic.person.telephone(),
        "occupation": generic.person.occupation(),
        "nationality": generic.person.nationality(),
    }


def create_todo(users):
    user = random.choice(users)

    return {
        "userId": user["id"],
        "id": generate(),
        "content": generic.text.text(),
        "done": random_boolean(),
    }


def create_comment(users, post_slug):
    user = random.choice(users)

    return {
        "userId": user["id"],
        "id": generate(),
        "postSlug": post_slug,
        "content": generic.text.text(),
        "createdAt": generic.datetime.datetime().isoformat(),
    }


def generate_title():
    return generic.text.text(random.randint(1, 2))


def create_posts(users, amount):
    titles = set()
    posts = []
    comments = []

    for i in range(amount):
        user = random.choice(users)

        title = generate_title()

        while title in titles:
            title = generate_title()

        titles.add(title)

        slug = slugify(title)

        current_comments = [create_comment(users, slug) for i in range(random.randint(0, 10))]

        comments += current_comments

        content = generic.text.text(quantity=random.randint(50, 60))

        posts.append({
            "userId": user["id"],
            "slug": slug,
            "title": title,
            "content": content,
            "readTime": f"{get_read_time(content)} minutes",
            "createdAt": generic.datetime.datetime().isoformat(),
            "comments": list(map(lambda comment: comment["id"], current_comments)),
        })

    return posts, comments


def create_photo(users, filename):
    user = random.choice(users)

    visits = random.randint(0, 100)

    return {
        "userId": user["id"],
        "id": generate(),
        "title": generic.text.title(),
        "description": generic.text.text(quantity=random.randint(5, 10)),
        "url": f"{IMAGES_URL}/{filename}.png",
        "createdAt": generic.datetime.datetime().isoformat(),
        "visits": visits,
        "likes": random.randint(0, visits // 2),
        "disLikes": random.randint(0, visits // 4),
    }


USER_AMOUNT = 250
TODO_AMOUNT = 1000
POSTS_AMOUNT = 100
PHOTO_AMOUNT = 500


def create_database():
    start_time = datetime.now()

    print("Creating database...")

    users = [create_user() for i in range(USER_AMOUNT)]

    print(f"Created {USER_AMOUNT} users")

    todos = [create_todo(users) for i in range(TODO_AMOUNT)]

    print(f"Created {TODO_AMOUNT} todos")

    posts, comments = create_posts(users, POSTS_AMOUNT)

    print(f"Created {POSTS_AMOUNT} posts and {len(comments)} comments")

    photos = [create_photo(users, i) for i in range(1, PHOTO_AMOUNT + 1)]

    print(f"Created {PHOTO_AMOUNT} photos")

    database = LightDB("data.json")

    database.reset()

    database.set("users", users)
    database.set("todos", todos)
    database.set("posts", posts)
    database.set("comments", comments)
    database.set("photos", photos)

    database.save()

    print(f"Database created in {datetime.now() - start_time} seconds")
