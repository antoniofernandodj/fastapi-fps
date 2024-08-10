from fastapi import FastAPI


def create_app(args):
    app = FastAPI()
    from fps_src import routes
    routes.init_app(app)
    return app
