import reflex as rx

config = rx.Config(
    app_name="MAIRE",
    show_built_with_reflex=False, ## to remove the badge
    db_url = "postgresql://postgres.qibqhgitlhnsbmuryfbw:rLh7XyDkrhn058nE@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres",
    tailwind={
        "theme": {
            "extend": {
            },
        },
        "plugins": ["@tailwindcss/typography"],
    },
)
