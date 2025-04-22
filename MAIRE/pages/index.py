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
    async def get_numbers_in_tissues(self) -> List[Dict[str, int]]:
        with rx.session() as session:
            statement = (
                select(Tissue.name, func.count(RNAeditingtissuelink.rnaediting_id))
                .join(RNAeditingtissuelink, RNAeditingtissuelink.tissue_id == Tissue.id)
                .group_by(Tissue.name)
            )
            result = session.exec(statement).all()
            return site_numbers_schema(result)


data = [
    {
        "image": "auditors",
        "title": "Search by Position",
        "description": "Retrieve the required data from the database based on the site and present it in a table",
    },
    {
        "image": "View by Gene",
        "title": "View by Gene",
        "description": "Visualization of gene-corresponding transcripts to anchor editing levels to transcript scale",
    },
    {
        "image": "accountants",
        "title": "Browse by Jbrowse2",
        "description": "Users can jump to any site through navigation and retrieve the edited site and the corresponding annotation information at the same time.",
    },
    {
        "image": "others",
        "title": "Others",
        "description": "Waiting for adding...",
    },
]


def create_featured(title: str, description: str) -> rx.Component:
    return rx.hstack(
        rx.box(
            width="42px",
            height="42px",
            bg=rx.color("gray", 4),
            border_radius="10px",
        ),
        rx.vstack(
            rx.text(title, size="2", weight="bold"),
            rx.text(description, size="1", weight="medium", color_scheme="gray"),
            spacing="1",
            width=["90%" if i <= 1 else "60%" for i in range(6)],
        ),
        width="100%",
        padding="12px 0px",
    )


def create_featured_section(features: List[Dict[str, str]]) -> rx.Component:
    return rx.vstack(
        rx.heading(
            "The database is not only a database",
            size="4",
            color=rx.color("slate", 12),
        ),
        rx.text(
            "In addition to simple searches, this website also provides interactive visualizations from multiple perspectives to fully help users study the prevalence and specificity of RNA editing sites.",
            color=rx.color("slate", 11),
        ),
        rx.hstack(
            *[create_featured(item["title"], item["description"]) for item in features],
            width="100%",
            display="grid",
            grid_template_columns=[
                "repeat(1, 1fr)" if i <= 1 else "repeat(2, 1fr)" for i in range(6)
            ],
            justify_content="start",
            align_items="start",
            padding="24px 0px",
            spacing="0",
            wrap="wrap",
        ),
        width="100%",
        display="flex",
        justify="center",
        align="start",
        margin_top="24px",
    )


@rx.page(route="/", title="MAIRE")
@template
def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.text(
                "Welcome To mammalian A-I RNA explorer (MAIRE) V1.0",
                class_name="text-3xl font-bold bg-gradient-to-r from-pink-500 via-red-500 to-yellow-500 bg-clip-text text-transparent",
            ),
            rx.text(
                "The largest RNA editing resource for Macaca fascicularis and other organisms V1.0",
                size="4",
            ),
            rx.divider(),
            rx.markdown(
                """
            **Adenosine-to-inosine (A-I) RNA editing** is one of the most prevalent post-transcriptional RNA modifications, playing critical roles in transcriptome diversity and cellular regulation. *Despite its abundance, the evolutionary and functional significance of A-I editing in primate brains remains poorly understood*. To address this gap, we conducted whole-genome and whole-transcriptome sequencing of **39** anatomically defined brain regions of adult **Macaca fascicularis** and identify **2,782,079** A-I editing sites, including **2,009** recoding sites enriched in genes related to neurotransmission functions. Most of macaque brain A-I editing sites are detected in the **cerebral cortex**, **cerebellum**, and **amygdala**. This resource provides a foundation for investigating the contribution of RNA editing to brain complexity and neurological disorders. Users can query editing sites by genomic coordinates or gene names. Datasets from additional mammals (e.g., humans, pigs, and mice) will be integrated in future updates.
            """
            ),
            rx.text(
                "Don't know how to use it? Please check the help page.",
                 rx.link("help",href="/help", label="Help"),
                size="2",
                color="red",
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
                        rx.recharts.y_axis(
                            type_="number",
                            hide=False,
                            width=25,
                        ),
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
            rx.divider(),
            create_featured_section(data),
        ),
        width="100%",
        class_name="mt-20",
    )
