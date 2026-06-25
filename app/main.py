from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import features, health, sessions
from app.db.database import Base, engine
from app.web import routes as web_routes


def create_app() -> FastAPI:
    Base.metadata.create_all(bind=engine)

    app = FastAPI(title="Code Foundry")
    app.mount("/static", StaticFiles(directory="app/web/static"), name="static")
    app.include_router(web_routes.router)
    app.include_router(health.router)
    app.include_router(features.router)
    app.include_router(sessions.router)
    return app


app = create_app()
