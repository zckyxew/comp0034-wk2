from flask import current_app


@current_app.route('/')
def hello():
    return f"Hello!"

