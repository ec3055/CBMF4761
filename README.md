# CBMF4761 Computational Genomics Final Project
This project expands on the original methods of DeepTFni, as described in the following paper (available [here](https://www.nature.com/articles/s42256-022-00469-5)):

```
Li, H., Sun, Y., Hong, H. et al.
Inferring transcription factor regulatory networks
from single-cell ATAC-seq data based on graph neural networks.
Nat Mach Intell 4, 389–400 (2022).
```

We modified DeepTFni's original scATAC-only model to include scRNA-seq and TF-target gene relationships, allowing us to infer both TF-TF and TF-target gene relationships using a C9orf72-mediated ALS dataset.

All sequencing data used in this study was obtained from the Gene Expression Omnibus repository under the accession code [GSE219281](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE219281). The reference genome hg19 should also be downloaded from [here](https://hgdownload.soe.ucsc.edu/downloads.html).

## Dependencies
DeepTFni is a codebase consisting of a mix of languages: Python, R, Perl, and Bash. Various modifications have been made to accommodate our data and ensure correct execution. We primarily executed this code on Google Colab. The following libraries need to be installed:
- pytorch 1.7.1
- numpy 1.8.11
- pandas 2.1.3
- matplotlib 3.8.2
- BioPerl 1.5.7
- R 4.0.3
- fimo
- scipy 1.11.4
- tqdm 4.66.2
- networkx 3.2.1
- MAESTRO 1.5.0
- matplotlib 3.8.2
- seaborn 0.13.2
- scikit-learn 1.4.0

## Description of code
data folder: contains zipped files for sample processed scATAC-seq/scRNA-seq data, sequencing metadata, TF-target gene binary matrix, and files from the HOCOMOCO and hTFtarget databases

results folder: contains sample TRN skeletons and corresponding outputted model predictions

define_tf_target_matrix.ipynb: generates the TF-target binary matrix

preprocess_atac_and_rna_data.ipynb: processes the raw scATAC-seq/scRNA-seq data from GEO GSE219281 into count matrices for each patient and then combines and subsets them according to cohort and cell type

DeepTFni.ipynb: Main notebook that contains necessary package installations and starts execution of the DeepTFni pipeline. It directly runs:

run_DeepTFni_csv.pl: Executes run_template_csv.sh, takes in experiment name as parameter.
run_template_csv.sh: Contains the actual sequence of modules in DeepTFni. These modules are listed below in order of execution:

1-ATAC_peaks.pl
Cleans ATACseq data by removing peaks that are found in less than 10% of overall cells.

2-SequenceGet.pl
Extract fasta file from chromosome number and coordinates in ATACseq file.

3-fimo.pl
3-fimo.py (due to issues running fimo.pl, this was developed as the main fimo file)
Detect TF motifs that are present in fasta file.

4-Get_TFBS_region.pl
Extracts sequences with detected TF binding sites.

5-GetMatrix.pl
Generates initial TF adjacency matrix.

6_dense_matrix_2_h5_for_MAESTRO_input.py
Generates de-sparsified matrix using 10X HDF5 file format for MAESTRO processing.

Run MAESTRO code (in MAESTRO folder):
This code has been modified from its original github source to fit our pipeline. It contains:
scATAC_Genescore.py 
Generates gene scores for ATACseq data
scATAC_H5Process.py
Process HDF5 file format for calculation of gene scores
scATAC_utility.py 
Supplementary functions for conversion of ATACseq data

7_for_TF_rp_score_ALT.R
7_for_TF_rp_score.R
Generates RP/regulatory potential scores for TFs in adjacency matrix. 
"ALT" suffix indicates experimentation script and is not used in final pipeline.

8_data_preparation_for_DeepTFni_GENE.py
8_data_preparation_for_DeepTFni.py
Prepares data for training, this includes checking validity of adjacency matrix (cannot contain all 0/1's). Formation of train/test pairs from majority sampling given negative links are the dominant class. 

9_train_DeepTFni_ALT.py
9_train_DeepTFni_GENE.py
9_train_DeepTFni.py
Initially TF RP score is the node feature and adjacency matrices are the edge feature. 
To expand the node feature, we implemented concatenation of RNAseq data in this script:
concatenate_rnaseq.py
To expand the edge feature, we implemented TF-target gene relationships in this script:
expand_adj_matrix.py
"GENE" suffix indicates it modified the script to accept expansion of initial adjacency matrix, including recalculation and reshaping of TF RP score table to complement new adjacency matrix.
"ALT" suffix indicates experimentation script and is not used in final pipeline.

10_weighted_2_binary_GENE.py
10_weighted_2_binary.py
Processes and transforms output across multiple replicates and folds, converting into a final predicted binary matrix.
"GENE" suffix indicates this version of the module is to be used when TF-target gene information is incorporated in the architecture.

11_integrated_output_GENE.py
11_integrated_output.py

Generates final TF lists and aggregated matrices and outputs into summary directory for further analysis. "GENE" suffix indicates this version of the module is to be used when TF-target gene information is incorporated in the architecture.

supplementary.ipynb
Contains accuracy/precision/recall calculation functions, graph plotting functions, and other analysis functions.

generating_network_graphs.ipynb: creates graph networks figures to visualize the differences between the TRN skeleton and model's predicted output

Other files with name format of run_(experiment name).sh, ex. run_ALS_ATAC_Astro_subset.sh, are generated per experiment based on filename given to run_DeepTFni_csv.pl.

final_report.pdf: project write up

## Running

To test-run the project on sample input, execute this line of code in run_DeepTFni.ipynb:
!perl /content/drive/MyDrive/deeptfni/run_DeepTFni_csv.pl /content/drive/MyDrive/deeptfni/Input_data hg19
Where hg19 is default reference genome.
Ensure that $my_dir variable in 1-ATAC_peaks.pl is also set to Input_data.

To run the project on true files, simply change argument to run_DeepTFni_csv.pl as well as previously indicated variable $my_dir to whichever folder contains true data.
