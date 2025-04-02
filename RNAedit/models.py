import reflex as rx
import sqlmodel
from typing import List, Optional


class Species(rx.Model, table=True):
    name: str
    genes: List["Gene"] = sqlmodel.Relationship(back_populates="species")


class Gene(rx.Model, table=True):
    species_id: int = sqlmodel.Field(foreign_key="species.id")
    species: Optional["Species"] = sqlmodel.Relationship(back_populates="genes")
    transcripts: List["Transcript"] = sqlmodel.Relationship(back_populates="gene")
    #rnaediting: List["RNAediting"] = sqlmodel.Relationship(back_populates="gene")
    chromosome: str
    start: int
    end: int
    strand: str
    symbol: str
    
class Transcript(rx.Model, table=True):
    gene_id: int = sqlmodel.Field(foreign_key="gene.id")
    gene: Optional["Gene"] = sqlmodel.Relationship(back_populates="transcripts")
    cdses: List["Cds"] = sqlmodel.Relationship(back_populates="transcript")
    utres: List["Utr"] = sqlmodel.Relationship(back_populates="transcript")
    transcript_id: str
    chromosome: str
    start: int
    end: int
    transcript_type: str

class Cds(rx.Model, table=True):
    transcript_id: int = sqlmodel.Field(foreign_key="transcript.id")
    transcript: Optional["Transcript"] = sqlmodel.Relationship(back_populates="cdses")
    chromosome: str
    start: int
    end: int

class Utr(rx.Model, table=True):
    transcript_id: int = sqlmodel.Field(foreign_key="transcript.id")
    transcript: Optional["Transcript"] = sqlmodel.Relationship(back_populates="utres")
    chromosome: str
    start: int
    end: int
    
"""
class RNAediting(rx.Model, table=True):
    gene_id: int = sqlmodel.Field(foreign_key="gene.id")
    gene: Optional["Gene"] = sqlmodel.Relationship(back_populates="rnaediting")
    position: int
    ref: str
    alt: str
    strand: str
    samplenumbers: int
    annotation: List["Annotation"] = sqlmodel.Relationship(back_populates="rnaediting")
    pvalue: List["Pvalue"] = sqlmodel.Relationship(back_populates="rnaediting")


class Annotation(rx.Model, table=True):
    rnaediting_id: int = sqlmodel.Field(foreign_key="rnaediting.id")
    rnaediting: Optional["RNAediting"] = sqlmodel.Relationship(
        back_populates="annotation"
    )
    annotation: str


class Pvalue(rx.Model, table=True):
    rnaediting_id: int = sqlmodel.Field(foreign_key="rnaediting.id")
    rnaediting: Optional["RNAediting"] = sqlmodel.Relationship(back_populates="pvalue")
    pvalue: float
    loci: str
"""