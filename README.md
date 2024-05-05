# CBMF4761 Computational Genomics Final Project

This project expands on the original methods of DeepTFni, as described in the following paper (available [here](https://www.nature.com/articles/s42256-022-00469-5)):
```
Li, H., Sun, Y., Hong, H. et al.
Inferring transcription factor regulatory networks
from single-cell ATAC-seq data based on graph neural networks.
Nat Mach Intell 4, 389–400 (2022).
```
We modify DeepTFni's original scATAC-only model to include scRNA-seq and TF-target gene relationships, allowing us to infer both TF-TF and TF-target gene relationships using a C9orf72-mediated ALS dataset. 

All sequencing data used in this study was obtained from the Gene Expression Omnibus repository under the accession code [GSE219281](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE219281).

## Description
- *data folder*: contains zipped files for sample processed scATAC-seq/scRNA-seq data, sequencing metadata, TF-target gene binary matrix, and files from the HOCOMOCO and hTFtarget databases
- *define_tf_target_matrix.ipynb*: generates the TF-target binary matrix
- *preprocess_atac_and_rna_data.ipynb*: processes the raw scATAC-seq/scRNA-seq data from GEO GSE219281 into count matrices for each patient and then combines and subsets them according to cohort and cell type
- *generating_network_graphs.ipynb*: creates graph networks figures to visualize the differences between the TRN skeleton and model's predicted output
