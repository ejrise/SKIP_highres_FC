#!/bin/bash -l
###########################################################################################################################################

#Set up the environmental variables
FSLDIR=/sw/fsl
. ${FSLDIR}/etc/fslconf/fsl.sh
PATH=${FSLDIR}/bin:${PATH}
export FSLDIR PATH
export PATH=$PATH:/sw/afni/bin

###########################################################################################################################################

subjects=()


for sub in "${subjects[@]}"; do
 echo "Processing subject: $sub"
 base_dir="/path/to/base/dir"
 sub_dir=$base_dir/$sub
 mni=$base_dir/MNI152_T1_2mm_brain.nii.gz

 #transform all fishZmaps to MNI space 
 fishz_path=$base_dir"/fishZmaps/fishZmaps_nativespace"

 find "$fishz_path" -type f -name $sub"_bin*" | while read -r file_path; do
  file_name=$(basename "$file_path")
  echo "the file name is" $file_name
  variable_name="${file_name%.nii}"
  echo "Transforming region: $variable_name"
  antsApplyTransforms -d 3 -e 3 -i $file_path -r $mni -t $sub_dir/$sub"_antshighres2mni1Warp.nii.gz" -t $sub_dir/$sub"_antshighres2mni0GenericAffine.mat" -o $base_dir"/fishZmaps/"$variable_name"_to_mni_ants.nii.gz"
  #flirt -in $file_path -ref $mni -applyxfm -init $sub_dir/$sub"_flirthighres2mni.mat" -out $base_dir/"fishZmaps/"$variable_name"_to_mni.nii.gz" 
 done
done 
