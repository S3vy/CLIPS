import cc3d
import numpy as np
from metrics import*




"""
Contains functions that count the number of TP, FN, and FP Lesions using NSD or DICE, using approach 1 or approach 2 :
Approach 1 (not used in the final assessment) : the "strict" approach each GT lesion is compared with each predicted lesion individually.
Approach 2 (used in the final assessment) : the "global" approach each GT lesion is compared with all the predicted lesions it intersects with, and each predicted lesion is compared with all the GT lesions it intersects with.
"""


def connected_comps(gt_array,seg_array):
    """
    The function takes as arguments : the thresholded tmtv-net prediction file and the thresholded gt file.
    the function outputs : one labeled array for each file and two dictionnaries linking the two : 
    a dictionnary where for each gt connected component, all the pred connected components that 
    have an intersection with it are listed, and a dictionnary where the same  is done for each pred 
    connected component.
    """

    gt_to_pred={}

    for a,b in zip(gt_array.reshape(-1),seg_array.reshape(-1)) :
        if a!=0:
            if a not in gt_to_pred:
                gt_to_pred[a]=[]
            if b!=0 :
                if a in gt_to_pred and b not in gt_to_pred[a] : 
                    gt_to_pred[a].append(b)

    pred_to_gt={}

    for a,b in zip(seg_array.reshape(-1),gt_array.reshape(-1)) :
        if a!=0:
            if a not in pred_to_gt:
                pred_to_gt[a]=[]
            if b!=0 :
                if a in pred_to_gt and b not in pred_to_gt[a] : 
                    pred_to_gt[a].append(b)
                
    return gt_array,seg_array,gt_to_pred,pred_to_gt




def lesionwise_nsd(gt_label,seg_label,gt_to_pred,pred_to_gt, spacing_mm, tolerance_mm):
    """
    This function takes are arguments : gt_label,seg_label et gt_to_pred
    The function outputs : 
    a dictionnary associating each gt tumour with a list of couples (pred tumour,nsd of the two)
    if a gt tumour has no prediction at all it is associated with the couple (0,0)
    a dictionnary associating each pred tumour with a list of couples  (gt tumour , nsd of the two)
    if a prediction is associated with no tumour at all, it is associated with the couple (0,0)
    """
    gt_to_pred_nsd={}
    for gt in gt_to_pred :
        if len(gt_to_pred[gt])==0:
            gt_to_pred_nsd[gt]=[]
            gt_to_pred_nsd[gt].append((0,0))
            continue
        for pred in gt_to_pred[gt]:
            gt_mask=(gt_label==gt)
            pred_mask=(seg_label==pred)
            if gt not in gt_to_pred_nsd:
                gt_to_pred_nsd[gt]=[]
            gt_to_pred_nsd[gt].append((pred,nsd(gt_mask,pred_mask,spacing_mm,tolerance_mm)))
    
    pred_to_gt_nsd={}
    for pred in pred_to_gt :
        if len(pred_to_gt[pred])==0:
            pred_to_gt_nsd[pred]=[]
            pred_to_gt_nsd[pred].append((0,0))
            continue
        for gt in pred_to_gt[pred]:
            gt_mask=(gt_label==gt)
            pred_mask=(seg_label==pred)
            if pred not in pred_to_gt_nsd:
                pred_to_gt_nsd[pred]=[]
            pred_to_gt_nsd[pred].append((gt,nsd(gt_mask,pred_mask,spacing_mm,tolerance_mm)))
    
    return gt_to_pred_nsd, pred_to_gt_nsd

def lesionwise_dsc(gt_label,seg_label,gt_to_pred,pred_to_gt):
    """
    This function takes are arguments : gt_label,seg_label et gt_to_pred
    The function outputs : 
    a dictionnary associating each gt tumour with a list of couples (pred tumour, dice of the two) 
    a dictionnary associating each pred tumour with a list of couples  (gt tumour , dice of the two)
    """
    gt_to_pred_dsc={}
    for gt in gt_to_pred :
        if len(gt_to_pred[gt])==0:
            gt_to_pred_dsc[gt]=[]
            gt_to_pred_dsc[gt].append((0,0))
            continue
        for pred in gt_to_pred[gt]:
            gt_mask=(gt_label==gt)
            pred_mask=(seg_label==pred)
            if gt not in gt_to_pred_dsc:
                gt_to_pred_dsc[gt]=[]
            gt_to_pred_dsc[gt].append((pred,dsc(gt_mask,pred_mask)))
    
    pred_to_gt_dsc={}
    for pred in pred_to_gt :
        if len(pred_to_gt[pred])==0:
            pred_to_gt_dsc[pred]=[]
            pred_to_gt_dsc[pred].append((0,0))
            continue
        for gt in pred_to_gt[pred]:
            gt_mask=(gt_label==gt)
            pred_mask=(seg_label==pred)
            if pred not in pred_to_gt_dsc:
                pred_to_gt_dsc[pred]=[]
            pred_to_gt_dsc[pred].append((gt,dsc(gt_mask,pred_mask)))
    
    return gt_to_pred_dsc, pred_to_gt_dsc

def tp_strict_identifier(gt_to_pred_metric,threshold=0.5): #successfully detected lesions
    """
    returns dictionnary that maps each gt tumour to a list of preds that *individualy* verify score>=threshold ( if equal to 0.5, only one pred possible)
    if gt tumour has no valid pred, it is not listed.
    """
    tp={}
    for gt in gt_to_pred_metric:
        for couple in gt_to_pred_metric[gt]:
            if couple[1]>=threshold : 
                if gt not in tp :
                    tp[gt]=[]
                tp[gt].append(couple[0])
    return tp


def fn_strict_identifier(gt_to_pred_metric,threshold=0.5): #undetected lesions
    """
    returns dictionnary that maps each gt tumour to the list of its preds that *individualy* verify score<threshold
    """
    fn={}
    for gt in gt_to_pred_metric:
        count=0
        for couple in gt_to_pred_metric[gt]:
            if couple[1]>=threshold :
                break 
            count+=1
        if count==len(gt_to_pred_metric[gt]): #if all are unvalid predictions then it's a fn
            if gt not in fn :
                fn[gt]=[]
            for couple in gt_to_pred_metric[gt]:
                fn[gt].append(couple[0])
    
    return fn

def fp_strict_identifier(pred_to_gt_metric,threshold=0.5): #wrong predictions
    """
    returns dictionnary that maps each pred tumour to a list of gts inside it that *individualy* verify score<threshold
    """
    fp={}
    for pred in pred_to_gt_metric:
        for couple in pred_to_gt_metric[pred]:
            if couple[1]<threshold:
                if pred not in fp :
                    fp[pred]=[]
                fp[pred].append(couple[0])
    return fp

def tp_global_identifier_nsd(gt_label,seg_label,gt_to_pred_metric,spacing_mm,tolerance_mm,threshold=0.5):
    """
    returns a list of gt tumours whose preds *collectively* verify nsd>threshold  
    """
    tp=[]
    for gt in gt_to_pred_metric:
        gt_mask=(gt_label==gt)
        pred_mask=np.sum(np.array([seg_label==pred[0] for pred in gt_to_pred_metric[gt]]),0)>0#np.sum fait la réunion des masks

        if nsd(gt_mask,pred_mask,spacing_mm,tolerance_mm)>threshold:
            tp.append(gt)
    return tp

def tp_global_identifier_dsc(gt_label,seg_label,gt_to_pred_metric,threshold=0.5):
    """
    returns a list of gt tumours whose preds *collectively* verify nsd>threshold  
    """
    tp=[]
    for gt in gt_to_pred_metric:
        gt_mask=(gt_label==gt)
        pred_mask=np.sum(np.array([seg_label==pred[0] for pred in gt_to_pred_metric[gt]]),0)>0 #np.sum fait la réunion des masks

        if dsc(gt_mask,pred_mask)>threshold:
            tp.append(gt)
    return tp

def fn_global_identifier_nsd(gt_label,seg_label,gt_to_pred_metric,spacing_mm,tolerance_mm,threshold=0.5):
    """
    returns a list of gt tumours whose preds *collectively* verify nsd<threshold   
    """
    fn=[]
    for gt in gt_to_pred_metric:
        gt_mask=(gt_label==gt)
        pred_mask=np.sum(np.array([seg_label==pred[0] for pred in gt_to_pred_metric[gt]]),0)>0 #np.sum fait la réunion des masks

        if nsd(gt_mask,pred_mask,spacing_mm,tolerance_mm)<threshold:
            fn.append(gt)
    return fn

def fn_global_identifier_dsc(gt_label,seg_label,gt_to_pred_metric,threshold=0.5):
    """
    returns a list of gt tumours whose preds *collectively* verify dice<threshold  
    """
    fn=[]
    for gt in gt_to_pred_metric:
        gt_mask=(gt_label==gt)
        pred_mask=np.sum(np.array([seg_label==pred[0] for pred in gt_to_pred_metric[gt]]),0)>0 #np.sum fait la réunion des masks

        if dsc(gt_mask,pred_mask)<threshold:
            fn.append(gt)
    return fn

def fp_global_identifier_nsd(gt_label,seg_label,pred_to_gt_metric,spacing_mm,tolerance_mm,threshold=0.5):
    """
    returns a list of preds whose gt tumours *collectively* verify nsd<threshold 
    """
    fp=[]
    for pred in pred_to_gt_metric:
        pred_mask=(seg_label==pred)
        gt_mask=np.sum(np.array([gt_label==gt[0] for gt in pred_to_gt_metric[pred]]),0)>0 #np.sum fait la réunion des masks

        if nsd(gt_mask,pred_mask,spacing_mm,tolerance_mm)<threshold:
            fp.append(pred)
    return fp

def fp_global_identifier_dsc(gt_label,seg_label,pred_to_gt_metric,threshold=0.5):
    """
    returns a list of preds whose gt tumours *collectively* verify dsc<threshold
    """
    fp=[]
    for pred in pred_to_gt_metric:
        pred_mask=(seg_label==pred)
        gt_mask=np.sum(np.array([gt_label==gt[0] for gt in pred_to_gt_metric[pred]]),0)>0 #np.sum fait la réunion des masks

        if dsc(gt_mask,pred_mask)<threshold:
            fp.append(pred)
    return fp

