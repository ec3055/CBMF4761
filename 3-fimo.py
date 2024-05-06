import os
import shutil
import subprocess
import sys
from pathlib import Path
from pymemesuite.common import MotifFile, Sequence
from pymemesuite.fimo import FIMO
import Bio.SeqIO

# fimo = "/content/drive/MyDrive/deeptfni/fimo"
dir = "/content/drive/MyDrive/deeptfni/data_resource/human_HOCOMO/"
fimoout= "/content/drive/MyDrive/deeptfni/fimo-res/"
Path(fimoout).mkdir(parents=True, exist_ok=True)

cell = sys.argv[1]
print (cell)

input_dir = f"/content/drive/MyDrive/deeptfni/Fasta/{cell}"
outdir = f"/content/drive/MyDrive/deeptfni/fimo-res/{cell}_1e4"
Path(outdir).mkdir(parents=True, exist_ok=True)

# hocomo file list
file_list = [f for f in os.listdir(dir) if 'meme' in f]

for fi in file_list:
    m_path = os.path.join(dir, fi)
    
    # subprocess.run([fimo, "--oc", outdir, "--no-qvalue", m_path, f"{input_dir}.fasta"])
    
    with MotifFile(m_path) as motif_file:
        motif = motif_file.read()

    sequences = [
        Sequence(str(record.seq), name=record.id.encode())
        for record in Bio.SeqIO.parse(f"{input_dir}.fasta", "fasta")
    ]

    fimo = FIMO(both_strands=False)
    pattern = fimo.score_motif(motif, sequences, motif_file.background)

    # open fimo.tsv
    output_file = os.path.join(outdir, "fimo.tsv")

    # write header row
    with open(output_file, "w") as f:
        f.write("motif_id\tmotif_alt_id\tsequence_name\tstart\tstop\tstrand\tscore\tp-value\tq-value\tmatched_sequence\n")

        for m in pattern.matched_elements:
            # motif_id = m.source.accession.decode()
            motif_id = fi.split(".meme")[0]
            motif_alt_id = ""  # if available?
            sequence_name = m.source.name.decode()
            start = m.start
            stop = m.stop
            strand = m.strand
            score = m.score
            pvalue = m.pvalue
            qvalue = m.qvalue
            matched_sequence = m.sequence

            # format with tab-separated values
            line = f"{motif_id}\t{motif_alt_id}\t{sequence_name}\t{start}\t{stop}\t{strand}\t{score}\t{pvalue}\t{qvalue}\t{matched_sequence}\n"

            f.write(line)
    # for m in pattern.matched_elements:
    #     print(
    #         m.source.accession.decode(),
    #         m.start,
    #         m.stop,
    #         m.strand,
    #         m.score,
    #         m.pvalue,
    #         m.qvalue
    # )

    # rename output file
    m_parts = m_path.split("/")[-1].split('_HUMAN.H10MO.')
    print(m_parts)
    b = m_parts[1].split('.meme')[0]
    print(b)
    name = f"{m_parts[0]}.{b}"
    
    # move FIMO output to a named file
    shutil.move(f"{outdir}/fimo.tsv", f"{outdir}/{name}.txt")

# extract base name from the cell argument
c = cell.split('.')[0]

# execute next step
subprocess.run(["perl", "/content/drive/MyDrive/deeptfni/4-Get_TFBS_region.pl", c])
