from metrics import*
from thresholder import *
from DicomNiftiConversion import*
import os 
from cc3dd import*
import ast

"""
The loaded folder has to have these three subfolders : gt_masks, pred_masks,dicom
pred_masks is the folder that contains unmodified TMTV-Net segmentations, 
dicom contains patient folders (pet/ct)
gt_masks have to have a subfolder pet0 that contains the grount truth segmentation(s)
segmentation containing suv3.0 in their name are priority

Returns:

a 'analyse' folder with subfolders in the patients' names, each one containing 4 files:
dicom_suv.nii
gt_mask4thresholded.nii
pred_mask4thresholded.nii
metrics.txt containing metrics between the ground truth and the tmtv_thresholded prediction.

"""
def find_gt_name(patient_gt_path):
    files = []
    for root, dirs, file_names in os.walk(os.path.join(patient_gt_path,'pet0')):
        for file_name in file_names:
            files.append(os.path.join(root, file_name))
    niifile=""
    for file in files:
        if file.endswith('.nii'):
            niifile=file
            if 'suv3.0' in file:
                return file
    if niifile=="":
        print(patient_gt_path,"does not exist or does not contain any ground truth .nii file.")
        return 0
    return niifile   


def assessSegmentation(gt_nii_path,tmtv_seg_path,patient_dicom,tolerance_mm,suv_threshold=4,percentile_hausdorff=95): 
    a=gt_nii_path
    b=tmtv_seg_path
    pet=list_of_modality_dirs(patient_dicom)['PT']
    dicom=os.path.dirname(pet)
    numero_patient=os.path.basename(dicom)
    folder=os.path.dirname(os.path.dirname((dicom)))
    os.makedirs(os.path.join(folder,"analyse",numero_patient),exist_ok=True)

    print(f'Conversion du dossier {pet} en nifti suv...')
    
    print(dicomToNifti(pet, os.path.join(folder,"analyse",numero_patient,f'{numero_patient}suv.nii.gz')))
    max_suv=np.max(nib.load(os.path.join(folder,"analyse",numero_patient,f'{numero_patient}suv.nii.gz')).get_fdata())
    print(f'Seuillage du fichier {a}...') 
    generate_thresholded_file(os.path.join(folder,"analyse",numero_patient,f'{numero_patient}suv.nii.gz'),a,os.path.join(folder,"analyse",numero_patient,f'{numero_patient}_{suv_threshold}thresholded_GT.nii.gz'),a,suv_threshold)
    print(f'Seuillage du fichier {b}...')
    generate_thresholded_file(os.path.join(folder,"analyse",numero_patient,f'{numero_patient}suv.nii.gz'),b,os.path.join(folder,"analyse",numero_patient,f'{numero_patient}_{suv_threshold}thresholded_SEG.nii.gz'),a,suv_threshold)

    data=load_fdata(os.path.join(folder,"analyse",numero_patient,f'{numero_patient}_{suv_threshold}thresholded_GT.nii.gz'),os.path.join(folder,"analyse",numero_patient,f'{numero_patient}_{suv_threshold}thresholded_SEG.nii.gz'))
    ground_truth=os.path.join(folder,'gt_masks',numero_patient,'pet0',find_gt_name(os.path.join(folder,'gt_masks',numero_patient)))

    avg_distance=round(average_distance(*data)[0],3)
    hausd_distance=round(hausdorff(*data,percentile_hausdorff),3)
    dice=round(dsc(*data[:2]),3)
    nsd1=round(nsd(*data,tolerance_mm),3)
    bji1=round(bji(*data,tolerance_mm),3)

    lesionwise_threshold=0.5

    data_lesions= connected_comps(data[0],data[1])
    
    lesionwise_metric=lesionwise_dsc(data_lesions[0],data_lesions[1],data_lesions[2],data_lesions[3])#,data[2], tolerance_mm) #replace nsd with dsc for dice

    nb_lesions=len(data_lesions[2])
    nb_predictions = len(data_lesions[3])

    if not nb_lesions : 
        nb_lesions = float('Nan')
    if not nb_predictions:
        nb_predictions = float('Nan')

    nb_tp_strict=len(tp_strict_identifier(lesionwise_metric[0],threshold=lesionwise_threshold))
    nb_fn_strict=len(fn_strict_identifier(lesionwise_metric[0],threshold=lesionwise_threshold))
    nb_fp_strict=len(fp_strict_identifier(lesionwise_metric[1],threshold=lesionwise_threshold))

    nb_tp_global=len(tp_global_identifier_dsc(data_lesions[0],data_lesions[1],lesionwise_metric[0]))#,data[2], tolerance_mm,threshold=lesionwise_threshold))#replace nsd with dsc for dice
    nb_fn_global=len(fn_global_identifier_dsc(data_lesions[0],data_lesions[1],lesionwise_metric[0]))#,data[2], tolerance_mm,threshold=lesionwise_threshold))#replace nsd with dsc for dice
    nb_fp_global=len(fp_global_identifier_dsc(data_lesions[0],data_lesions[1],lesionwise_metric[1]))#,data[2], tolerance_mm,threshold=lesionwise_threshold))#replace nsd with dsc for dice
    
    print("Max SUV = ",max_suv)
    print("Distance moyenne : ", avg_distance,"mm")
    print("Distance de Hausdorff : ",hausd_distance,"mm") #ajuster le percentile pour négliger les aberrances
    print("Dice : ",dice)
    print(f"NSD à {tolerance_mm}mm : ",nsd1)#20mm de marge 
    print(f"BJI à {tolerance_mm}mm : ",bji1)
    print("TMTV calculé par TMTV-NET (non seuillé):", tmtv(b),'ml')
    print("TMTV calculé par TMTV-NET (seuillé):",tmtv(os.path.join(folder,"analyse",numero_patient,f'{numero_patient}_{suv_threshold}thresholded_SEG.nii.gz')),'ml')
    print("TMTV réel (seuillé à 4):",tmtv(os.path.join(folder,"analyse",numero_patient,f'{numero_patient}_{suv_threshold}thresholded_GT.nii.gz')),'ml')
    print("Volume faussement segmenté (TMTV-NET seuillé) : ",faux_positifs(os.path.join(folder,"analyse",numero_patient,f'{numero_patient}_{suv_threshold}thresholded_SEG.nii.gz'),os.path.join(folder,"analyse",numero_patient,f'{numero_patient}_{suv_threshold}thresholded_GT.nii.gz')),'ml')
    print("Volume faussement segmenté (TMTV-NET non seuillé) : ", faux_positifs(b,os.path.join(folder,"analyse",numero_patient,f'{numero_patient}_{suv_threshold}thresholded_GT.nii.gz')),'ml')
    print("Volume Tumoral non segmenté : ",faux_negatifs(os.path.join(folder,"analyse",numero_patient,f'{numero_patient}_{suv_threshold}thresholded_SEG.nii.gz'),os.path.join(folder,"analyse",numero_patient,f'{numero_patient}_{suv_threshold}thresholded_GT.nii.gz')),'ml')
    print("Volume Tumoral segmenté : ",vrai_positifs(os.path.join(folder,"analyse",numero_patient,f'{numero_patient}_{suv_threshold}thresholded_SEG.nii.gz'),os.path.join(folder,"analyse",numero_patient,f'{numero_patient}_{suv_threshold}thresholded_GT.nii.gz')),'ml')
    
    tp_tmtv=vrai_positifs(os.path.join(folder,"analyse",numero_patient,f'{numero_patient}_{suv_threshold}thresholded_SEG.nii.gz'),os.path.join(folder,"analyse",numero_patient,f'{numero_patient}_{suv_threshold}thresholded_GT.nii.gz'))
    fn_tmtv=faux_negatifs(os.path.join(folder,"analyse",numero_patient,f'{numero_patient}_{suv_threshold}thresholded_SEG.nii.gz'),os.path.join(folder,"analyse",numero_patient,f'{numero_patient}_{suv_threshold}thresholded_GT.nii.gz'))
    fp_tmtv=faux_positifs(os.path.join(folder,"analyse",numero_patient,f'{numero_patient}_{suv_threshold}thresholded_SEG.nii.gz'),os.path.join(folder,"analyse",numero_patient,f'{numero_patient}_{suv_threshold}thresholded_GT.nii.gz'))
    
    precision = round(tp_tmtv/(tp_tmtv+fp_tmtv),4)
    recall=round(tp_tmtv/(tp_tmtv+fn_tmtv),4)

    if precision == float('nan'):
        precision=0

    file_content=f"""

Patient : {numero_patient}
Tolerance : {tolerance_mm}
Lesionwise threshold : {100*lesionwise_threshold}%

Max SUV = {max_suv}
Distance moyenne : {avg_distance} mm
Distance de Hausdorff : {hausd_distance} mm
Dice : {dice}
NSD à {tolerance_mm}mm : {nsd1}
BJI à {tolerance_mm}mm : {bji1}

TMTV calculé par TMTV-NET (non seuillé): { tmtv(b)}ml
TMTV calculé par TMTV-NET (seuillé): {tmtv(os.path.join(folder,"analyse",numero_patient,f'{numero_patient}_{suv_threshold}thresholded_SEG.nii.gz'))} ml
TMTV réel (seuillé à 4): {tmtv(os.path.join(folder,"analyse",numero_patient,f'{numero_patient}_{suv_threshold}thresholded_GT.nii.gz'))} ml 

TMTV FP non seuillé :{faux_positifs(b,os.path.join(folder,"analyse",numero_patient,f'{numero_patient}_{suv_threshold}thresholded_GT.nii.gz'))} ml
TMTV FP seuillé : {fp_tmtv} ml
TMTV FN : {fn_tmtv} ml   
TMTV TP : {tp_tmtv} ml
Précision : {100*precision } %
Recall : {100*recall} %

Approach 1 :
Nombre de lésions TP : {nb_tp_strict} / {nb_lesions} ({round(100*nb_tp_strict/nb_lesions,2)}%)
Nombre de lésions FN : {nb_fn_strict} / {nb_lesions} ({round(100*nb_fn_strict/nb_lesions,2)}%)
Nombre de prédictions FP : {nb_fp_strict} / {nb_predictions} ({round(100*nb_fp_strict/nb_predictions,2)}%)

Approach 2 :
Nombre de lésions TP : {nb_tp_global} / {nb_lesions} ({round(100*nb_tp_global/nb_lesions,2)}%)
Nombre de lésions FN : {nb_fn_global} / {nb_lesions} ({round(100*nb_fn_global/nb_lesions,2)}%)
Nombre de prédictions FP : {nb_fp_global} / {nb_predictions} ({round(100*nb_fp_global/nb_predictions,2)}%)
    """
    file_path=os.path.join(folder,"analyse",numero_patient,"metriques.txt")
    with open(file_path, 'w') as file:
        file.write(file_content)


def assessAll(data_base_folder,tolerance_mm,percentile_hausdorff=95,suv_threshold=4,patients_list=0):
    listdirs=os.listdir(data_base_folder)
    if 'gt_masks' not in listdirs:
        print('There is no ground truth folder named "gt_masks", pleasdef find_gt_name(patient):')

    elif 'pred_masks' not in listdirs:
        print('There is no segmentation folder named "pred_masks", please include one by this name or rename your segmentation folder.')
        return
    elif 'dicom' not in listdirs:
        print('There is no dicom folder named "dicom", pgt_listdirslease include one by this name or rename your dicom folder.')
        return
    else:
        print("Found pred_masks, gt_masks and dicom")
    
    gdt_path=os.path.join(data_base_folder,'gt_masks')
    pred_path=os.path.join(data_base_folder,'pred_masks')
    dicom_path=os.path.join(data_base_folder,'dicom')
    analyse_path=os.path.join(data_base_folder,'analyse')

    gt_listdirs=os.listdir(gdt_path)
    pred_listdirs=os.listdir(pred_path)
    dicom_listdirs=os.listdir(dicom_path)
    analyse_listdirs=os.listdir(analyse_path)

    if patients_list ==0:
        list_patients=[patients for patients in gt_listdirs]
        list_of_interest=[patients for patients in list_patients if patients not in analyse_listdirs]
    else :
        file = open(patients_list)
        list_of_interest= [patients for patients in ast.literal_eval(file.read()) if patients not in analyse_listdirs]

    for patient in list_of_interest:
        print(os.path.join(gdt_path,patient))
        gt_patient_path=os.path.join(gdt_path,patient,'pet0',find_gt_name(os.path.join(gdt_path,patient)))
        tmtv_seg_path=os.path.join(pred_path,patient+"_SEG.nii.gz")
        patient_dicom=os.path.join(dicom_path,patient)
        assessSegmentation(gt_patient_path,tmtv_seg_path,patient_dicom,tolerance_mm,suv_threshold=4,percentile_hausdorff=100)