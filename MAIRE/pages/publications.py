import reflex as rx
from ..template import template


def pub_view(picture:str, content:str)->rx.Component:
    return rx.card(
    rx.flex(
        rx.inset(
            rx.box(
                background=f"center/cover url('{picture}')",
                height="100%",
            ),
            width="20%",
            side="left",
            pr="current",
        ),
        rx.text(
            content,
        ),
        direction="row",
        width="100%",
    ),
    width="60vw",
)

class pubState(rx.State):
    pass

@rx.page(route="/pub",title="Publications",)
@template
def publications() -> rx.Component:
    
    return rx.container(
        rx.flex(
            rx.heading("Publications",
            size="6",
            align="left",),
            pub_view("/logo.png","this part to show our articles"),
            direction="column",
            spacing="2"
        ),
        width="100%",
        class_name="mt-20",)
