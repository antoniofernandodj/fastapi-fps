from fastapi import FastAPI
from . import user

import tomli


with open("pyproject.toml", "rb") as toml_file:
    toml_data = tomli.load(toml_file)
    version = toml_data["tool"]["poetry"]["version"]
    description = toml_data["tool"]["poetry"]["description"]
    name = toml_data["tool"]["poetry"]["name"]


def init_app(app: FastAPI):
    app.include_router(user.router)

    @app.get("/")
    async def index():

        return {
            "version": version,
            "name": name,
            "description": description,
            "links": [
                {"rel": "self", "href": "/"},
            ]
            + [
                {
                    "rel": route.path.split("/")[1],  # type: ignore
                    "href": route.path,  # type: ignore
                }
                for route in app.router.routes
                if route.path != "/"  # type: ignore
            ],
            "actions": [
                {
                    "name": (
                        route.name.replace(  # type: ignore
                            "_", " "
                        ).capitalize()
                    ),
                    "methods": list(route.methods),  # type: ignore
                    "path": route.path,  # type: ignore
                }
                for route in app.router.routes  # type: ignore
            ],
        }
