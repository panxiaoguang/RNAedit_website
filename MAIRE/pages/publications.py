import reflex as rx
from ..template import template
from typing import Callable


def pub_view(picture: str, content: Callable[[], rx.Component]) -> rx.Component:
    return rx.card(
        rx.flex(
            rx.inset(
                rx.box(
                    background=f"center/cover url('{picture}')",
                    height="180px",
                    width="145px",
                ),
                side="left",
                pr="current",
            ),
            content,
            direction="row",
            width="100%",
        ),
        width="60vw",
        class_name="animate__animated animate__bounceInDown",
    )


class pubState(rx.State):
    pass


@rx.page(
    route="/pub",
    title="Publications",
)
@template
def publications() -> rx.Component:
    return rx.container(
        rx.flex(
            rx.heading(
                "Publications",
                size="6",
                align="left",
            ),
            pub_view(
                "/NAR_cover.jpeg",
                rx.flex(
                    rx.text(
                        "Li, C.,Lv, W., He, Z., et al. Brain-wide A-I RNA Editing Analysis in Macaque and Insights into Nervous System Evolution and Functions. Nucleic Acids Res. (2025)."
                    ),
                    rx.text("In review.", color_scheme="orange"),
                    rx.link("click to view", href="#"),
                    direction="column",
                    width="75%",
                ),
            ),
            pub_view(
                "/CB_cover.png",
                rx.flex(
                    rx.text(
                        "Huang, J., Lin, L., Dong, Z. et al. A porcine brain-wide RNA editing landscape. Commun Biol 4, 717 (2021)."
                    ),
                    rx.link(
                        "click to view",
                        href="https://www.nature.com/articles/s42003-021-02238-3",
                        is_external=True,
                    ),
                    direction="column",
                    width="75%",
                ),
            ),
            direction="column",
            spacing="2",
        ),
        width="100%",
        class_name="mt-20",
    )
