import dicom2nifti
import dicom2nifti.settings as settings
import nibabel as nib
import pydicom
import numpy as np
import os
from datetime import datetime
from dateutil import parser


def convert_dicom_to_nifti(dicom_folder):
    # Convert the DICOM folder to NIfTI
    settings. disable_validate_slice_increment() #ignore slice increment discrepancies 
    dicom2nifti.dicom_series_to_nifti(dicom_folder, "temp.nii", reorient_nifti=False)

def convert_bqml_to_suv(dicom_folder, output_file):
    """
    Trouve un dossier ou ya des PETs et le converti en suv nifti
    """
    folders = os.listdir(dicom_folder)
    fichiers = []
    # Parcourir récursivement les sous-dossiers
    for i in range(len(folders)):
        for root, dirs, files in os.walk(os.path.join(dicom_folder, folders[i])):
            for file in files:
                fichiers.append(os.path.join(root, file))
    #récuperer un PT au hasard
    file_metadata=""
    maybe_file_metadata=""
    maybe_correct_max=0
    numberOfCorrections=0
    for file in fichiers:
        if pydicom.filereader.dcmread(file).Modality == 'PT':
            if numberOfCorrections<len(pydicom.filereader.dcmread(file)[0x00280051].value):
                numberOfCorrections = len(pydicom.filereader.dcmread(file)[0x00280051].value) #prend le dossier pet avec le plus de corrections
                file_metadata=file
            elif numberOfCorrections==len(pydicom.filereader.dcmread(file)[0x00280051].value):
                maybe_file_metadata=file
                maybe_correct_max=numberOfCorrections
    pet1= (pydicom.filereader.dcmread(file_metadata).SeriesDescription if 'SeriesDescription' in pydicom.filereader.dcmread(file_metadata) else os.path.basename(os.path.dirname(file_metadata)))
    pet2=(pydicom.filereader.dcmread(maybe_file_metadata).SeriesDescription if 'SeriesDescription' in pydicom.filereader.dcmread(maybe_file_metadata) else os.path.basename(os.path.dirname(maybe_file_metadata)))
    if maybe_correct_max==numberOfCorrections and (pet1!=pet2 or os.path.basename(os.path.dirname(file_metadata))!=os.path.basename(os.path.dirname(maybe_file_metadata))):
        aa = input(f"Found two corrected PET folders : {pet1}({os.path.basename(os.path.dirname(file_metadata))}) and {pet2}({os.path.basename(os.path.dirname(maybe_file_metadata))}). Which one do you chose? (Enter 1 for 1st one or 2 for 2nd one. Enter anything else to exit.)")
        if aa == '2':
            file_metadata = maybe_file_metadata
        elif aa=='1':
            pass
        else:
            exit()
    if file_metadata=="":
        print("No PT file found. Cannot proceed.")
        return
    convert_dicom_to_nifti(os.path.dirname(file_metadata))
    dicom_metadata= pydicom.filereader.dcmread(file_metadata)
    img = nib.load('temp.nii')
    data = img.get_fdata()

    
    patient_weight = dicom_metadata[0x0010, 0x1030].value  # in kg
    injected_dose = dicom_metadata[0x054, 0x0016][0][0x0018, 0x1074].value  # Total injected dose (Bq)
    half_life = float(dicom_metadata[0x054, 0x0016][0][0x0018, 0x1075].value)  # Radionuclide half life (s)
    
    parse = lambda x: parser.parse(x)

    series_time = str(dicom_metadata[0x0008, 0x00031].value)  # Series start time (hh:mm:ss)
    series_date = str(dicom_metadata[0x0008, 0x00021].value)  # Series start date (yyy:mm:dd)
    series_datetime_str = series_date + ' ' + series_time
    series_dt = parse(series_datetime_str)

    injection_time = str(dicom_metadata[0x054, 0x0016][0][0x0018, 0x1072].value)  # Radionuclide time of injection (hh:mm:ss)
    nuclide_datetime_str = series_date + ' ' + injection_time
    nuclide_dt = parse(nuclide_datetime_str)
    # Convert times to seconds
    decay_time = (series_dt - nuclide_dt).total_seconds()
    decay_factor = np.exp(-decay_time * np.log(2) / half_life)

    # Calculate SUV
    manufacturer = dicom_metadata[0x00080070].value.lower()

    units = dicom_metadata[0x00541001].value.lower()
    unitIsNotBqml = "bqml" not in units
    

    if "philips" in manufacturer and unitIsNotBqml:
        suv_data = data * float(dicom_metadata[0x70531000].value)
        print("suv_factor=",float(dicom_metadata[0x70531000].value))
    else:
        suv_data = data * patient_weight *1000/ (injected_dose * decay_factor)
        print("suv_factor=",patient_weight *1000/ (injected_dose * decay_factor))

    suv_img = nib.Nifti1Image(suv_data, img.affine, img.header)
    nib.save(suv_img, output_file)
    print(f"Conversion complete. Saved as {output_file}")
    os.remove('temp.nii')