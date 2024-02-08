%This code inputs preprocessed functional brain data along with region masks that you want as seed regions. 
%It outputs a fisher's Z map with voxel-wise connectivity to inputted region seed mask. 
% 
%Region masks and functional data must be in the same space (i.e. MNI space or subject anatomical space). 
% 
% Code depends on fisherZcorr.m 


clear all;
close all;

% Define a cell array of subjects
subjects = {'subject_id'};

% Iterate through subjects
for subject_index = 1:length(subjects)
    subject = subjects{subject_index};
    fprintf('Processing subject: %s\n', subject);
    % Define a cell array of region mask file paths
    region_masks = {
    ['/path/to/mask/folder/',subject,'_region_masks/region_mask_in_X_space.nii.gz']
    ['/path/to/mask/folder/',subject,'_region_masks/region_mask_in_X_space.nii.gz'],
  }; 
    % Iterate through the region masks
    for mask_index = 1:length(region_masks)
        ROImask_dir_file = region_masks{mask_index};
        fprintf('Processing mask: %s\n', ROImask_dir_file);
        
        % Extract just the filename without the path
        [~, mask_filename, ~] = fileparts(ROImask_dir_file);
        
        % Remove the common ending from the mask name
        common_ending = '_in_X_space.nii.gz';
        mask_name = strrep(mask_filename, common_ending, '');
        
        % Start the timer
        tic;
        
        BOLD_dir_file = ['/path/to/func/',subject,'_func.nii.gz'];

        BOLD_hdr = spm_vol(BOLD_dir_file);
        BOLD_data = spm_read_vols(BOLD_hdr);

        ROImask_hdr = spm_vol(ROImask_dir_file);
        ROImask_data = spm_read_vols(ROImask_hdr);

        % Find inds of ROI
        ROI_inds = find(ROImask_data);
        [xm, ym, zm] = ind2sub(size(ROImask_data), ROI_inds);

        seed = zeros(1, size(BOLD_data, 4));
        for vox = 1:size(ROI_inds, 1)
            seed = seed + squeeze(BOLD_data(xm(vox), ym(vox), zm(vox), :))';
        end
        seed = seed / size(ROI_inds, 1);

        [X, Y, Z, T] = size(BOLD_data);

        R_map = zeros(X, Y, Z);

        for x = 1:X
            for y = 1:Y
                for z = 1:Z
                    if mean(squeeze(BOLD_data(x, y, z, :))) ~= 0  % OUR TEST FOR NOW OF INSIDE BRAIN OR NOT
                        fishZ = fisherZcorr(seed, squeeze(BOLD_data(x, y, z, :))');
                        R_map(x, y, z) = fishZ;
                    end
                end
            end
        end

        % Modify the output file name based on the region mask name
        output_filename = ['/path/to/folder/',subject,'_', mask_name,'_fishZmap.nii'];

        Vout = ROImask_hdr;
        Vout.fname = output_filename;
        spm_write_vol(Vout, R_map);
        
        % Stop the timer and display the elapsed time
        elapsed_time = toc;
        fprintf('Elapsed time for subject %s, mask %s: %.2f seconds\n', subject, mask_name, elapsed_time);
    end
end


