import reflex as rx
from ..template import template
from typing import List


class SearchByPositionState(rx.State):
    orngism_name: str = "Homo sapiens"
    genome_version: str
    region: str
    gene_symbol: str
    body_site: str

    @rx.event
    def get_data_from_database(self):
        print("hello world!")

    @rx.var
    def get_genome_versions(self) -> List[str]:
        if self.orngism_name == "Homo sapiens":
            return ["hg38", "hg19"]
        elif self.orngism_name == "Macaca_fascicularis":
            return ["Mmul_10"]
        else:
            return ["Unknown"]

    @rx.var
    def get_body_sites(self) -> List[str]:
        if self.orngism_name == "Homo sapiens":
            return ["Bone Marrow", "Whole Brain", "Cells-Primary Neurons"]
        elif self.orngism_name == "Macaca_fascicularis":
            return ["Mmul_10"]
        else:
            return ["Unknown"]


@rx.page("/search_by_position")
@template
def search_by_position():
    return rx.container(
        rx.vstack(
            rx.heading("Search RNA Editing Sites By:"),
            rx.divider(),
            rx.flex(
                rx.flex(
                    rx.text("Organism Name:"),
                    rx.select(
                        ["Homo sapiens", "Macaca_fascicularis"],
                        value=SearchByPositionState.orngism_name,
                        on_change=SearchByPositionState.set_orngism_name,
                        width="20%",
                    ),
                    spacing="5",
                    align="center",
                ),
                rx.flex(
                    rx.text("Genome Version:"),
                    rx.select(
                        SearchByPositionState.get_genome_versions,
                        on_change=SearchByPositionState.set_genome_version,
                        width="20%",
                    ),
                    spacing="5",
                    align="center",
                ),
                rx.flex(
                    rx.text("Genomic Region:"),
                    rx.input(
                        placeholder="Coordinates like chr4:158149690-158282538",
                        on_blur=SearchByPositionState.set_region,
                        width="50%",
                    ),
                    spacing="5",
                    align="center",
                ),
                rx.flex(
                    rx.text("Genomic Name:"),
                    rx.input(
                        placeholder="Gene Symbol like GRIA2,TP53,SOD1 ...",
                        on_blur=SearchByPositionState.set_gene_symbol,
                        width="50%",
                    ),
                    spacing="5",
                    align="center",
                ),
                rx.flex(
                    rx.text("Body Sites:"),
                    rx.select(
                        SearchByPositionState.get_body_sites,
                        on_change=SearchByPositionState.set_body_site,
                        width="20%",
                    ),
                    spacing="5",
                    align="center",
                ),
                rx.hstack(
                    rx.button(
                        "Search",
                        on_click=SearchByPositionState.get_data_from_database,
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
