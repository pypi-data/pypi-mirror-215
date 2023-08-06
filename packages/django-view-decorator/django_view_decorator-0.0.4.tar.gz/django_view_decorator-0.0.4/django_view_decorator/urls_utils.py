from collections.abc import Sequence
from importlib import import_module

from django.urls import include
from django.urls import URLPattern
from django.urls import URLResolver


def include_view_urls(
    *,
    extra_modules: list[str] | None = None,
) -> tuple[Sequence[URLResolver | URLPattern], str | None, str | None]:
    """
    Include the view urls from the registry discovered by django_view_decorator, and
    optionally from the given modules.
    :param extra_modules: A list of modules to import before including the view urls.
    :return: A tuple of (urlpatterns, app_name, namespace) (result from calling
        include())
    """
    if extra_modules:
        for module in extra_modules:
            import_module(f"{module}")

    return include("django_view_decorator.urls")
