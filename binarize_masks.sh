#!/bin/bash

# Set the parent directory containing the subject directories
parent_dir="/path/to/sub/mask/folders"

# Iterate through subject directories
for subject_dir in "$parent_dir"/*_region_masks; do
    if [ -d "$subject_dir" ]; then
        echo "Processing masks in directory: $subject_dir"
        
        # Iterate through mask files
        for mask_file in "$subject_dir"/*.nii.gz; do
            if [ -f "$mask_file" ]; then
                echo "Processing mask: $mask_file"
                
                # Extract the filename without path and extension
                mask_filename=$(basename "$mask_file" .nii.gz)
                
                # Apply fslmaths -bin to binarize the mask
                fslmaths "$mask_file" -thrP 25 -bin "$subject_dir/bin_$mask_filename.nii.gz"
                
                echo "Binarized and renamed to: $subject_dir/bin_$mask_filename.nii.gz"
            fi
        done
    fi
done
