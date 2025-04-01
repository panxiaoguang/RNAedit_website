import reflex as rx
from ..template import template


class IndexState(rx.State):
    pass


@rx.page(route="/", title="RNAedit")
@template
def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("Welcome To RNAediting V1.0"),
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
        ),
        width="100%",
        class_name="mt-20"
    )
