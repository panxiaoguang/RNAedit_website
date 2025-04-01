import reflex as rx
from ..template import template
from .view_by_genes import ViewByGeneState
from ..utils import render_image
import plotly.graph_objects as go


class Render_gene_view(rx.State):
    figure: go.Figure = go.Figure()

    @rx.event
    async def get_query_test_data(self):
        query_parms = await self.get_state(ViewByGeneState)
        fig = await render_image(query_parms.gene_symbol)
        self.figure = fig
        yield


@rx.page("/render_by_gene", on_load=Render_gene_view.get_query_test_data)
@template
def render_by_gene() -> rx.components:
    return rx.flex(
        rx.plotly(data=Render_gene_view.figure, width="100%"),
        width="100%",
        align="center",
        justify="center",
        class_name="mt-20",
    )
