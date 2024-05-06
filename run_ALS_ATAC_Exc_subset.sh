#! /bin/bash

sample_type="ALS_ATAC_Exc_subset"
echo "processing $sample_type"

reference="hg19"
echo "using reference $reference"

# ##### 	generate initial adjacency matrix	#####
# command_1=`perl /content/drive/MyDrive/deeptfni/1-ATAC_peaks.pl $sample_type $reference`
# echo $command_1

# # command_1="python /content/drive/MyDrive/deeptfni/6_dense_matrix_2_h5_for_MAESTRO_input.py -sample $input -input_file $input_file -output_dir $out_dir");
# # echo $command_1

# # command_1=`perl /content/drive/MyDrive/deeptfni/4-Get_TFBS_region.pl $sample_type`
# # echo $command_1

# #####	generate RP score using MAESTRO	#####
# command_2=`python /content/drive/MyDrive/deeptfni/MAESTRO/scATAC_Genescore.py scatac-genescore --format h5 --peakcount /content/drive/MyDrive/deeptfni/$sample_type/8_$sample_type\_peak_count.h5 --genedistance 10000 --species GRCh38 --model Enhanced --outprefix /content/drive/MyDrive/deeptfni/$sample_type/9_$sample_type`
# #make sure to use Absolute Path for MAESTRO scatac-genescore function
# echo $command_2

# #####	    extract TF RP score as feature matrix	#####
# command_3=`Rscript /content/drive/MyDrive/deeptfni/7_for_TF_rp_score.R $sample_type`
# echo $command_3

#####	        split data set for DeepTFni		#####
# require source ~/.bashrc
command_4=`python /content/drive/MyDrive/deeptfni/8_data_preparation_for_DeepTFni_NEW.py -sample $sample_type`
echo $command_4

#####	               train DeepTFni	        	#####
command_5=`python /content/drive/MyDrive/deeptfni/9_train_DeepTFni_NEW.py -sample $sample_type`
echo $command_5

#####	               organize output	#####
command_6=`python /content/drive/MyDrive/deeptfni/10_weighted_2_binary_NEW.py -sample $sample_type`
echo $command_6
command_7=`python /content/drive/MyDrive/deeptfni/11_integrated_output_NEW.py -sample $sample_type`
echo $command_7

#####		organize file		#####
#echo "mv /content/DeepTFni-main/$sample_type/file_to_remove"

