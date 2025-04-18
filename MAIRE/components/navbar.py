import reflex as rx

class NavbarState(rx.State):
    reverse: bool = False

    @rx.event
    def toggle_reverse(self, value:bool):
        self.reverse = value

def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(rx.text(text, class_name="text-base text-gray-500"), href=url)


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.image(src="/logo.png", width="150px", height="50px"),
            rx.hstack(
                navbar_link("Home", "/"),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.button(
                            rx.text(
                                "Search",
                                class_name="text-base text-gray-500",
                            ),
                            rx.cond(
                                NavbarState.reverse,
                                rx.icon("chevron-up",color="gray"),
                                rx.icon("chevron-down",color="gray"),
                            ),
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
                    on_open_change=NavbarState.toggle_reverse,
                ),
                navbar_link("JBrowse", "/jbrowse_view"),
                navbar_link("Publications", "/#"),
                #navbar_link("Help", "/help"),
                class_name="space-x-4 justify-items-end py-5",
            ),
            class_name="px-9  justify-between content-start items-center",
        ),
        class_name="shadow-md fixed top-0 bg-white z-50",
        width="100%",
    )
