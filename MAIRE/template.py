from typing import Callable

import reflex as rx

from .components import navbar, footer_v2


def template(page: Callable[[], rx.Component]) -> rx.Component:
    def wrapper(*args, **kwargs):
        return rx.vstack(
            navbar(),
            page(*args, **kwargs),
            footer_v2(),
            width="100%",
        )
    return wrapper
