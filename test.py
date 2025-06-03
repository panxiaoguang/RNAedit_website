import reflex as rx
from types import SimpleNamespace

class AGRenderers(SimpleNamespace):
    link = rx.vars.function.ArgsFunctionOperation.create(
        ("params",),
        rx.link(
            rx.Var("params.value"),
            href=rx.Var("params.value", _var_type=str),
            target="_blank",
        ),
    )

print(AGRenderers.link)