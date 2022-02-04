from database import create_database
from os import path


def create_app():
    from fastapi import FastAPI
    from routes import api, client
    from fastapi.staticfiles import StaticFiles

    app = FastAPI(docs_url=None, redoc_url=None)

    app.mount("/avatars", StaticFiles(directory="avatars"), name="avatars")
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(api.router, prefix="/api")
    app.include_router(client.router)

    return app


def create_server():
    if not path.exists("data.json"):
        create_database()

    return create_app()


app = create_server()
