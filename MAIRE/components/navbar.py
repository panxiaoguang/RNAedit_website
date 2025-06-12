import reflex as rx


class NavbarState(rx.State):
    reverse: bool = False


def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(
       rx.text(text, class_name="text-base text-gray-500"),
        href=url,
    )


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.link(
                rx.image(src="/logo.png", width="150px", height="50px"),
                href="/"
            ),
            rx.hstack(
                navbar_link("Home", "/"),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.button(
                            rx.text(
                                "Search",
                                class_name="text-base text-gray-500",
                            ),
                            rx.icon(
                                "chevron-down",
                                color="gray",
                                class_name="chevron transition-transform duration-200 ease-in-out",
                            ),
                            variant="ghost",
                            weight="medium",
                            class_name="cursor-pointer",
                        ),
                        style={
                            "&[data-state='open'] .chevron": {
                                "transform": "rotate(180deg)",
                            },
                        },
                    ),
                    rx.menu.content(
                        rx.menu.item(
                            navbar_link("Search by Position", "/search_by_position"),
                             
                        ),
                        rx.menu.item(
                            navbar_link("View by Gene", "/view_by_gene"),
                        ),
                        color_scheme="gray",
                        variant="soft",
                        align="center"
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
