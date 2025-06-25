import reflex as rx
from MAIRE.models import (
    RNAediting,
    Repeat,
    Gene,
    Aminochange,
    Tissue,
    RNAeditingtissuelink,
    Transcript,
    Species,
    Cds,
    Utr,
    Organ,
    EditingLevel,
)
from rxconfig import config
import sqlalchemy
import os


class DataLoader:
    def __init__(
        self,
        url,
        genefile,
        repeatfile,
        tissuefile,
        aachangefile,
        editingfile,
        editinglevelfile,
    ):
        self.url = url
        self.genefile = genefile
        self.repeatfile = repeatfile
        self.tissuefile = tissuefile
        self.aachangefile = aachangefile
        self.editingfile = editingfile
        self.editinglevelfile = editinglevelfile

    def _upload_gene(self):
        with rx.session(url=self.url) as session:
            # 清空数据库
            with open(self.genefile, "r") as f:
                current_gene = None
                current_transcript = None
                human = Species(name="Macaca_fascicularis")

                for line in f:
                    if line.startswith("Chromosome"):
                        continue

                    (
                        Chromosome,
                        transcript_start,
                        transcript_end,
                        transcript_id,
                        strand,
                        gene_id,
                        gene_name,
                        cds_start,
                        cds_end,
                        utr5_start,
                        utr5_end,
                        utr3_start,
                        utr3_end,
                        gene_type,
                        gene_start,
                        gene_end,
                    ) = line.strip("\n").split("\t")

                    Chromosome = "chr" + Chromosome
                    # 处理新基因的情况
                    if current_gene is None or gene_id != current_gene.ensembly_id:
                        # 如果当前基因存在，先保存到数据库
                        if current_gene is not None:
                            session.add(current_gene)
                        if gene_name == "NA":
                            # 创建新基因对象
                            current_gene = Gene(
                                chromosome=Chromosome,
                                start=int(gene_start),
                                end=int(gene_end),
                                strand=strand,
                                symbol=" ",
                                ensembly_id=gene_id,
                                species=human,
                            )
                        else:
                            current_gene = Gene(
                                chromosome=Chromosome,
                                start=int(gene_start),
                                end=int(gene_end),
                                strand=strand,
                                symbol=gene_name,
                                ensembly_id=gene_id,
                                species=human,
                            )
                        current_transcript = None

                    # 处理新转录本的情况
                    if (
                        current_transcript is None
                        or transcript_id != current_transcript.transcript_id
                    ):
                        # 如果已有转录本，先添加到基因中
                        if current_transcript is not None:
                            current_gene.transcripts.append(current_transcript)

                        # 创建新转录本对象
                        current_transcript = Transcript(
                            chromosome=Chromosome,
                            start=int(transcript_start),
                            end=int(transcript_end),
                            transcript_id=transcript_id,
                            transcript_type=gene_type,
                            gene=current_gene,
                        )

                    # 添加CDS和UTR
                    if cds_start != "NA":
                        cds = Cds(
                            chromosome=Chromosome,
                            start=int(cds_start),
                            end=int(cds_end),
                            transcript=current_transcript,
                        )
                        current_transcript.cdses.append(cds)

                    if utr5_start != "NA":
                        utr5 = Utr(
                            chromosome=Chromosome,
                            start=int(utr5_start),
                            end=int(utr5_end),
                            transcript=current_transcript,
                        )
                        current_transcript.utres.append(utr5)

                    if utr3_start != "NA":
                        utr3 = Utr(
                            chromosome=Chromosome,
                            start=int(utr3_start),
                            end=int(utr3_end),
                            transcript=current_transcript,
                        )
                        current_transcript.utres.append(utr3)

                # 循环结束后，添加最后一个转录本和基因
                if current_transcript is not None:
                    current_gene.transcripts.append(current_transcript)
                if current_gene is not None:
                    session.add(current_gene)

            session.commit()

    def _upload_repeat(self):
        with rx.session(url=self.url) as session:
            with open(self.repeatfile, "r") as f:
                ### 每100条数据提交一次数据库
                for line in f:
                    repClass = line.strip("\n")
                    repeat = Repeat(repeatclass=repClass)
                    session.add(repeat)
                session.commit()


    def _upload_tissue(self):
        with rx.session(url=self.url) as session:
            organ = Organ(name="brain")
            with open(self.tissuefile, "r") as f:
                for line in f:
                    tissue_name = line.strip("\n")
                    tissue = Tissue(name=tissue_name, organ=organ)
                    session.add(tissue)
                session.commit()


    def _upload_AA_change(self):
        with rx.session(url=self.url) as session:
            with open(self.aachangefile, "r") as f:
                for line in f:
                    trans, changes = line.strip("\n").split(":")
                    transcript = session.exec(
                        Transcript.select().where(Transcript.transcript_id == trans)
                    ).first()
                    if transcript:
                        aa_change = Aminochange(change=changes, transcript=transcript)
                        session.add(aa_change)
                    else:
                        continue
                session.commit()

    def _upload_edit(self):
        with rx.session(url=self.url) as session:
            with open(self.editingfile, "r") as f:
                for lineid, line in enumerate(f):
                    if line.startswith("Chromosome"):
                        continue
                    (
                        chromosome,
                        position,
                        ref,
                        ed,
                        location,
                        repeat,
                        gene,
                        geneName,
                        genicRegion,
                        exFun,
                        aminoAcidChanges,
                        n_Samples,
                        n_Tissues,
                        tissues,
                    ) = line.strip("\n").split("\t")
                    if "," in repeat or ";" in aminoAcidChanges:
                        continue
                    location = "REP" if location != "NONREP" else location
                    if repeat == "-":
                        repeat_db = None
                    else:
                        repeat_db = session.exec(
                            Repeat.select().where(Repeat.repeatclass == repeat)
                        ).first()
                    if gene == "-":
                        gene_db = None
                    else:
                        gene_id = gene.split(":")[0]
                        gene_db = session.exec(
                            Gene.select().where(Gene.ensembly_id == gene_id)
                        ).first()
                    if aminoAcidChanges == "-":
                        aminoAcidChange_dbs = []
                    else:
                        aminoAcidChange_dbs = []
                        for aminoAcidChange in aminoAcidChanges.split(";"):
                            if ":" in aminoAcidChange:
                                trans, acidchange = aminoAcidChange.split(":")
                                aminoAcidChange_db = session.exec(
                                    Aminochange.select().where(
                                        Aminochange.change == acidchange
                                    )
                                ).first()

                                if aminoAcidChange_db is not None:
                                    trans_db = session.exec(
                                        Transcript.select().where(
                                            Transcript.transcript_id == trans
                                        )
                                    ).first()
                                    aminoAcidChange_db.transcript = trans_db
                                    aminoAcidChange_dbs.append(aminoAcidChange_db)
                            else:
                                print("aminoAcidChange is", aminoAcidChange)
                    final_data = RNAediting(
                        chromosome=chromosome,
                        position=int(position),
                        ref=ref,
                        alt=ed,
                        location=location,
                        repeat=repeat_db,
                        gene=gene_db,
                        region=genicRegion,
                        exfun=exFun,
                        aminochanges=aminoAcidChange_dbs,
                        samplenumbers=int(n_Samples),
                        tissuenumbers=int(n_Tissues),
                    )
                    if tissues == "-":
                        tissues_dbs = []
                    else:
                        tissues_dbs = []
                        for tissue in tissues.split(";"):
                            if tissue != "":
                                tissue_db = session.exec(
                                    Tissue.select().where(Tissue.name == tissue)
                                ).first()
                                if tissue_db is not None:
                                    haha = RNAeditingtissuelink(
                                        rnaediting=final_data, tissue=tissue_db
                                    )
                                    tissues_dbs.append(haha)

                    final_data.tissues = tissues_dbs
                    session.add(final_data)
                    if lineid % 100 == 0:
                        session.commit()
                        session.refresh(final_data)
                session.commit()

    def _upload_levels(self):
        with rx.session(url=self.url) as session:
            with open(self.editinglevelfile, "r") as f:
                ## read the header
                for lineid, line in enumerate(f):
                    if line.startswith("Chromosome"):
                        continue
                    chrom, pos, tissue_name, level = line.strip("\n").split("\t")
                    level = float(level)
                    ## get rnaediting and tissues
                    rnaediting_db = session.exec(
                        RNAediting.select().where(
                            RNAediting.chromosome == chrom,
                            RNAediting.position == pos,
                        )
                    ).first()
                    tissues_dbs = session.exec(
                        Tissue.select().where(Tissue.name == tissue_name)
                    ).first()
                    if rnaediting_db is not None and tissues_dbs is not None:
                        final_db = EditingLevel(
                            rnaediting=rnaediting_db,
                            tissue=tissues_dbs,
                            level=level,
                        )
                        session.add(final_db)
                    if lineid % 20000 == 0:
                        session.commit()
                        session.refresh(final_db)
                        print(f"loaded {lineid} lines")
                session.commit()

    def load_data(self):
        print("loading data begin...")
        #print("load gene annotations")
        #self._upload_gene()
        #print("load repeat annotations")
        #self._upload_repeat()
        #print("load tissues")
        #self._upload_tissue()
        #print("load aminoacid changes")
        #self._upload_AA_change()
        #print("load RNA editing")
        #self._upload_edit()
        print("load editing levels")
        self._upload_levels()
        print("All data loaded!")
    def clear_all_tables(self):
        all_tables = [
            "alembic_version",
            "aminochange",
            "cds",
            "editinglevel",
            "gene",
            "organ",
            "repeat",
            "rnaediting",
            "rnaeditingtissuelink",
            "species",
            "tissue",
            "transcript",
            "utr"]

        with rx.session(url=self.url) as session:
            session.execute(sqlalchemy.text("SET FOREIGN_KEY_CHECKS = 0;"))
            for table in all_tables:
                session.execute(sqlalchemy.text("TRUNCATE TABLE :table"),{"table": table})
            session.execute(sqlalchemy.text("SET FOREIGN_KEY_CHECKS = 1;"))
            session.commit()
            

if __name__ == "__main__":
    data_path = "/home/panxiaoguang/Projects/maire_data"
    data_files = [
        "Gene_data_Macaque.txt",
        "repeats.tsv",
        "tissues.tsv",
        "AA_changes.tsv",
        "RNA_editing_data.txt",
        "RE_levels.tsv",
    ]
    data_files = [os.path.join(data_path, file) for file in data_files]
    dataloader = DataLoader(config.db_url, *data_files)
    dataloader.load_data()
