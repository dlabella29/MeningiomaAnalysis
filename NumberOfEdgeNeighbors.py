import os
import nibabel as nib
import numpy as np
import pandas as pd
from datetime import datetime

# Define the main directory path
main_folder_path = r"D:\BraTSMets\ASNR-MICCAI-BraTS2023-MET-Challenge-TrainingData"

# Function to count border voxels
def count_border_voxels(label_array, t1c_array):
    border_voxel_count = 0
    # Iterate through the label array
    for x in range(1, label_array.shape[0] - 1):
        for y in range(1, label_array.shape[1] - 1):
            for z in range(1, label_array.shape[2] - 1):
                if label_array[x, y, z] > 0:  # If voxel is part of the label
                    # Check neighbors in the t1c array
                    neighbors = [t1c_array[x-1:x+2, y, z].flatten(),
                                 t1c_array[x, y-1:y+2, z].flatten(),
                                 t1c_array[x, y, z-1:z+2].flatten()]
                    if 0 in np.concatenate(neighbors):
                        border_voxel_count += 1
    return border_voxel_count

# Function to calculate volumes of label values
def calculate_volumes(label_array, voxel_volume):
    volumes = {1: 0, 2: 0, 3: 0}
    for label_value in volumes.keys():
        volumes[label_value] = np.sum(label_array == label_value) * voxel_volume
    return volumes

# Results list
results = []

# Iterate through each case folder
for case_folder in os.listdir(main_folder_path):
    case_path = os.path.join(main_folder_path, case_folder)
    if os.path.isdir(case_path):
        seg_file_path = os.path.join(case_path, f'{case_folder}-seg.nii.gz')
        t1c_file_path = os.path.join(case_path, f'{case_folder}-t1c.nii.gz')

        # Load NIfTI files
        seg_img = nib.load(seg_file_path)
        t1c_img = nib.load(t1c_file_path)

        # Convert NIfTI images to numpy arrays
        seg_array = seg_img.get_fdata()
        t1c_array = t1c_img.get_fdata()

        # Calculate voxel volume from header (assuming cubic voxels for simplicity)
        voxel_dims = seg_img.header.get_zooms()
        voxel_volume = voxel_dims[0] * voxel_dims[1] * voxel_dims[2]

        # Count border voxels
        border_voxels = count_border_voxels(seg_array, t1c_array)

        # Calculate volumes for label values
        volumes = calculate_volumes(seg_array, voxel_volume)

        # Append results
        results.append({'Case': case_folder,
                        'Border Voxels': border_voxels,
                        'Volume Label 1': volumes[1],
                        'Volume Label 2': volumes[2],
                        'Volume Label 3': volumes[3]})

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Save results to an Excel file
time_suffix = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
filename = f"C:\\Users\\dlabe\\Documents\\Mets_volumes_and_border_voxels_{time_suffix}.xlsx"
results_df.to_excel(filename, index=False)

print(f"Results saved to {filename}")
