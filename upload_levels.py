import reflex as rx
from rxconfig import config
from MAIRE.models import (
    RNAediting,
    Tissue,
    EditingLevel,
)
import sys

def upload_RNAediting_levels(editinglevelfile):
    with rx.session(url=config.db_url) as session:
        with open(editinglevelfile, "r") as f:
            for lineid, line in enumerate(f):
                if line.startswith("Chromosome"):
                    continue
                chrom, pos, tissue_name, level = line.strip("\n").split("\t")
                level = float(level)
                ## get rnaediting and tissues
                try:
                    rnaediting_db = session.exec(
                        RNAediting.select().where(
                            RNAediting.chromosome == chrom,
                            RNAediting.position == pos,
                        )
                    ).first()
                except Exception as e:
                    print(f"Error: {e}")
                    print(f"LineID: {lineid}; this is {lineid//20000} round, the last databaseid should be {20000*(lineid//20000)}")
                    sys.exit(1)
                try:
                    tissues_dbs = session.exec(
                        Tissue.select().where(Tissue.name == tissue_name)
                    ).first()
                except Exception as e:
                    print(f"Error: {e}")
                    print(f"LineID: {lineid} ; this is {lineid//20000} round, the last databaseid should be {20000*(lineid//20000)}")
                    sys.exit(1)
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
                    print(f"loaded {lineid} lines, current database id: {20000*(lineid//20000)}")
            session.commit()
            session.refresh(final_db)
            print("congradulations! all data loaded!")
    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--editinglevelfile", type=str, required=True)
    args = parser.parse_args()
    upload_RNAediting_levels(args.editinglevelfile)