import reflex as rx


def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(rx.text(text, class_name="text-base text-gray-500"), href=url)


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.heading("RNAediting", class_name="text-2xl font-bold"),
            rx.hstack(
                navbar_link("Home", "/"),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.button(
                            rx.text(
                                "Search",
                                class_name="text-base text-gray-500",
                            ),
                            rx.icon("chevron-down",color="gray"),
                            variant="ghost",
                            weight="medium",
                            class_name="cursor-pointer",
                        ),
                    ),
                    rx.menu.content(
                        rx.menu.item(
                            navbar_link("Search by Position", "/search_by_position"),
                        ),
                        rx.menu.item(
                            navbar_link("View by Gene", "/view_by_gene"),
                        ),
                    ),
                ),
                navbar_link("JBrowse", "/jbrowse_view"),
                navbar_link("Publications", "/#"),
                navbar_link("Help", "/help"),
                class_name="space-x-4 justify-items-end ",
            ),
            class_name="px-9 py-5 justify-between content-start items-center",
        ),
        class_name="shadow-md fixed top-0 bg-white",
        width="100%",
    )
