import reflex as rx 
from RNAedit.models import Species, Gene, Transcript, Cds, Utr

def upload_data():
    with rx.session(url="sqlite:///reflex.db") as session:
        # 清空数据库
        with open("/Users/panxiaoguang/Desktop/RNAediting/RNAedit/assets/martquery_0401071929_391.txt", "r") as f:
            current_gene = None
            current_transcript = None
            human = Species(name="Homo_Sapiens")
            
            for line in f:
                if line.startswith("Chromosome"):
                    continue
                    
                Chromosome, transcript_start, transcript_end, transcript_id, strand, gene_name, cds_start, cds_end, utr5_start, utr5_end, utr3_start, utr3_end, gene_type, gene_start, gene_end = line.strip("\n").split("\t")
                if gene_name == "":
                    continue
               
                Chromosome = "chr" +  Chromosome 
                # 处理新基因的情况
                if current_gene is None or gene_name != current_gene.symbol:
                    # 如果当前基因存在，先保存到数据库
                    if current_gene is not None:
                        session.add(current_gene)
                        print(f"Gene {current_gene.symbol} has been added to the database")
                    
                    # 创建新基因对象
                    current_gene = Gene(
                        chromosome=Chromosome, 
                        start=int(gene_start), 
                        end=int(gene_end), 
                        strand=strand, 
                        symbol=gene_name, 
                        species=human
                    )
                    current_transcript = None
                
                # 处理新转录本的情况
                if current_transcript is None or transcript_id != current_transcript.transcript_id:
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
                        gene=current_gene
                    )
                
                # 添加CDS和UTR
                if cds_start != "":
                    cds = Cds(
                        chromosome=Chromosome, 
                        start=int(cds_start), 
                        end=int(cds_end), 
                        transcript=current_transcript
                    )
                    current_transcript.cdses.append(cds)
                
                if utr5_start != "":
                    utr5 = Utr(
                        chromosome=Chromosome, 
                        start=int(utr5_start), 
                        end=int(utr5_end), 
                        transcript=current_transcript
                    )
                    current_transcript.utres.append(utr5)
                
                if utr3_start != "":
                    utr3 = Utr(
                        chromosome=Chromosome, 
                        start=int(utr3_start), 
                        end=int(utr3_end), 
                        transcript=current_transcript
                    )
                    current_transcript.utres.append(utr3)
            
            # 循环结束后，添加最后一个转录本和基因
            if current_transcript is not None:
                current_gene.transcripts.append(current_transcript)
            if current_gene is not None:
                session.add(current_gene)
                print(f"Gene {current_gene.symbol} has been added to the database")
                
        session.commit()

upload_data()