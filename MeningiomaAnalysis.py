import os
import glob
import numpy as np
import nibabel as nib
import pandas as pd
from scipy.spatial.distance import dice, cdist
from scipy.ndimage import label
from scipy.ndimage import label, center_of_mass

def calculate_volume(mask, voxel_dimensions):
    return np.sum(mask) * np.prod(voxel_dimensions)
def dice_similarity(mask1, mask2):
    intersection = np.sum(mask1 & mask2)
    return 2. * intersection / (np.sum(mask1) + np.sum(mask2))
def count_discrete_lesions(mask, voxel_dimensions, min_distance=6, min_volume=30):
    labeled_array, num_features = label(mask)
    centroids = center_of_mass(mask, labeled_array, range(1, num_features+1))
    distances = cdist(centroids, centroids)

    discrete_lesion_count = 0
    for i in range(1, num_features + 1):
        lesion_volume = calculate_volume(labeled_array == i, voxel_dimensions)
        if lesion_volume < min_volume:
            continue
        if all(distances[i - 1, j] >= min_distance or i - 1 == j for j in range(num_features)):
            discrete_lesion_count += 1

    return discrete_lesion_count

save_dir = "SAVE_FILE_PATH"
base_dir = "DATA_FILE_PATH"
results = []

for folder_path in glob.glob(os.path.join(base_dir, '*')):
    folder_name = os.path.basename(folder_path)

    SSMen_path = os.path.join(folder_path, folder_name + '_tumor-seg-gtv.nii.gz')
    FSMen_path = os.path.join(folder_path, folder_name + '_tumor-seg-manual.nii.gz')
    SSImg_path = os.path.join(folder_path, folder_name + '_t1c_wm.nii.gz')

    SSMen_img = nib.load(SSMen_path)
    FSMen_img = nib.load(FSMen_path)
    SSImg_img = nib.load(SSImg_path)

    SSMen_data = SSMen_img.get_fdata() > 0
    FSMen_data = FSMen_img.get_fdata() > 0
    SSImg_data = SSImg_img.get_fdata() == 0

    voxel_dimensions = SSMen_img.header.get_zooms()

    num_lesions = count_discrete_lesions(FSMen_data, voxel_dimensions)

    SSMen_vol = calculate_volume(SSMen_data, voxel_dimensions)
    FSMen_vol = calculate_volume(FSMen_data, voxel_dimensions)
    overlap_vol = calculate_volume(SSMen_data & FSMen_data, voxel_dimensions)
    FSMen_not_SSMen_vol = calculate_volume(FSMen_data & ~SSMen_data, voxel_dimensions)
    FSMen_not_SSMen_SSImg0_vol = calculate_volume(FSMen_data & ~SSMen_data & SSImg_data, voxel_dimensions)
    SSMen_SSImg0_vol = calculate_volume(SSMen_data & SSImg_data, voxel_dimensions)
    FSMen_SSImg0_vol = calculate_volume(FSMen_data & SSImg_data, voxel_dimensions)
    relative_increase = (FSMen_vol / SSMen_vol)*100 - 100 if SSMen_vol != 0 else np.nan
    dice_coef = dice_similarity(SSMen_data, FSMen_data)

    results.append([folder_name, SSMen_vol, FSMen_vol, overlap_vol, FSMen_not_SSMen_vol,
                    FSMen_not_SSMen_SSImg0_vol, SSMen_SSImg0_vol, FSMen_SSImg0_vol,
                    relative_increase, dice_coef,num_lesions])

columns = ["Case", "SSMen_Volume", "FSMen_Volume", "Overlap_Volume",
           "FSMen_Not_SSMen_Volume", "FSMen_Not_SSMen_SSImg0_Volume", "SSMen_SSImg0_Volume",
           "FSMen_SSImg0_Volume", "Relative_Increase_Volume", "Dice_Coefficient","Number of Lesions"]

df = pd.DataFrame(results, columns=columns)
output_path = os.path.join(save_dir, "SAVE_FILE_NAME.xlsx")
df.to_excel(output_path, index=False)
