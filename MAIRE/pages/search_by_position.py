import reflex as rx
from ..template import template
from ..models import RNAediting, Aminochange, Gene, EditingLevel
from typing import List, Dict
from ..styles import info, tooltip


##################################################################################################
################data structure for database parse:
def data_schema(record: RNAediting) -> dict:
    return {
        "id": record.id,
        "Chr": record.chromosome,
        "Position": record.position,
        "Ref": record.ref,
        "Ed": record.alt,
        #"Strand": record.gene.strand, ## conghui said we shouldn't show strand
        "Location": record.location,
        "Repeats": "-/-" if record.repeat is None else record.repeat.repeatclass,
        "Gene": "-/-" if record.gene.symbol == " " else record.gene.symbol,
        "Region": record.region,
        "Samples": record.samplenumbers,
        "Tissues": record.tissuenumbers,
        "ExFun": record.exfun,
    }


def amino_change_schema(record: Aminochange) -> dict:
    return {
        "id": record.id,
        "change": record.change,
        "transcript": record.transcript.transcript_id,
    }


def editing_level_schema(records: EditingLevel, samples: List[str]) -> List[dict]:
    final_data = []
    for sample in samples:
        newdata = 0
        for record in records:
            if record.tissue.name == sample:
                newdata = record.level
        final_data.append({"tissue": sample, "level": round(newdata, 3)})
    return final_data


def create_table_header(title: Dict[str, str]):
    return rx.tooltip(
        rx.table.column_header_cell(title["title"], justify="center"),
        content=title["tip"],
    )


def render_exfun_table_row(row_data: Dict[str, str]):
    return rx.table.row(
        rx.table.cell(
            rx.text(row_data["transcript"]),
            cursor="pointer",
            justify="center",
        ),
        rx.table.cell(
            rx.text(row_data["change"]),
            cursor="pointer",
            justify="center",
        ),
        _hover={"bg": rx.color(color="gray", shade=4)},
        align="center",
        white_space="nowrap",
    )


total_tissues = [
    "caudate nucleus",
    "inferior frontal gyrus",
    "middle frontal gyrus",
    "posterior parahippocampal gyrus",
    "straight gyrus",
    "occipital gyrus",
    "anterior cingulate gyrus",
    "cerebellum",
    "claustrum",
    "dentate gyrus",
    "globus pallidus",
    "inferior occipital gyrus",
    "inferior temporal gyrus",
    "insular cortex",
    "lateral occipitotemporal gyrus",
    "middle temporal gyrus",
    "pons",
    "postcentral gyrus",
    "posterior cingulate gyrus",
    "precentral gyrus",
    "septum",
    "superior frontal gyrus",
    "superior temporal gyrus",
    "supramarginal gyrus",
    "angular gyrus",
    "preoptic area",
    "thalamus",
    "annectant gyrus",
    "cuneus",
    "putamen",
    "superior parietal lobule",
    "amygdala",
    "anterior hypothalamus",
    "entorhinal cortex",
    "geniculate nucleus",
    "orbital gyrus",
    "posterior hippocampus",
    "posterior hypothalamus",
    "spinal cord dorsal",
    "subiculum",
    "substantia nigra",
    "superior colliculus",
    "spinal cord ventral",
    "anterior hippocampus",
    "medulla",
    "midbrain",
]
table_colums = [
    {"title": "Editing Level", "tip": "Click to show editing level plots in bottom"},
    {"title": "Chr", "tip": "Chromosome"},
    {"title": "Position", "tip": "Editing Position"},
    {"title": "Ref", "tip": "Nucleotide on reference"},
    {"title": "Ed", "tip": "Alt nucleotide"},
    #{"title": "Strand", "tip": "Gene Strand not editing strand"},
    {"title": "Location", "tip": "Whether the editing is in the repeat region or not"},
    {"title": "Repeats", "tip": "Repeat Class"},
    {"title": "Gene", "tip": "Gene Symbol"},
    {"title": "Region", "tip": "Whether the editing is in the coding region or not"},
    {"title": "NSamples", "tip": "How many samples have this editing"},
    {"title": "NTissues", "tip": "How many tissues have this editing"},
    {"title": "ExFun", "tip": "Extra annotation in Amino Acid Change"},
]
#################################################################################################


class SearchByPositionState(rx.State):
    orngism_name: str = "Monkey"
    genome_version: str
    region: str = ""
    gene_symbol: str
    main_data: List[Dict[str, str]] = []
    paginated_data: List[Dict[str, str]] = []
    column_names: List[Dict[str, str]] = []
    limits: List[str] = ["10", "15", "20", "30", "50"]
    current_limit: int = 10
    offset: int = 0
    current_page: int = 1
    number_of_rows: int = 0
    total_pages: int = 0
    exfun_data: List[Dict[str, str]] = []
    editing_level: List[Dict[str, int]] = []
    table_find: bool = False
    _all_tissues: List[str] = total_tissues

    @rx.var
    def show_table(self) -> bool:
        if self.main_data == []:
            return True
        else:
            return False

    @rx.var
    def show_plots(self) -> bool:
        if self.editing_level == []:
            return True
        else:
            return False

    @rx.event
    def paginate(self):
        start = self.offset
        end = start + self.current_limit
        self.paginated_data = self.main_data[start:end]
        self.current_page = (self.offset // self.current_limit) + 1

    @rx.event
    def delta_limit(self, limit: str):
        self.current_limit = int(limit)
        self.offset = 0
        self.total_pages = (
            self.number_of_rows + self.current_limit - 1
        ) // self.current_limit
        self.paginate()

    @rx.event
    def previous(self):
        if self.offset >= self.current_limit:
            self.offset -= self.current_limit
        else:
            self.offset = 0

        self.paginate()

    @rx.event
    def next(self):
        if self.offset + self.current_limit < self.number_of_rows:
            self.offset += self.current_limit

        self.paginate()

    @rx.event
    def clear_data(self):
        self.main_data = []
        self.paginated_data = []
        self.column_names = []
        self.editing_level = []

    @rx.event
    async def get_data_from_database(self):
        self.table_find = True
        yield
        with rx.session() as session:
            if self.region != "":
                ## use region to get records
                chrom, pos = self.region.split(":")
                start, end = pos.split("-")
                start = int(start)
                end = int(end)
                records = session.exec(
                    RNAediting.select().where(
                        RNAediting.chromosome == chrom,
                        RNAediting.position >= start,
                        RNAediting.position <= end,
                    )
                ).all()
                if records is not None:
                    self.main_data = [data_schema(record) for record in records]
                    self.paginated_data = self.main_data[:10]
                    self.column_names = table_colums
                    self.number_of_rows = len(self.main_data)
                    self.total_pages = (
                        self.number_of_rows + self.current_limit - 1
                    ) // self.current_limit
                    self.table_find = False
                    yield
                else:
                    self.table_find = False
                    yield rx.toast("No region found!")
            else:
                ## use gene symbol to get records
                records = session.exec(
                    Gene.select().where(Gene.symbol == self.gene_symbol)
                ).first()
                if records is not None:
                    self.main_data = [
                        data_schema(record) for record in records.rnaediting
                    ]
                    self.paginated_data = self.main_data[:10]
                    self.column_names = table_colums
                    self.number_of_rows = len(self.main_data)
                    self.total_pages = (
                        self.number_of_rows + self.current_limit - 1
                    ) // self.current_limit
                    self.table_find = False
                    yield
                else:
                    self.table_find = False
                    yield rx.toast("No gene found!")

    @rx.event
    async def get_exfun_data(self, value: bool, rnaedit_id: int):
        with rx.session() as session:
            records = session.get(RNAediting, rnaedit_id)
            self.exfun_data = [
                amino_change_schema(record) for record in records.aminochanges
            ]

    @rx.event
    async def render_editing_level_plot(self, rnaedit_id: int):
        with rx.session() as session:
            records = session.get(RNAediting, rnaedit_id)
            self.editing_level = editing_level_schema(
                records.editinglevel, self._all_tissues
            )

    @rx.event
    def show_example(self):
        self.genome_version = "macFas5"
        self.region = "chr1:117451-18582865"
        return SearchByPositionState.get_data_from_database()


#### util functions for Table UI
#################################################################################
def render_exfun_dialog(row_data: Dict[str, str]):
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                row_data["ExFun"],
                variant="solid",
                cursor="pointer",
                color_scheme=rx.cond(
                    row_data["ExFun"] == "Nonsynonymous", "orange", "sky"
                ),
            )
        ),
        rx.dialog.content(
            rx.dialog.title("Extra function annotation:"),
            rx.inset(
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Ensembl ID", justify="center"),
                            rx.table.column_header_cell(
                                "Amino change", justify="center"
                            ),
                        ),
                    ),
                    rx.table.body(
                        rx.foreach(
                            SearchByPositionState.exfun_data, render_exfun_table_row
                        )
                    ),
                ),
                side="x",
                margin_top="24px",
                margin_bottom="24px",
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        "Close",
                        variant="soft",
                        color_scheme="gray",
                    ),
                ),
                spacing="3",
                justify="end",
            ),
        ),
        on_open_change=lambda c: SearchByPositionState.get_exfun_data(
            c, row_data["id"]
        ),
    )


def render_row(data: Dict[str, str]):
    return rx.table.row(
        rx.table.cell(
            rx.button(
                rx.icon(
                    "arrow-big-right-dash",
                    class_name="hover:rotate-90 transition-transform duration-200 ease-in-out",
                ),
                variant="solid",
                cursor="pointer",
                color_scheme="indigo",
                on_click=SearchByPositionState.render_editing_level_plot(data["id"]),
            ),
            justify="center",
        ),
        rx.table.cell(
            rx.text(data["Chr"]),
            cursor="pointer",
            justify="center",
        ),
        rx.table.cell(
            rx.text(data["Position"]),
            cursor="pointer",
            justify="center",
        ),
        rx.table.cell(
            rx.text(data["Ref"]),
            cursor="pointer",
            justify="center",
        ),
        rx.table.cell(
            rx.text(data["Ed"]),
            cursor="pointer",
            justify="center",
        ),
        #rx.table.cell(
        #    rx.text(data["Strand"]),
        #    cursor="pointer",
        #    justify="center",
        #),
        rx.table.cell(
            rx.text(data["Location"]),
            cursor="pointer",
            justify="center",
        ),
        rx.table.cell(
            rx.text(data["Repeats"]),
            cursor="pointer",
            justify="center",
        ),
        rx.table.cell(
            rx.cond(
                data["Gene"] == "-/-",
                rx.text(data["Gene"]),
                rx.button(
                    data["Gene"],
                    variant="solid",
                    cursor="pointer",
                    color_scheme="grass",
                    on_click=rx.redirect(
                        f"https://www.genecards.org/cgi-bin/carddisp.pl?gene={data['Gene']}",
                        is_external=True,
                    ),
                ),
            ),
            cursor="pointer",
            justify="center",
        ),
        rx.table.cell(
            rx.text(data["Region"]),
            cursor="pointer",
            justify="center",
        ),
        rx.table.cell(
            rx.text(data["Samples"]),
            cursor="pointer",
            justify="center",
        ),
        rx.table.cell(
            rx.text(data["Tissues"]),
            cursor="pointer",
            justify="center",
        ),
        rx.table.cell(
            rx.cond(
                data["ExFun"] == "-",
                rx.text(data["ExFun"]),
                render_exfun_dialog(data),
            ),
            cursor="pointer",
            justify="center",
        ),
        _hover={"bg": rx.color(color="gray", shade=4)},
        align="center",
        white_space="nowrap",
    )


def create_pagination():
    return rx.hstack(
        rx.hstack(
            rx.text("Rows per page", weight="bold", font_size="12px"),
            rx.select(
                SearchByPositionState.limits,
                default_value="10",
                on_change=SearchByPositionState.delta_limit,
                width="80px",
            ),
            align_items="center",
        ),
        rx.hstack(
            rx.text(
                f"Page {SearchByPositionState.current_page} of {SearchByPositionState.total_pages}",
                width="100px",
                weight="bold",
                font_size="12px",
            ),
            rx.button(
                rx.icon(
                    tag="chevron-left",
                    on_click=SearchByPositionState.previous,
                    size=25,
                    cursor="pointer",
                ),
                color_scheme="gray",
                variant="surface",
                size="1",
                width="32px",
                height="32px",
            ),
            rx.button(
                rx.icon(
                    tag="chevron-right",
                    on_click=SearchByPositionState.next,
                    size=25,
                    cursor="pointer",
                ),
                color_scheme="gray",
                variant="surface",
                size="1",
                width="32px",
                height="32px",
            ),
            align_items="center",
            spacing="1",
        ),
        align_items="center",
        spacing="4",
        flex_wrap="wrap",
    )


#################################################################################
#################################################################################
#################################################################################


#### main UI for this page:
@rx.page("/search_by_position",title="Search By Position")
@template
def search_by_position():
    return rx.flex(
        rx.container(
            rx.vstack(
                rx.heading("Search RNA Editing Sites By:"),
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
                            value=SearchByPositionState.orngism_name,
                            on_change=SearchByPositionState.set_orngism_name,
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
                                    SearchByPositionState.orngism_name,
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
                            value=SearchByPositionState.genome_version,
                            on_change=SearchByPositionState.set_genome_version,
                            width="20%",
                        ),
                        spacing="5",
                        align="center",
                    ),
                    rx.flex(
                        rx.text("Genomic Region:"),
                        rx.input(
                            placeholder="Coordinates like chr1:117467-117689671",
                            value=SearchByPositionState.region,
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
                            disabled=rx.cond(
                                SearchByPositionState.region != "", True, False
                            ),
                            on_blur=SearchByPositionState.set_gene_symbol,
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
                            on_click=SearchByPositionState.get_data_from_database,
                            loading=SearchByPositionState.table_find,
                        ),
                        rx.button(
                            "Reset",
                            color_scheme="orange",
                            cursor="pointer",
                            on_click=SearchByPositionState.clear_data,
                        ),
                        rx.button(
                            "Example",
                            color_scheme="violet",
                            cursor="pointer",
                            on_click=SearchByPositionState.show_example,
                        ),
                    ),
                    direction="column",
                    width="100%",
                    spacing="3",
                ),
                width="100%",
                class_name="mt-20",
            ),
            width="100%",
        ),
        rx.cond(
            SearchByPositionState.show_table,
            rx.flex(),
            rx.flex(
                rx.divider(width="90%"),
                create_pagination(),
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.foreach(
                                SearchByPositionState.column_names,
                                create_table_header,
                            )
                        ),
                    ),
                    rx.table.body(
                        rx.foreach(SearchByPositionState.paginated_data, render_row)
                    ),
                    width="90%",
                    variant="surface",
                    size="1",
                ),
                direction="column",
                width="100%",
                align="center",
                spacing="3",
                margin_top="25px",
            ),
        ),
        rx.cond(
            SearchByPositionState.show_plots,
            rx.flex(),
            rx.flex(
                rx.center(
                    rx.divider(width="90%", class_name="justify-self-center mb-5"),
                ),
                rx.center(
                    rx.hstack(
                        info(
                            "RNA editing level - All tissues",
                            "3",
                            "Showing all RNA editing level in all tissues",
                            "start",
                        ),
                        align="center",
                        width="90%",
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
                            data_key="level",
                            fill=rx.color("accent"),
                            radius=[2, 2, 0, 0],
                        ),
                        rx.recharts.y_axis(type_="number", hide=True),
                        rx.recharts.x_axis(
                            data_key="tissue",
                            type_="category",
                            axis_line=False,
                            tick_line=True,
                            custom_attrs={"fontSize": "12px", "dx": -5},
                            text_anchor="end",
                            angle=-90,
                            height=200,
                        ),
                        data=SearchByPositionState.editing_level,
                        width="90%",
                        height=380,
                    ),
                ),
                class_name="w-[100%] [&_.recharts-tooltip-item-separator]:w-full mt-10",
                direction="column",
            ),
        ),
        direction="column",
        width="100%",
    )
