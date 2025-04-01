from typing import Callable

import reflex as rx

from .components import navbar, footer_v2


def template(page: Callable[[], rx.Component]) -> rx.Component:
    return rx.vstack(
        navbar(),
        page(),
        footer_v2(),
        width="100%",
    )
