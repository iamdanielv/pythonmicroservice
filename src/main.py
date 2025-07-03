"""A Sample FastAPI Microservice"""

import logging
import os

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader

from src.config import LogConfig, Settings
from src.models import DefaultMessage
from src.routers.todo import router as todo_router
from src.routers.todo import todo_list

# Initialize configuration
settings = Settings()
log_config = LogConfig()
log_config.configure()

# Initialize logger
logger = logging.getLogger("todo_app")

app = FastAPI(title=settings.title, summary=settings.summary)
app.mount(
    "/styles",
    StaticFiles(directory=os.path.join(os.getcwd(), "src/resources/styles")),
    name="styles",
)
app.mount(
    "/scripts",
    StaticFiles(directory=os.path.join(os.getcwd(), "src/resources/scripts")),
    name="scripts",
)

# Use the router
app.include_router(todo_router, tags=["API"])


env = Environment(
    loader=FileSystemLoader(os.path.join(os.getcwd(), "src/templates"))
)
template = env.get_template("index.html")


# #########################
# # SETUP the application #
# #########################
def get_settings():
    return settings


@app.get("/status")
async def get_status():
    """useful when using Docker or Kubernetes to see if the application is up"""
    return DefaultMessage(message="OK")


@app.get("/")
async def root(request: Request):
    return HTMLResponse(content=template.render(todo_list=todo_list))


if __name__ == "__main__":
    RELOAD = not settings.is_prod

    print(
        f"App: {settings.title}"
        f" -- Host: {settings.host}:{settings.port} "
        f"Reload: {RELOAD}"
    )
    uvicorn.run(app, host=settings.host, port=settings.port, reload=RELOAD)
