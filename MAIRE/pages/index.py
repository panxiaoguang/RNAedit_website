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
            rx.text("Welcome To mammalian A-I RNA explorer (MAIRE) V1.0",class_name="text-3xl font-bold bg-gradient-to-r from-pink-500 via-red-500 to-yellow-500 bg-clip-text text-transparent"),
            rx.text(
                "The largest RNA editing resource for human and other organisms V1.0",
                size="4",
            ),
            rx.divider(),
            rx.markdown(
                """
            **Adenosine-to-inosine (A-I) RNA editing** is one of the most prevalent post-transcriptional RNA modifications, playing critical roles in transcriptome diversity and cellular regulation. *Despite its abundance, the evolutionary and functional significance of A-I editing in primate brains remains poorly understood*. To address this gap, we conducted whole-genome and whole-transcriptome sequencing of **39** anatomically defined brain regions of adult **Macaca fascicularis** and identify **2,782,079** A-I editing sites, including **2,009** recoding sites enriched in genes related to neurotransmission functions. Most of macaque brain A-I editing sites are detected in the **cerebral cortex**, **cerebellum**, and **amygdala**. This resource provides a foundation for investigating the contribution of RNA editing to brain complexity and neurological disorders. Users can query editing sites by genomic coordinates or gene names. Datasets from additional mammals (e.g., humans, pigs, and mice) will be integrated in future updates.
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
                        rx.recharts.y_axis(type_="number", hide=False,width=25,),
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
