import reflex as rx

class TopBannerBasic(rx.ComponentState):
    hide: bool = False

    @rx.event
    def toggle(self):
        self.hide = not self.hide

    @classmethod
    def get_component(cls, **props):
        return rx.cond(
            ~cls.hide,
            rx.hstack(
                rx.flex(
                    rx.badge(
                        rx.icon("megaphone", size=18),
                        padding="0.30rem",
                        radius="full",
                    ),
                    rx.text(
                        "Our Publication has been accepted - 2025-06-12 ",
                        rx.link(
                            "DOI!",
                            href="https://www.nature.com/articles/s42003-021-02238-3",
                            underline="always",
                            display="inline",
                            underline_offset="2px",
                        ),
                        weight="medium",
                    ),
                    align="center",
                    margin="auto",
                    spacing="3",
                ),
                rx.icon(
                    "x",
                    cursor="pointer",
                    justify="end",
                    flex_shrink=0,
                    on_click=cls.toggle,
                ),
                wrap="nowrap",
                # position="fixed",
                justify="between",
                width="100%",
                # top="0",
                align="center",
                left="0",
                # z_index="50",
                padding="1rem",
                background=rx.color("accent", 4),
                **props,
            )
        )


top_banner_basic = TopBannerBasic.create