from dataclasses import dataclass, field

import reflex as rx
from reflex.constants.colors import Color

@dataclass
class FooterV1Style:
    base: dict[str, str] = field(
        default_factory=lambda: {
            "width": "100%",
            "height": "100%",
            "wrap": "wrap",
            "gap": "1em",
            "padding": "1em",
        },
    )

    title: dict[str, str] = field(
        default_factory=lambda: {
            "color": rx.color("slate", 12),
            "weight": "bold",
            "size": "2",
        },
    )

    link: dict[str, str] = field(
        default_factory=lambda: {
            "color": rx.color("slate", 11),
            "weight": "medium",
            "size": "2",
        },
    )

    stack: dict[str, str] = field(
        default_factory=lambda: {"min_width": "200px", "padding": "1em 0em"},
    )

    icon: dict[str, str] = field(
        default_factory=lambda: {
            "size": 20,
            "color": rx.color("slate", 10),
            "_hover": {
                "color": rx.color("slate", 12),
                "fill": rx.color("slate", 12),
            },
            "fill": rx.color("slate", 10),
            "cursor": "pointer",
        },
    )


FooterV1Style = FooterV1Style()


active: Color = rx.color("slate", 12)
passive: Color = rx.color("slate", 10)


@dataclass
class FooterV2Style:
    base: dict[str, str] = field(
        default_factory=lambda: {
            "width": "100%",
            "height": "20vh",
            "align": "center",
            "justify": "center",
            "padding": "0em 1em",
        },
    )

    content: dict[str, str] = field(
        default_factory=lambda: {
            "width": "100%",
            "max_width": "80%",
            "justify": "between",
            "align": "center",
            "padding": "1em 0em",
        },
    )

    link: dict[str, str] = field(
        default_factory=lambda: {"color": passive, "size": "2"},
    )

    brand: dict[str, str] = field(
        default_factory=lambda: {"color": active, "size": "2"},
    )


FooterV2Style = FooterV2Style()


def media(name: str, href: str) -> rx.Component:
    return rx.link(rx.text(name, **FooterV1Style.link), href= href)


def footer_v2() -> rx.Component:
    return rx.vstack(
        rx.divider(color=rx.color("slate", 11)),
        rx.hstack(
            rx.text("© 2025, Department of Biomedicine, Aarhus University", **FooterV2Style.brand),
            rx.hstack(media("Github","https://github.com/panxiaoguang"), media("Blog","https://xiaohanys.top"), media("zhihu","https://www.zhihu.com/people/luo-tian-bao-92")),
            **FooterV2Style.content,
        ),
        **FooterV2Style.base,
    )
