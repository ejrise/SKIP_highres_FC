#!/bin/bash

# Base directory
base_dir='/path/to/tedana/processed/bolds'

# List of subjects
subjects=()
# Loop through each subject
for subject_id in "${subjects[@]}"; do
    echo "Processing subject: $subject_id"

    # Paths to input files
    input_bold="${base_dir}/${subject_id}_desc-denoised_bold.nii.gz"
    regressors_file="/path/to/physio/regressors/multiple_regressors.txt"
 

    # Check if input files exist
    if [[ ! -f "$input_bold" ]]; then
        echo "Error: Input BOLD file not found for $subject_id"
        continue
    fi

    if [[ ! -f "$regressors_file" ]]; then
        echo "Error: Regressors file not found for $subject_id"
        continue
    fi

    if [[ ! -f "$motion_outliers" ]]; then
        echo "Error: Motion outliers file not found for $subject_id"
        continue
    fi

    # Step 1: Regress out nuisance variables
    output_clean="${base_dir}/${subject_id}_desc-denoised_bold_clean.nii.gz"
    fsl_regfilt -i "$input_bold" -d "$regressors_file" -o "$output_clean" -f "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18"

    # Step 2: Smooth the output with a 2.5mm kernel
    output_smooth="${base_dir}/${subject_id}_desc-denoised_bold_clean_smooth.nii.gz"
    fslmaths "$output_clean" -s 1.061 "${output_smooth}"

    echo "Completed processing for $subject_id"
done

echo "All subjects processed."
