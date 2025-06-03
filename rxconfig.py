import reflex as rx

config = rx.Config(
    app_name="MAIRE",
    show_built_with_reflex=False, ## to remove the badge
    db_url="postgresql+psycopg2://postgres.qibqhgitlhnsbmuryfbw:CLelSV6CMlh3KI3g@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres",
    tailwind={
        "theme": {
            "extend": {
            },
        },
        "plugins": ["@tailwindcss/typography"],
    },
)
