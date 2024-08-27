#!/bin/bash

# Directory containing the connectivity map images
connectivity_dir="/path/to/fishZmaps"

# Initialize a variable to store the output filename
output_file="mean_connectivity_values_lefthem.csv"

# Write header to CSV file
echo "Subject_ID,Connectivity_Map,Mask,Mean_Connectivity_Value,Std_Deviation,Percentile_50,Min_Value,Max_Value,Max_Voxel_Coordinates" > "$output_file"

# Iterate through each subject's folder
for subject_dir in /path/to/sub/folders; do
    # Extract subject ID from the folder name
    subject_id=$(basename "$subject_dir" | cut -d'_' -f3)
    echo "Processing subject: $subject_id"

    # Find all files with "bin" in their names in the subject's mask folder and store their full paths
    masks=()
    while IFS= read -r -d $'\0'; do
        if [[ "$REPLY" != *"bilateral"* ]]; then
            masks+=("$REPLY")
        fi
    done < <(find "$subject_dir" -maxdepth 1 -type f -name "*bin_*" -print0)

    # Check if bin masks were found
    if [ ${#masks[@]} -eq 0 ]; then
        echo "No valid bin masks found in the directory for subject $subject_id."
        continue
    fi

    # Iterate through each mask
    for mask in "${masks[@]}"; do
        echo "Processing mask: $mask"
        # Iterate through each connectivity map, excluding those with "bilateral" in the filename
        for connectivity_map in "$connectivity_dir"/*"${subject_id}_bin_left_"* "$connectivity_dir"*/*"${subject_id}_bin_frontmed_"*; do
			
			echo "Processing fishZmap: $connectivity_map"

            # Extract the mask name without extension and suffix
            mask_name=$(basename "$mask" .nii.gz | sed 's/_MNI_2mm_to_t1_flirt//')
            
            # Extract the connectivity map name without extension and suffix
            connectivity_map_name=$(basename "$connectivity_map" _fishZmap.nii)
            
            # Extract the subject ID from the connectivity map name
            connectivity_map_subject_id=$(echo "$connectivity_map_name" | cut -d'_' -f3)
            
            # Remove the subject ID from the connectivity map name
            connectivity_map_name_without_id=$(echo "$connectivity_map_name" | sed 's/7T_control_.*_bin_//')
            
            # Check if subject ID matches for the connectivity map
            if [ "$connectivity_map_subject_id" != "$subject_id" ]; then
                continue
            fi
            
            # Apply the mask to the connectivity map and calculate the required statistics
            mean_connectivity=$(fslstats "$connectivity_map" -k "$mask" -M)
            sd_connectivity=$(fslstats "$connectivity_map" -k "$mask" -S)
            percentile_50=$(fslstats "$connectivity_map" -k "$mask" -P 50)
            min_value=$(fslstats "$connectivity_map" -k "$mask" -R | awk '{print $1}')
            max_value=$(fslstats "$connectivity_map" -k "$mask" -R | awk '{print $2}')
            max_voxel_coords=$(fslstats "$connectivity_map" -k "$mask" -x | awk '{print $1, $2, $3}')
            
            # Write to CSV file
            echo "${subject_id},${connectivity_map_name_without_id},${mask_name},${mean_connectivity},${sd_connectivity},${percentile_50},${min_value},${max_value},${max_voxel_coords}" >> "$output_file"
        done
    done
done

echo "Connectivity statistics of masks applied to connectivity maps saved in '$output_file'."

