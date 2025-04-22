import reflex as rx
from ..template import template


@rx.page(route="/help",title="how to use this website")
@template
def faq_v1():
    return rx.container(
        rx.flex(
            rx.heading(
                "Website Introduction:",
                size="6",
                align="left",
                color_scheme="indigo",
            ),
            rx.image(
                src="https://tncache1-f1.v3mh.com/image/2025/04/22/763f67315ec7f4058acff588e9158caa.png"
            ),
            rx.text(
                "This website is a database site. On the homepage, you can view the website introduction and a simple statistics page, allowing users to intuitively see the types and quantities of data currently stored in the database."
            ),
            rx.text("The website currently mainly includes three functions:"),
            rx.list.ordered(
                rx.list.item("Search by gene name or genomic coordinates"),
                rx.list.item(
                    "Preview editing levels in the transcript illustration by gene name"
                ),
                rx.list.item(
                    "Fully browse all editing sites and their corresponding annotations (repetitive sequences, transcripts, etc.) in the whole genome browser"
                ),
            ),
            rx.heading("Instructions for Using Website Functions:",
            size="6",
            align="left",
            color_scheme="indigo"),
            rx.heading("Coordinate or Gene Name Search",
            size="5",
            align="left",
            color_scheme="blue"),
            rx.image(src="https://tncache1-f1.v3mh.com/image/2025/04/22/09d5bceb9895f3ea485f1267cd91176b.png"),
            rx.text("As shown in the figure, after selecting the species and the corresponding genome version, you can choose either coordinates or gene name as input. By clicking the search button, you can view the corresponding editing sites, which are presented in a table format."),
            rx.text("Note that clicking the gene button will directly navigate to the Gene Card page."),
            rx.image(src="https://tncache1-f1.v3mh.com/image/2025/04/22/f7fed3d94e8931792079267c8128c0cc.png"),
            rx.text("As shown above, users can click the ExFun button to see additional annotations in the pop-up dialog, mainly regarding amino acid changes in the corresponding transcript."),
            rx.image(src="https://tncache1-f1.v3mh.com/image/2025/04/22/b60d620c62538053e1f0e51db3f9f1f2.png"),
            rx.text("Users can also click the Editing level button to view editing levels of each editing site in different tissues."),
            rx.heading("Gene Landscape",
            size="5",
            align="left",
            color_scheme="blue"),
            rx.image(src="https://tncache1-f1.v3mh.com/image/2025/04/22/53742b2ec4e8d60374c93acba15a1f80.png"),
            rx.text("As shown above, after selecting species and genome version, enter a gene name to simultaneously view transcripts and editing levels of all editing sites in that gene, which provides a more intuitive overview."),
            rx.heading("Browser",
            size="5",
            align="left",
            color_scheme="blue"),
            rx.image(src="https://tncache1-f1.v3mh.com/image/2025/04/22/de6ad349b091343291011df92a119d0a.png"),
            rx.text("Users can directly click the Jbrowse button in the navigation bar to enter the global browsing page. On this page, users will see all editing sites, as well as corresponding repetitive elements and transcripts, in Jbrowse2. Users can zoom in or out, and also jump to specific locations by entering genome coordinate positions at the top."),
            direction="column",
            spacing="2"
        ),
        width="100%",
        class_name="mt-20",
        
    )
