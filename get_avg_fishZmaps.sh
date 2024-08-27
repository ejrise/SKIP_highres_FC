#!/bin/bash

# Define the list of subjects
subjects=("sub-01")

# Define the list of brain regions
regions=("left_accumbens_thr50" "left_AMY_BL_Complex" "left_AMY_CEN" "left_BF_ch4" "left_CMA" "left_dorsal_putamen" "left_GPi_pauli" "left_precentral_gyrus_A4ul_thr25" "left_SMA" "left_STH_pauli" "left_Thal_VL_AAL3" "left_ventral_putamen" "right_accumbens_thr50" "right_AMY_BL_Complex" "right_AMY_CEN" "right_BF_ch4" "right_CMA" "right_dorsal_putamen" "right_GPi_pauli" "right_precentral_gyrus_A4ul_thr25" "right_SMA" "right_STH_pauli" "right_Thal_VL_AAL3" "right_ventral_putamen")

# Create a directory to store intermediate results
mkdir -p results

# Loop through each region
for region in "${regions[@]}"; do
  echo "Processing region: $region"

  # Initialize an array to store thresholded images for each subject
  pos_images=()
  neg_images=()
  nothresh_images=()

  # Threshold and binarize each subject's image for the current region
  for subject in "${subjects[@]}"; do
    echo "Processing subject: $subject"
    fslmaths "${subject}_bin_${region}_fishZmap_to_mni_ants.nii.gz" -thr 0 "results/${subject}_bin_${region}_thresholded_pos.nii.gz"
    fslmaths "${subject}_bin_${region}_fishZmap_to_mni_ants.nii.gz" -uthr 0 "results/${subject}_bin_${region}_thresholded_neg.nii.gz"
    scp "${subject}_bin_${region}_fishZmap_to_mni_ants.nii.gz" "results/${subject}_bin_${region}_nothreshold.nii.gz"
    pos_images+=("results/${subject}_bin_${region}_thresholded_pos.nii.gz")
    neg_images+=("results/${subject}_bin_${region}_thresholded_neg.nii.gz")
    nothresh_images+=("results/${subject}_bin_${region}_nothreshold.nii.gz")
  done

  # Concatenate thresholded images for all subjects into a 4D image
  fslmerge -t "results/${region}_combined_pos.nii.gz" "${pos_images[@]}"
  fslmerge -t "results/${region}_combined_neg.nii.gz" "${neg_images[@]}"
  fslmerge -t "results/${region}_combined_nothreshold.nii.gz" "${nothresh_images[@]}"

  # Take the mean across the concatenated images
  fslmaths "results/${region}_combined_pos.nii.gz" -Tmean "results/${region}_average_pos.nii.gz"
  fslmaths "results/${region}_combined_neg.nii.gz" -Tmean "results/${region}_average_neg.nii.gz"
  fslmaths "results/${region}_combined_nothreshold.nii.gz" -Tmean "results/${region}_average_nothresh.nii.gz"
done

echo "Processing complete."

