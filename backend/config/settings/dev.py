from .base import *  # noqa: F403


DEBUG = True
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["localhost", "127.0.0.1", "testserver"])  # noqa: F405

CORS_ALLOW_ALL_ORIGINS = not CORS_ALLOWED_ORIGINS  # noqa: F405
