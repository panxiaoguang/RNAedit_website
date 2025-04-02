import reflex as rx
from ..template import template
from .view_by_genes import ViewByGeneState
from ..utils import parse_gene_data, create_visualization
import plotly.graph_objects as go
from ..models import Gene, Transcript
import sqlalchemy 


class Render_gene_view(rx.State):
    figure: go.Figure = go.Figure()
    showfigure: bool = False
    _trans_len: int = 0
    @rx.event
    async def get_query_test_data(self):
        self.showfigure = False
        yield
        query_parms = await self.get_state(ViewByGeneState)
        if query_parms.gene_symbol=="":
            yield rx.toast("Please input gene symbol")
        else:
            with rx.session() as session:
                gene_data = session.exec(
                    Gene.select().options(
                        sqlalchemy.orm.selectinload(Gene.transcripts).options(
                            sqlalchemy.orm.selectinload(Transcript.cdses),
                            sqlalchemy.orm.selectinload(Transcript.utres)
                    )).where(
                        Gene.symbol == query_parms.gene_symbol
                    )
                ).one()
            transcripts = parse_gene_data(gene_data)
            self._trans_len = len(transcripts)
            self.figure = create_visualization(transcripts)
            self.showfigure = True
            yield
    @rx.var
    def get_figure_width(self) -> str:
        height = 40 * self._trans_len
        return f"{height}px"


@rx.page("/render_by_gene", on_load=Render_gene_view.get_query_test_data)
@template
def render_by_gene() -> rx.components:
    return rx.flex(
        rx.cond(Render_gene_view.showfigure, 
        rx.plotly(data=Render_gene_view.figure, width="100%", height=Render_gene_view.get_figure_width),
        rx.skeleton(rx.plotly(data=Render_gene_view.figure, width="95%", height="450px"),),
        ),
        align="center",
        justify="center",
        class_name="mt-20 w-full",
    )
