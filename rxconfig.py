
import reflex as rx
config = rx.Config(
    app_name="RNAedit",
    db_url="sqlite:///reflex.db",
    tailwind={
        "theme": {
            "extend": {},
        },
        "plugins": ["@tailwindcss/typography"],
    },
)