import reflex as rx
from ..template import template
from typing import List
from ..models import Gene
from ..utils import create_visualization_2
import plotly.graph_objects as go


def generate_geneview_schema(records: Gene):
    transcript_data = records.transcripts
    rna_editing_data = records.rnaediting  ## List
    transcript_list = []
    level_dot_data = []
    for transcript in transcript_data:
        if not transcript.cdses and not transcript.utres:
            continue
        else:
            transcript_dict = {
                "id": transcript.transcript_id,
                "gene_name": records.symbol,
                "gene_type": transcript.transcript_type,
                "strand": "+" if records.strand == 1 else "-",
                "coding_exons": [(cds.start, cds.end) for cds in transcript.cdses],
                "utrs": [("UTR", utr.start, utr.end) for utr in transcript.utres],
                "transcript_start": transcript.start,
                "transcript_end": transcript.end,
            }
            transcript_list.append(transcript_dict)
    ## WE need get all editing levels
    for rna_editing in rna_editing_data:
        x_coord = rna_editing.position
        for level in rna_editing.editinglevel:
            level_dict = {
                    "x": x_coord,
                    "tissue_name": level.tissue.name,
                    "y": round(level.level, 3),
                }
            level_dot_data.append(level_dict)
    return transcript_list, level_dot_data


class ViewByGeneState(rx.State):
    orngism_name: str = "Monkey"
    genome_version: str
    gene_symbol: str
    _transcript_data: List[dict] = []
    _level_dot_data: List[dict] = []
    figure: go.Figure = go.Figure()
    _trans_len: int = 0
    show_figure: bool = False

    @rx.event
    async def get_gene_view_data(self):
        self.show_figure = True
        yield
        with rx.session() as session:
            records = session.exec(Gene.select().where(Gene.symbol == self.gene_symbol).limit(5)).first()
            if records is not None:
                self._transcript_data, self._level_dot_data = generate_geneview_schema(
                records
                )
                self.figure = create_visualization_2(self._transcript_data, self._level_dot_data)
                self._trans_len = len(self._transcript_data)
                self.show_figure = False
                yield
            else:
                self._transcript_data = []
                self._level_dot_data = []
                self.show_figure = False
                yield rx.toast("Gene not found!")
            
    @rx.event
    def clear_data(self):
        self._transcript_data = []
        self._level_dot_data = []
        self._trans_len = 0
        self.show_figure = False 
    @rx.var
    def show_gene_view(self) -> bool:
        if self._trans_len == 0:
            return True
        else:
            return False

    @rx.var
    def get_figure_width(self) -> str:
        height = 100 * self._trans_len + 400
        return f"{height}px"

    @rx.event
    def show_example(self):
        self.genome_version = "macFas5"
        self.gene_symbol = "ACTA1"
        return ViewByGeneState.get_gene_view_data()
@rx.page("/view_by_gene")
@template
def view_by_genes() -> rx.Component:
    return rx.flex(
        rx.container(
            rx.vstack(
                rx.heading("View RNA Editing for a given gene:"),
                rx.divider(),
                rx.flex(
                    rx.flex(
                        rx.text("Organism Name:"),
                        rx.select.root(
                            rx.select.trigger(placeholder="Select a Organism Name"),
                            rx.select.content(
                                rx.select.group(
                                    rx.select.item("Monkey", value="Monkey"),
                                    rx.select.item(
                                        "Human", value="Human", disabled=True
                                    ),
                                    rx.select.item(
                                        "Mouse", value="Mouse", disabled=True
                                    ),
                                ),
                            ),
                            value=ViewByGeneState.orngism_name,
                            on_change=ViewByGeneState.set_orngism_name,
                            width="20%",
                        ),
                        spacing="5",
                        align="center",
                    ),
                    rx.flex(
                        rx.text("Genome Version:"),
                        rx.select.root(
                            rx.select.trigger(placeholder="Select a Genome Version"),
                            rx.select.content(
                                rx.match(
                                    ViewByGeneState.orngism_name,
                                    (
                                        "Monkey",
                                        rx.select.group(
                                            rx.select.item("macFas5", value="macFas5"),
                                        ),
                                    ),
                                    (
                                        "Human",
                                        rx.select.group(
                                            rx.select.item("GRCh38", value="GRCh38"),
                                            rx.select.item("GRCh37", value="GRCh37"),
                                        ),
                                    ),
                                    (
                                        "Mouse",
                                        rx.select.group(
                                            rx.select.item("GRCm38", value="GRCm38"),
                                            rx.select.item("GRCm39", value="GRCm39"),
                                        ),
                                    ),
                                ),
                            ),
                            value=ViewByGeneState.genome_version,
                            on_change=ViewByGeneState.set_genome_version,
                            width="20%",
                        ),
                        spacing="5",
                        align="center",
                    ),
                    rx.flex(
                        rx.text("Genomic Name:"),
                        rx.input(
                            placeholder="Gene Symbol like GRIA2,TP53,SOD1 ...",
                            value=ViewByGeneState.gene_symbol,
                            on_blur=ViewByGeneState.set_gene_symbol,
                            width="50%",
                        ),
                        spacing="5",
                        align="center",
                    ),
                    rx.hstack(
                        rx.button(
                            "Search",
                            color_scheme="iris",
                            cursor="pointer",
                            on_click=ViewByGeneState.get_gene_view_data,
                            loading=ViewByGeneState.show_figure,
                        ),
                        rx.button(
                            "Reset",
                            color_scheme="orange",
                            cursor="pointer",
                            on_click=ViewByGeneState.clear_data,
                        ),
                        rx.button(
                            "Example",
                            color_scheme="violet",
                            cursor="pointer",
                            on_click=ViewByGeneState.show_example
                        )
                    ),
                    direction="column",
                    width="100%",
                    spacing="3",
                ),
            ),
            width="100%",
            class_name="mt-20",
        ),
        rx.cond(
            ViewByGeneState.show_gene_view,
            rx.flex(),
            rx.flex(
                rx.divider(width="90%"),
                rx.plotly(
                    data=ViewByGeneState.figure,
                    width="100%",
                    height=ViewByGeneState.get_figure_width,
                ),
                align="center",
                justify="center",
                class_name="mt-5 w-full",
                direction="column",
            ),
        ),
        direction="column",
        width="100%",
    )
