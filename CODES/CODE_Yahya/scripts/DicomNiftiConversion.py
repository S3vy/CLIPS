import os
import pydicom
import pandas as pd
import gzip
import shutil
import json
import csv
import dicom2nifti
import nibabel as nib
# from rt_utils import RTStructBuilder
import numpy as np
import SimpleITK as sitk
import dicom2nifti.settings as settings
import dicom2nifti.convert_generic as convert_generic
# from helper import winapi_path, bqml_to_suv
from datetime import datetime

import platform
import dateutil



def convert_dicom_to_nifti(dicom_folder,output_file):
    # Convert the DICOM folder to NIfTI
    settings.disable_validate_slice_increment() #ignore slice increment discrepancies 
    dicom_input=dicom2nifti.common.read_dicom_directory(dicom_folder)

    # remove duplicate slices based on position and data
    dicom_input = convert_generic.remove_duplicate_slices(dicom_input)

    # remove localizers based on image type
    dicom_input = convert_generic.remove_localizers_by_imagetype(dicom_input)

    # remove_localizers based on image orientation (only valid if slicecount is validated)
    dicom_input = convert_generic.remove_localizers_by_orientation(dicom_input)

    grouped_dicoms = convert_generic.get_grouped_dicoms(dicom_input)

    if convert_generic.is_4d(grouped_dicoms):
        return _four_d_to_nifti(grouped_dicoms, output_file)

    return convert_generic.dicom_to_nifti(dicom_input, output_file)


def winapi_path(dos_path, encoding=None):
    path = os.path.abspath(dos_path)
    if platform.system() == 'Windows':
        if path.startswith("\\\\"):
            path = "\\\\?\\UNC\\" + path[2:]
        else:
            path = "\\\\?\\" + path

    return path


def bqml_to_suv(dcm_file: pydicom.FileDataset) -> float:
    '''
    Calculates the conversion factor from Bq/mL to SUV bw [g/mL] using 
    the dicom header information in one of the images from a dicom series
    '''
    # TODO: You can access these attributes in a more user friendly way rather
    # than using the codes...change this at some point
    manufacturer = dcm_file[0x00080070].value.lower()
    units = dcm_file[0x00541001].value.lower()
    unitIsNotBqml = "bqml" not in units
    if "philips" in manufacturer and unitIsNotBqml:
        print("Philips")
        suv_factor = float(dcm_file[0x70531000].value)
    else:
        nuclide_dose = dcm_file[0x054, 0x0016][0][0x0018, 0x1074].value  # Total injected dose (Bq)
        weight = dcm_file[0x0010, 0x1030].value  # Patient weight (Kg)
        half_life = float(dcm_file[0x054, 0x0016][0][0x0018, 0x1075].value)  # Radionuclide half life (s)

        parse = lambda x: dateutil.parser.parse(x)

        series_time = str(dcm_file[0x0008, 0x00031].value)  # Series start time (hh:mm:ss)
        series_date = str(dcm_file[0x0008, 0x00021].value)  # Series start date (yyy:mm:dd)
        series_datetime_str = series_date + ' ' + series_time
        series_dt = parse(series_datetime_str)

        nuclide_time = str(dcm_file[0x054, 0x0016][0][0x0018, 0x1072].value)  # Radionuclide time of injection (hh:mm:ss)
        nuclide_datetime_str = series_date + ' ' + nuclide_time
        nuclide_dt = parse(nuclide_datetime_str)

        delta_time = (series_dt - nuclide_dt).total_seconds()
        decay_correction = 2 ** (-1 * delta_time/half_life)
        suv_factor = (weight * 1000) / (decay_correction * nuclide_dose)
    Rescale_Slope= dcm_file[0x0028,0x1053].value
    Rescale_Intercept=dcm_file[0x0028,0x1052].value

    return (suv_factor, Rescale_Slope, Rescale_Intercept)


def list_of_modality_dirs(input_dir):
    # scan the input dir for directories containing DICOM series
    # determine which directory corresponds to which modality
    dir_list = next(os.walk(input_dir))[1]
    pt_dir_list={}
    ct_dir_list={}
    pt_dir=None
    numberOfCorrections=0
    for direc in dir_list:
        file_list = os.listdir(os.path.join(input_dir, direc))
        for file in file_list:
            filename = os.path.join(input_dir, direc, file)
            if filename.endswith(".dcm"):
                ds = pydicom.read_file(filename)
                Patient_ID = ds.PatientID
                if ds.Modality == 'PT':
                    print('Found PET DIR')
                    if numberOfCorrections<len(ds[0x00280051].value):
                        numberOfCorrections = len(ds[0x00280051].value) #prend le dossier pet avec le plus de corrections
                        pt_dir_list={}
                        pt_dir_list[os.path.join(input_dir,direc)]=ds.SeriesDescription if 'SeriesDescription' in ds else ""
                        break
                    elif numberOfCorrections==len(ds[0x00280051].value):
                        pt_dir_list[os.path.join(input_dir,direc)]=ds.SeriesDescription if 'SeriesDescription' in ds else ""
                    break
                elif ds.Modality == 'CT':
                    print('Found CT DIR')
                    ct_dir_list[os.path.join(input_dir,direc)]=ds.SeriesDescription if 'SeriesDescription' in ds else ""
                    break
                else:
                    print('Found dir without PET or CT')
                    break
    if pt_dir_list=={}:
        print("Could not find PET DIR")
        os._exit(0)
    if ct_dir_list=={}:
        print("Could not find CT DIR")
        os._exit(0)
    else:
        if len(pt_dir_list)>1:
            print(f"Multiple corrected PET files found, please enter the path of the correct file : ", )
            for element in (pt_dir_list):
                print(f'{pt_dir_list[element]}'," "*(max([len(pt_dir_list[j]) for j in pt_dir_list])-len(pt_dir_list[element])),f'{element}')
            choice= input("Enter path : ")
            pt_dir=choice
        else:
            for element in pt_dir_list:
                pt_dir=element
        if len(ct_dir_list)>1:
            print(f"Multiple corrected CT files found, please enter the path of the correct file : ", )
            for element in (ct_dir_list):
                print(f'{ct_dir_list[element]}'," "*(max([len(ct_dir_list[j]) for j in ct_dir_list])-len(ct_dir_list[element])),f'{element}')
            ct_dir= input("Enter path : ")
        else:
            for element in ct_dir_list:
                ct_dir=element
        modality_dirs = {'PT':pt_dir, 'CT':ct_dir, 'ID': Patient_ID}
    return modality_dirs

def read_slices_from_dir(input_dir):
    # read and sort .dcm slices from a directory
    # first, read all dicom files
    dicom_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".dcm"):
                filename_full = os.path.join(root, file)
                ds = pydicom.read_file(filename_full)
                dicom_files.append(ds)
    # second, only choose files that have 'location' attribure, and sort
    slices = []
    skipcount = 0
    # only include dicom files that represent image slices
    for f in dicom_files:
        if skipcount>=len(dicom_files)//2:
            a='y' #input("Warning : More than half files in series have no SliceLocation tag, do you wish to ignore this tag? (y/n)")
            if a.lower()=='y':
                #return dicom_files
                #elif a.lower()=='n':
                slices = []
                skipcount = 0
                for f in dicom_files:    
                    if hasattr(f, 'SliceLocation'):
                        slices.append(f)
                    else:
                        skipcount += 1
            #print('Skipped {} files'.format(skipcount))
                slices = sorted(slices,key=lambda s: s.SliceLocation)
                return slices
        if hasattr(f, 'SliceLocation'):
            slices.append(f)
        else:
            skipcount += 1
    #print('Skipped {} files'.format(skipcount))
    slices = sorted(slices,key=lambda s: s.SliceLocation)
    return slices


def dicomToNifti(seriesDir, savePath):
    # converts DICOM series in the seriesDir to NIFTI image in the savePath specified
    for root, dirs, files in os.walk(seriesDir):
        for file in files:
            if file.endswith('.dcm'):
                filename = os.path.join(root, file)
                ds = pydicom.dcmread(filename, force=True)
                break

    traits = {
            "Patient ID":
            getattr(ds, 'PatientID', None),
            "Patient's Sex":
            getattr(ds, 'PatientSex', None),
            "Patient's Age":
            getattr(ds, 'PatientAge', None),
            "Patient's Birth Date":
            getattr(ds, 'PatientBirthDate', None),
            "Patient's Weight":
            getattr(ds, 'PatientWeight', None),
            "Institution Name":
            getattr(ds, 'InstitutionName', None),
            "Referring Physician's Name":
            getattr(ds, 'ReferringPhysicianName', None),
            "Operator's Name":
            getattr(ds, 'OperatorsName', None),
            "Study Date":
            getattr(ds, 'StudyDate', None),
            "Study Time":
            getattr(ds, 'StudyTime', None),
            "Modality":
            getattr(ds, 'Modality', None),
            "Series Description":
            getattr(ds, 'SeriesDescription', None),
            "Dimensions":
            np.array(getattr(ds, 'pixel_array', None)).shape,
        }

    reader = sitk.ImageSeriesReader()
    seriesNames = reader.GetGDCMSeriesFileNames(seriesDir)
    reader.SetFileNames(seriesNames)
    image = reader.Execute()
    image_array = sitk.GetArrayFromImage(image)

    if traits["Modality"] == 'PT':
        pet = pydicom.dcmread(seriesNames[0])  # read one of the images for header info
        suv_result = bqml_to_suv(pet)
        suv_factor = suv_result[0]
        Rescale_Slope = suv_result[1]
        Rescale_Intercept = suv_result[2]

        #image = sitk.Multiply(image, Rescale_Slope)
        #image = image + Rescale_Intercept
        #image = sitk.Multiply(image, suv_factor)
        convert_dicom_to_nifti(seriesDir,'temp.nii')
        image_float = nib.load('temp.nii').get_fdata()
        image_float = image_float*suv_factor
        #image_float= np.flip(image_float,1) #Because this way, data is in the same format as sitk extracted data, this way the model gets data the way it's supposed to
        suv_img = nib.Nifti1Image(image_float, nib.load('temp.nii').affine, nib.load('temp.nii').header)
        
    else:
        print(f"PT file not found. There is an anomaly in the supposedely PT folder, a", traits["Modality"]," file. Please rename it or delete it.")

    
    nib.save(suv_img, savePath)
    os.remove('temp.nii')
    return savePath