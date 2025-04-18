import reflex as rx
from ..template import template
from ..styles import info, tooltip
from ..models import Tissue, RNAeditingtissuelink
from sqlmodel import select
from sqlalchemy import func
from typing import List, Dict


def site_numbers_schema(result: tuple) -> List[Dict[str, int]]:
    fin_data = []
    for tissue, count in result:
        fin_data.append({"tissue": tissue, "count": count})
    return fin_data


class IndexState(rx.State):
    
    @rx.var
    async def get_numbers_in_tissues(self)->List[Dict[str, int]]:
        with rx.session() as session:
            statement = (
                select(Tissue.name, func.count(RNAeditingtissuelink.rnaediting_id))
                .join(RNAeditingtissuelink, RNAeditingtissuelink.tissue_id == Tissue.id)
                .group_by(Tissue.name)
            )
            result = session.exec(statement).all()
            return site_numbers_schema(result)


@rx.page(route="/", title="MAIRE")
@template
def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.text("Welcome To mammalian A-I RNA explorer (MAIRE) V1.0",class_name="text-4xl font-bold bg-gradient-to-r from-pink-500 via-red-500 to-yellow-500 bg-clip-text text-transparent"),
            rx.text(
                "The largest RNA editing resource for human and other organisms V1.0",
                size="4",
            ),
            rx.divider(),
            rx.markdown(
                """
            RNA editing is a relevant epitranscriptomic phenomenon by which primary RNAs are modified by base substitutions, insertions and/or deletions. In humans and other mammals, it mainly involves the deamination of adenosines to inosines by the ADAR family of enzymes acting on double RNA strands. A-to-I RNA editing has a plethora of biological effects and its deregulation has been linked to several human disorders. REDIportal V3.0 collects **15,680,833** sites from **9,642** [GTEx](https://gtexportal.org/home/) **RNAseq samples (across 31 tissues and 54 body sites)** and **9,683** [TCGA](https://portal.gdc.cancer.gov/) **RNAseq samples (across 31 studies and 24 disease types)**. Although human-oriented, REDIportal V3.0 collects also **107,095** sites from mouse nascent RNAseq samples, covering 3 different tissues <u>(Pubmed)</u>. Users can always search sites at the position level (by providing a genomic region or a gene name) and at the sample level (by providing a GTEx run accession or a TCGA aliquot id) to have an overview of RNA editing per RNAseq experiment. REDIportal V3.0 implements the Gene View module to look at individual events in their genic context and the dsRNA module to explore RNA editing at dsRNAs. REDIportal V3.0 hosts the CLAIRE resource **(Pubmed)**. Finally, REDIportal V3.0 includes interconnections with with [Ensembl](https://www.ensembl.org/), [UniProt](https://www.uniprot.org/), [RNAcentral](https://rnacentral.org/), and [PRIDE](https://www.ebi.ac.uk/pride/), which are widespread and internationally recognized [ELIXIR Core Data](https://elixir-europe.org/platforms/data/core-data-resources) resources, part of the European infrastructure for life sciences ([ELIXIR](https://elixir-europe.org/)).
            """
            ),
            rx.flex(
                rx.center(
                    rx.divider(width="100%", class_name="justify-self-center mb-5"),
                ),
                rx.center(
                    rx.hstack(
                        info(
                            "RNA editing sites load in All tissues",
                            "3",
                            "Statistic of all RNA editing sites in each tissues",
                            "start",
                        ),
                        align="center",
                        width="100%",
                        wrap="wrap",
                    ),
                ),
                rx.center(
                    rx.recharts.bar_chart(
                        rx.recharts.graphing_tooltip(**tooltip),
                        rx.recharts.cartesian_grid(
                            horizontal=True, vertical=False, class_name="opacity-25"
                        ),
                        rx.recharts.bar(
                            data_key="count",
                            fill=rx.color("accent"),
                            radius=[2, 2, 0, 0],
                        ),
                        rx.recharts.y_axis(type_="number", hide=False),
                        rx.recharts.x_axis(
                            data_key="tissue",
                            type_="category",
                            axis_line=False,
                            tick_line=True,
                            custom_attrs={"fontSize": "12px", "dx": -5},
                            text_anchor="end",
                            angle=-90,
                            height=200,
                            interval=0,
                        ),
                        data=IndexState.get_numbers_in_tissues,
                        width="100%",
                        height=380,
                    ),
                ),
                class_name="w-[100%] [&_.recharts-tooltip-item-separator]:w-full mt-10",
                direction="column",
            ),
        ),
        width="100%",
        class_name="mt-20",
    )
