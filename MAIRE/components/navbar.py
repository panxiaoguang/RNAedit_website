import reflex as rx
from ..components.navmenu import nav_menu


def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(
        rx.text(text, class_name="text-base text-gray-500"), href=url, underline="none"
    )


def resource_item(text: str, url: str):
    return rx.el.li(
        rx.link(
            rx.box(
                rx.text(
                    text, class_name="text-base text-gray-500 py-1 hover:bg-gray-100"
                ),
            ),
            underline="none",
            href=url,
        ),
    )


def doc_section():
    return nav_menu.content(
        rx.el.ul(
            resource_item("Search by Position", "/search_by_position"),
            resource_item("View by Gene", "/view_by_gene"),
        ),
    )


def new_menu_trigger(title: str) -> rx.Component:
    return nav_menu.trigger(
        rx.box(
            rx.text(
                title,
                class_name="font-small text-gray-500 transition-colors cursor-pointer",
            ),
            rx.icon(
                "chevron-down",
                class_name="chevron size-5 py-1 mr-0 transition-colors ",
            ),
            class_name="flex flex-row items-center gap-x-1 group user-select-none",
            on_click=rx.stop_propagation,
        ),
        style={
            "&[data-state='open'] .chevron": {
                "transform": "rotate(180deg)",
            },
        },
    )


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.link(rx.image(src="/logo.png", width="150px", height="50px"), href="/"),
            rx.hstack(
                navbar_link("Home", "/"),
                nav_menu.root(
                    nav_menu.list(
                        nav_menu.item(
                            new_menu_trigger("Search"),
                            doc_section(),
                        ),
                    ),
                    rx.el.div(
                        nav_menu.viewport(),
                        class_name="top-full left-0 absolute flex justify-start w-full",
                    ),
                ),
                navbar_link("JBrowse", "/jbrowse_view"),
                navbar_link("Publications", "/pub"),
                navbar_link("Help", "/help"),
                class_name="space-x-4 justify-items-end py-5",
            ),
            class_name="px-9  justify-between content-start items-center",
        ),
        class_name="fixed top-0 bg-white z-50 border-b border-gray-200 h-[69px] navbar",
        width="100%",
    )
