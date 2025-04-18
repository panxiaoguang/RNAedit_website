import reflex as rx

config = rx.Config(
    app_name="MAIRE",
    tailwind={
        "theme": {
            "extend": {
            },
        },
        "plugins": ["@tailwindcss/typography"],
    },
)
