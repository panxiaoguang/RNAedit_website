import reflex as rx
from ..template import template
from typing import List


class ViewByGeneState(rx.State):
    orngism_name: str = "Homo sapiens"
    genome_version: str
    gene_symbol: str

    @rx.var
    def get_genome_versions(self) -> List[str]:
        if self.orngism_name == "Homo sapiens":
            return ["hg38", "hg19"]
        elif self.orngism_name == "Macaca_fascicularis":
            return ["Mmul_10"]
        else:
            return ["Unknown"]


@rx.page("/view_by_gene")
@template
def view_by_genes() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("View RNA Editing for a given gene:"),
            rx.divider(),
            rx.flex(
                rx.flex(
                    rx.text("Organism Name:"),
                    rx.select(
                        ["Homo sapiens", "Macaca_fascicularis"],
                        value=ViewByGeneState.orngism_name,
                        on_change=ViewByGeneState.set_orngism_name,
                        width="20%",
                    ),
                    spacing="5",
                    align="center",
                ),
                rx.flex(
                    rx.text("Genome Version:"),
                    rx.select(
                        ViewByGeneState.get_genome_versions,
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
                        on_blur=ViewByGeneState.set_gene_symbol,
                        width="50%",
                    ),
                    spacing="5",
                    align="center",
                ),
                rx.hstack(
                    rx.button(
                        "Search",
                        on_click=rx.redirect("/render_by_gene"),
                    ),
                ),
                direction="column",
                width="100%",
                spacing="3",
            ),
        ),
        width="100%",
        class_name="mt-20"
    )
