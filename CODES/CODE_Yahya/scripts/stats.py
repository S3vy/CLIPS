import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import csv

"""
analyse= chemin du dossier analyse

Principe d'extraction:
pour extraires les données des fichiers metriques.txt, on fait tourner une boucle for sur tous les patients,
pour chaque patient on divise le fichier en une liste de ses lignes, et chaque ligne en une liste de ses mots(un mot est chaque ensemble de caractère non séparés par un espace ou un retour de ligne.), 
et chaque métrique en particulier à des "coordonnées" fixe dans ce fichier. Exemple pour le maxsuv:

maxsuv[patient] = content.split('\n')[6].split(' ')[3]

la position du maxsuv est toujours 6ème ligne, 3ème mot (en comptant de 0)
"""


def csv_maxsuv(analyse):
    list_patients=os.listdir(analyse)
    maxsuv={}
    for patient in list_patients:
        if len(os.listdir(os.path.join(analyse,patient)))<4:
            continue
        csv_file='maxsuv.csv'
        
        with open(os.path.join(analyse,patient,"metriques.txt"),'r') as file :
            content=file.read()
            maxsuv[patient] = content.split('\n')[6].split(' ')[3]
        
    with open(csv_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        for patient in maxsuv:
            writer.writerow([patient, maxsuv[patient]])

def csv_meandistance(analyse):
    list_patients=os.listdir(analyse)
    meandistance={}
    for patient in list_patients:
        if len(os.listdir(os.path.join(analyse,patient)))<4:
            continue
        csv_file='meandistance.csv'
        
        with open(os.path.join(analyse,patient,"metriques.txt"),'r') as file :
            content=file.read()
            meandistance[patient] = content.split('\n')[7].split(' ')[3]
        
    with open(csv_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        for patient in meandistance:
            writer.writerow([patient, meandistance[patient]])


def csv_hausdorff(analyse):
    list_patients=os.listdir(analyse)
    hausdorff={}
    for patient in list_patients:
        if len(os.listdir(os.path.join(analyse,patient)))<4:
            continue
        csv_file='hausdorff.csv'
        
        with open(os.path.join(analyse,patient,"metriques.txt"),'r') as file :
            content=file.read()
            hausdorff[patient] = content.split('\n')[8].split(' ')[4]
        
    with open(csv_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        for patient in hausdorff:
            writer.writerow([patient, hausdorff[patient]])

def csv_dice(analyse):
    list_patients=os.listdir(analyse)
    dice={}
    for patient in list_patients:
        if len(os.listdir(os.path.join(analyse,patient)))<4:
            continue
        csv_file='dice.csv'
        
        with open(os.path.join(analyse,patient,"metriques.txt"),'r') as file :
            content=file.read()
            dice[patient] = content.split('\n')[9].split(' ')[2]
        
    with open(csv_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        for patient in dice:
            writer.writerow([patient, dice[patient]])

def csv_nsd(analyse):
    list_patients=os.listdir(analyse)
    nsd={}
    for patient in list_patients:
        if len(os.listdir(os.path.join(analyse,patient)))<4:
            continue
        csv_file='nsd.csv'
        
        with open(os.path.join(analyse,patient,"metriques.txt"),'r') as file :
            content=file.read()
            nsd[patient] = content.split('\n')[10].split(' ')[4]
        
    with open(csv_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        for patient in nsd:
            writer.writerow([patient, nsd[patient]])

def csv_bji(analyse):
    list_patients=os.listdir(analyse)
    bji={}
    for patient in list_patients:
        if len(os.listdir(os.path.join(analyse,patient)))<4:
            continue
        csv_file='bji.csv'
        
        with open(os.path.join(analyse,patient,"metriques.txt"),'r') as file :
            content=file.read()
            bji[patient] = content.split('\n')[11].split(' ')[4]
        
    with open(csv_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        for patient in bji:
            writer.writerow([patient, bji[patient]])

def csv_tmtvnet_unthresholded(analyse):
    list_patients=os.listdir(analyse)
    tmtvnet_unthresholded={}
    for patient in list_patients:
        if len(os.listdir(os.path.join(analyse,patient)))<4:
            continue
        csv_file='tmtvnet_unthresholded.csv'
        
        with open(os.path.join(analyse,patient,"metriques.txt"),'r') as file :
            content=file.read()
            tmtvnet_unthresholded[patient] = content.split('\n')[13].split(' ')[6]
        
    with open(csv_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        for patient in tmtvnet_unthresholded:
            writer.writerow([patient, tmtvnet_unthresholded[patient]])

def csv_tmtvnet_thresholded(analyse):
    list_patients=os.listdir(analyse)
    tmtvnet_thresholded={}
    for patient in list_patients:
        if len(os.listdir(os.path.join(analyse,patient)))<4:
            continue
        csv_file='tmtvnet_thresholded.csv'
        
        with open(os.path.join(analyse,patient,"metriques.txt"),'r') as file :
            content=file.read()
            tmtvnet_thresholded[patient] = content.split('\n')[14].split(' ')[5]
        
    with open(csv_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        for patient in tmtvnet_thresholded:
            writer.writerow([patient, tmtvnet_thresholded[patient]])

def csv_realtmtv_thresholded(analyse):
    list_patients=os.listdir(analyse)
    realtmtv_thresholded={}
    for patient in list_patients:
        if len(os.listdir(os.path.join(analyse,patient)))<4:
            continue
        csv_file='realtmtv_thresholded.csv'
        
        with open(os.path.join(analyse,patient,"metriques.txt"),'r') as file :
            content=file.read()
            realtmtv_thresholded[patient] = content.split('\n')[15].split(' ')[5]
        
    with open(csv_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        for patient in realtmtv_thresholded:
            writer.writerow([patient, realtmtv_thresholded[patient]])

def csv_tmtvprecision(analyse):
    list_patients=os.listdir(analyse)
    tmtvprecision={}
    for patient in list_patients:
        if len(os.listdir(os.path.join(analyse,patient)))<4:
            continue
        csv_file='tmtvprecision.csv'
        
        with open(os.path.join(analyse,patient,"metriques.txt"),'r') as file :
            content=file.read()
            tmtvprecision[patient] = content.split('\n')[21].split(' ')[2]
        
    with open(csv_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        for patient in tmtvprecision:
            writer.writerow([patient, tmtvprecision[patient]])

def csv_tmtvrecall(analyse):
    list_patients=os.listdir(analyse)
    tmtvrecall={}
    for patient in list_patients:
        if len(os.listdir(os.path.join(analyse,patient)))<4:
            continue
        csv_file='tmtvrecall.csv'
        
        with open(os.path.join(analyse,patient,"metriques.txt"),'r') as file :
            content=file.read()
            tmtvrecall[patient] = content.split('\n')[22].split(' ')[2]
        
    with open(csv_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        for patient in tmtvrecall:
            writer.writerow([patient, tmtvrecall[patient]])

def csv_lesionwise(analyse): #pour identifier les segmentations vérifiant certains critères
    list_patients=os.listdir(analyse)
    lesionwise_recall={}
    lesionwise_precision={}
    for patient in list_patients:
        if len(os.listdir(os.path.join(analyse,patient)))<4:
            continue
        csv_file1='lesionwiseRecall.csv'
        csv_file2='lesionwisePrecision.csv'
        
        with open(os.path.join(analyse,patient,"metriques.txt"),'r') as file :
            content=file.read()
            nb_tp=eval(content.split('\n')[30].split(' ')[5])
            nb_fn=eval(content.split('\n')[31].split(' ')[5])
            nb_lesions=eval(content.split('\n')[30].split(' ')[7])
            nb_fp=eval(content.split('\n')[32].split(' ')[5])
            nb_predictions=content.split('\n')[32].split(' ')[7]
            
            if (nb_predictions).lower()=='nan': #prediction mask is void
                lesionwise_recall[patient] = 0
                lesionwise_precision[patient] = 0
            else:
                lesionwise_recall[patient] = nb_tp/nb_lesions
                lesionwise_precision[patient] = (eval(nb_predictions)-nb_fp)/eval(nb_predictions)
        
    with open(csv_file1, mode='w', newline='') as f:
        writer = csv.writer(f)
        for patient in lesionwise_recall:
            writer.writerow([patient, lesionwise_recall[patient]])
    with open(csv_file2, mode='w', newline='') as f:
        writer = csv.writer(f)
        for patient in lesionwise_precision:
            writer.writerow([patient, lesionwise_precision[patient]])


def ae_are(analyse):
    """
    ae = Absolute Error
    are = Average relative error
    """
    adiff=[] #liste des differences absolues
    rdiff=[] #liste des differences divisées par tmtv_reel

    list_patients=os.listdir(analyse)

    count=0
    for patient in list_patients:
        if len(os.listdir(os.path.join(analyse,patient)))<4:
            continue
        with open(os.path.join(analyse,patient,"metriques.txt"),'r') as file :
            content=file.read()
            tmtv_reel=eval(content.split('\n')[15].split(' ')[5])
            tmtv_net=eval(content.split('\n')[14].split(' ')[5])
            adiffv= abs(tmtv_reel-tmtv_net)
            rdiffv= abs(tmtv_reel-tmtv_net)/tmtv_reel
            adiff.append(adiffv)
            rdiff.append(rdiffv)
    return adiff,rdiff

def csv_ae_are(analyse):
    list_patients=os.listdir(analyse)
    ae={}
    are={}
    for patient in list_patients:
        if len(os.listdir(os.path.join(analyse,patient)))<4:
            continue
        csv_file1='absoluteError.csv'
        csv_file2='AverageRelativeError.csv'
        
        with open(os.path.join(analyse,patient,"metriques.txt"),'r') as file :
            content=file.read()
            tmtv_reel=eval(content.split('\n')[15].split(' ')[5])
            tmtv_net=eval(content.split('\n')[14].split(' ')[5])
            ae[patient] = abs(tmtv_reel-tmtv_net)
            are[patient] = abs(tmtv_reel-tmtv_net)/tmtv_reel
        
    with open(csv_file1, mode='w', newline='') as f:
        writer = csv.writer(f)
        for patient in ae:
            writer.writerow([patient, ae[patient]])
    with open(csv_file2, mode='w', newline='') as f:
        writer = csv.writer(f)
        for patient in are:
            writer.writerow([patient, are[patient]])

def stat(analyse):
    tmtv_precision_list=[]
    lesionwise_precision=[]
    tmtv_recall_list=[]
    lesionwise_recall=[]
    dice_list=[]
    hausdorff_list=[]
    nsd_list=[]
    no_predictions=[]

    list_patients=os.listdir(analyse)

    count=0
    for patient in list_patients:
        if len(os.listdir(os.path.join(analyse,patient)))<4:
            continue
        with open(os.path.join(analyse,patient,"metriques.txt"),'r') as file :
            content=file.read()
            nb_tp=eval(content.split('\n')[25].split(' ')[5])
            nb_fn=eval(content.split('\n')[26].split(' ')[5])
            if (nb_predictions).lower()=='nan': #prediction mask is void
                no_predictions.append(patient)
                continue

            if (tmtv_precision).lower()=='nan': #precision is actually equal to 0
                no_predictions.append(patient)
                continue
            count+=1
            lesionwise_recall.append(nb_tp/nb_lesions)
            lesionwise_precision.append((eval(nb_predictions)-nb_fp)/eval(nb_predictions))
            #(nb_lesions-nb_fp) and not nb_tp because nb_tp represents the number of successfully detected lesions, which might be different from the number of true predictions

            tmtv_recall_list.append(eval(tmtv_recall))
            tmtv_precision_list.append(eval(tmtv_precision))

            dice_list.append(dice)
            hausdorff_list.append(hausdorff)
            nsd_list.append(nsd)

    return {'lesionwise_recall':np.array(lesionwise_recall),'lesionwise_precision':np.array(lesionwise_precision),'tmtv_recall_list':np.array(tmtv_recall_list),'tmtv_precision_list':np.array(tmtv_precision_list),'dice':np.array(dice_list,dtype=float),'hausdorff':np.array(hausdorff_list,dtype=float),'nsd':np.array(nsd_list,dtype=float),'nombre patients':count,'nopred':no_predictions}
            
def correlation_tmtv(analyse):
    list1 = []
    list2 = []
    list_patients=os.listdir(analyse)
    for patient in list_patients:
        print(patient)
        if len(os.listdir(os.path.join(analyse,patient)))<4:
            continue
        with open(os.path.join(analyse,patient,"metriques.txt"),'r') as file :
            content=file.read()
            print(content.split('\n')[15])
            tmtv_reel=eval(content.split('\n')[15].split(' ')[5])
            tmtv_net=eval(content.split('\n')[14].split(' ')[5])
            if tmtv_net>0:
                list1.append(tmtv_reel)
                list2.append(tmtv_net)
            
    correlation = np.corrcoef(list1, list2)[0, 1]

    plt.figure(figsize=(8, 6))
    sns.regplot(x=list1, y=list2, ci=None)
    plt.title(f'Scatter Plot with Correlation: {correlation:.2f}')
    plt.xlabel('GT TMTV (ml)')
    plt.ylabel('TMTV-Net(ml)')
    plt.grid(True)

    plt.show()

def mean_dice(analyse):
    mean=0
    list_patients=os.listdir(analyse)
    for patient in list_patients:
        with open(os.path.join(analyse,patient,"metriques.txt"),'r') as file :
            content=file.read()  
        dice=eval(content.split('\n')[9].split()[2])
        mean+=dice
    mean/=len(list_patients)
    return mean

def mean_dice_no_zero(analyse): #moyenne dice sans patients à masque nul
    mean=0
    count=0
    list_patients=os.listdir(analyse)
    for patient in list_patients:
        with open(os.path.join(analyse,patient,"metriques.txt"),'r') as file :
            content=file.read()  
        dice=eval(content.split('\n')[9].split()[2])
        if dice>0.0:
            count+=1
            mean+=dice
    mean/=count
    return mean

def std_dice(analyse):
    dice_list=[]
    list_patients=os.listdir(analyse)
    for patient in list_patients:
        with open(os.path.join(analyse,patient,"metriques.txt"),'r') as file :
            content=file.read()  
            dice_list.append(eval(content.split('\n')[9].split()[2]))
    return np.std(np.array(dice_list))

def std_dice_no_zero(analyse):
    dice_list=[]
    list_patients=os.listdir(analyse)
    for patient in list_patients:
        with open(os.path.join(analyse,patient,"metriques.txt"),'r') as file :
            content=file.read()  
            if eval(content.split('\n')[9].split()[2])>0.0:   
                dice_list.append(eval(content.split('\n')[9].split()[2]))
    return np.std(np.array(dice_list))



def flag_badsegs(analyse): #pour identifier les segmentations vérifiant certains critères

    list_patients=os.listdir(analyse)

    flags=[]
    for patient in list_patients:
        if len(os.listdir(os.path.join(analyse,patient)))<4:
            continue
        with open(os.path.join(analyse,patient,"metriques.txt"),'r') as file :
            content=file.read()
            nb_tp=eval(content.split('\n')[30].split(' ')[5])
            nb_fn=eval(content.split('\n')[31].split(' ')[5])
            nb_lesions=eval(content.split('\n')[30].split(' ')[7])

            nb_fp=eval(content.split('\n')[32].split(' ')[5])
            nb_predictions=content.split('\n')[32].split(' ')[7]

        
            if (nb_predictions).lower()=='nan': #prediction mask is void
                flags.append(patient)
                continue

            percentage_tp= nb_tp/nb_lesions
            percentage_fn= nb_fn/nb_lesions
            percentage_fp=nb_fp/eval(nb_predictions)

            if percentage_tp<0.75 or percentage_fn>0.5 or percentage_fp>0.5 :
                flags.append(patient)

    return flags