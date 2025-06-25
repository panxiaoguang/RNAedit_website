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
        class_name="hover:-translate-y-0.5 hover:scale-105 transition delay-150 duration-300 ease-in-out",
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
                "https://tncache1-f1.v3mh.com/image/2025/06/25/dd4b59bd084d51dd5b6548c51863d892.jpeg",
                rx.flex(
                    rx.text(
                        "Li, C.,Lv, W., He, Z., Pan, X., et al. Landscape of A-I RNA editing in mouse, pig, macaque, and human brains. Nucleic Acids Res. (2025)."
                    ),
                    rx.text("Accepted.", color_scheme="green"),
                    rx.link(
                        "click to view",
                        href="https://academic.oup.com/nar/article/53/11/gkaf534/8166790",
                        is_external=True,
                    ),
                    direction="column",
                    width="75%",
                ),
            ),
            pub_view(
                "https://tncache1-f1.v3mh.com/image/2025/06/25/557b6fd28fc8323e6f1156cc1ec79da2.jpg",
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
            class_name="pt-[32px]",
        ),
        width="100%",
        class_name="h-[calc(100vh-10vh-80px)] mt-[69px]",
    )
