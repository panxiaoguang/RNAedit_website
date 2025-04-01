import reflex as rx
from ..template import template
from ..components import j_browse_linear_genome_view
### test AG-Grid component to render button in cells


assembly = {
    "name": "hg38",
    "sequence": {
        "type": "ReferenceSequenceTrack",
        "trackId": "GRCh38-ReferenceSequenceTrack",
        "adapter": {
            "type": "BgzipFastaAdapter",
            "uri": "https://jbrowse.org/genomes/GRCh38/fasta/hg38.prefix.fa.gz",
        },
    },
    "refNameAliases": {
        "adapter": {
            "type": "RefNameAliasAdapter",
            "uri": "https://s3.amazonaws.com/jbrowse.org/genomes/GRCh38/hg38_aliases.txt",
        }
    },
}

tracks = [
    {
        "type": "FeatureTrack",
        "trackId": "genes",
        "name": "NCBI RefSeq Genes",
        "assemblyNames": ["hg38"],
        "category": ["Genes"],
        "adapter": {
            "type": "Gff3TabixAdapter",
            "gffGzLocation": {
                "uri": "https://s3.amazonaws.com/jbrowse.org/genomes/GRCh38/ncbi_refseq/GCA_000001405.15_GRCh38_full_analysis_set.refseq_annotation.sorted.gff.gz"
            },
            "index": {
                "location": {
                    "uri": "https://s3.amazonaws.com/jbrowse.org/genomes/GRCh38/ncbi_refseq/GCA_000001405.15_GRCh38_full_analysis_set.refseq_annotation.sorted.gff.gz.tbi"
                }
            },
        },
        "textSearching": {
            "textSearchAdapter": {
                "type": "TrixTextSearchAdapter",
                "textSearchAdapterId": "gff3tabix_genes-index",
                "uri": "https://s3.amazonaws.com/jbrowse.org/genomes/GRCh38/ncbi_refseq/GCA_000001405.15_GRCh38_full_analysis_set.refseq_annotation.sorted.gff.gz.ix",
                "assemblyNames": ["GRCh38"],
            }
        },
    },
    {
        "type": "FeatureTrack",
        "trackId": "rmsk_hg38",
        "name": "UCSC RepeatMasker",
        "category": ["Repeats"],
        "assemblyNames": ["hg38"],
        "adapter": {"type": "UCSCAdapter", "track": "rmsk"},
        "displays": [
            {
                "type": "LinearBasicDisplay",
                "displayId": "rmsk_display",
                "renderer": {
                    "type": "SvgFeatureRenderer",
                    "labels": {"name": "jexl:get(feature,'repName')"},
                },
            }
        ],
    },
]

session = {
    "name": "this session",
    "margin": 0,
    "view": {
        "id": "linearGenomeView",
        "type": "LinearGenomeView",
        "init": {
            "assembly": "hg38",
            "loc": "11:89,177,875..89,295,759",
            "tracks": [
                "GRCh38-ReferenceSequenceTrack",
                "genes",
                "rmsk_hg38",
            ],
        },
    },
}


class BrowseState(rx.State):
    assembly: dict = assembly
    tracks: list = tracks
    location: str = "11:89,177,875..89,295,759"
    default_session: dict = session


@rx.page(route="/jbrowse_view")
@template
def jbrowse_view() -> rx.Component:
    return rx.flex(
        rx.heading("Test JBrowse"),
        j_browse_linear_genome_view(
            assembly=BrowseState.assembly,
            tracks=BrowseState.tracks,
            location=BrowseState.location,
            default_session=BrowseState.default_session,
        ),
        direction="column",
        width="100%",
        justify="center",
        class_name="p-5 mt-20",
    )
