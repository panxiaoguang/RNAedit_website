import reflex as rx

config = rx.Config(
    app_name="MAIRE",
    #db_url="postgresql+psycopg://postgres:admin@localhost:5432/reflexdb",
    db_url="postgresql://postgres.qibqhgitlhnsbmuryfbw:rLh7XyDkrhn058nE@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres",
    tailwind={
        "theme": {
            "extend": {
            },
        },
        "plugins": ["@tailwindcss/typography"],
    },
    backend_port=8010
)
