import numpy as np
#import nrrd
import os
import nibabel as nib
import torch
from matplotlib import pyplot as plt
import cc3d
from metrics import*
    
def flatten_seg(segmentation_file):
    segmentation_nii_file = nib.load(segmentation_file)
    segmentation_img_data = segmentation_nii_file.get_fdata()
    print("segmentation file ok")
    
    segmentation_img_tensor = torch.tensor(segmentation_img_data, dtype=torch.float32).squeeze()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu") 

    segmentation_img_tensor = segmentation_img_tensor.to(device) 

    print("Flattening...")
    
    segmentation_img_tensor=segmentation_img_tensor.squeeze()
    if len(segmentation_img_tensor.shape)>3:
        segmentation_sum = segmentation_img_tensor.sum(dim=-1)
    else:
        segmentation_sum = segmentation_img_tensor
    
    segmentation_sum=segmentation_sum>0
    
    #segmented_suv_file=nib.Nifti1Image(segmentation_sum.cpu().numpy(),nib.load(segmentation_file).affine, nib.load(segmentation_file).header)
    #nib.save(segmented_suv_file,'flatten.nii.gz')
    return segmentation_sum.cpu().numpy()

def connected_cops(segmentation_array):
    print("Decomposing...")
    return cc3d.connected_components(segmentation_array, connectivity=6,out_dtype=np.uint32)

def threshold_suv(suv_file,flattened_seg,suv_threshold=4):
    suv_nii_file = nib.load(suv_file)
    suv_img_data = suv_nii_file.get_fdata()

    suv_img_tensor = torch.tensor(suv_img_data, dtype=torch.float32).squeeze()
    segmentation_img_tensor = torch.tensor(flattened_seg, dtype=torch.int32).squeeze()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu") 
    
    thresholded_segmentation_mask=torch.zeros(suv_img_data.shape).to(device)

    print("suv_img_tensor.shape= ",suv_img_tensor.shape)
    print("segmentation_img_tensor.shape=",segmentation_img_tensor.shape)
    if suv_img_tensor.shape[:2] != segmentation_img_tensor.shape[:2]:
        print("WARNING : SEGMENTATION AND SUV_FILE MUST BE THE SAME SIZE")
        return

    suv_img_tensor = suv_img_tensor.to(device) 
    segmentation_img_tensor = segmentation_img_tensor.to(device) 

    print("Thresholding...")

    # Create a boolean mask where segmentation_sum is greater than 0 
    segmentation_mask = segmentation_img_tensor > 0 
    print("segmentation_mask voxels :",(int)(torch.sum(segmentation_mask))," voxels")

    # Create a boolean mask where suv_img_tensor is greater than the threshold 
    suv_threshold_mask = suv_img_tensor > suv_threshold 
    print("suv_threshold_mask voxels :",(int)(torch.sum(suv_threshold_mask))," voxels")
    # Combine the two masks 
    
    print("segmentation_mask.shape : ",segmentation_mask.shape)
    print("suv_threshold_mask.shape : ",suv_threshold_mask.shape)
    combined_mask = segmentation_img_tensor * suv_threshold_mask 

    #seg_img = nib.Nifti1Image(segmentation_mask.cpu().numpy(), segmentation_nii_file.affine, segmentation_nii_file.header)
    #suv_img = nib.Nifti1Image(suv_threshold_mask.cpu().numpy(), suv_nii_file.affine, suv_nii_file.header)
    #nib.save(seg_img,"segmentation_mask.nii.gz")
    #nib.save(suv_img,"suv_threshold_mask.nii.gz")

    # Move the result back to CPU and convert to numpy array if needed 

    thresholded_segmentation = combined_mask.cpu().numpy() 
    thresholded_segmentation_mask[segmentation_mask * suv_threshold_mask]=1
    print("Number of voxels in thresholded segmentation : ",torch.sum(thresholded_segmentation_mask)," voxels")
    print("Thresholding done")
    return thresholded_segmentation

def generate_thresholded_file(suv_file,segmentation_file,output_file_name,gt,suv_threshold=4):
    flattened_seg=flatten_seg(segmentation_file)
    flattened_seg_cc3d=connected_cops(flattened_seg)
    thresholded_segmentation=threshold_suv(suv_file,flattened_seg_cc3d,suv_threshold)
    segmented_suv_file=nib.Nifti1Image(thresholded_segmentation,nib.load(gt).affine, nib.load(gt).header)
    nib.save(segmented_suv_file,output_file_name)

    


    