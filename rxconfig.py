import reflex as rx

config = rx.Config(
    app_name="MAIRE",
    show_built_with_reflex=False, ## to remove the badge
    tailwind={
        "theme": {
            "extend": {
            },
        },
        "plugins": ["@tailwindcss/typography"],
    },
)
