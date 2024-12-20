---
title: Notes sur la bibliographie
author: FALK Anthonin
date: 23/11/2024
---
# TMTV-Net

Article présentant le réseau TMTV-Net ayant pour but de segmenter les tumeurs des patients atteint de lymphomes.

## Données utilisées
1418 FDG PET/CT scans provenant de 4 centres différents. 900 utilisés pour la phase de développement/validation/test et 518 pour les test multicentres extérieurs. La première partie des données comprend 450 scans de lymphomes, cancer du poumon ou mélanomes et 450 scans négatifs. La deuxième partie des données comprend des patients atteints de lymphomes venant de plusieurs centres différents et atteints de DLBCL, de "primary mediastinal large B cell, and classic Hodgkin lymphoma cases".

## Le modèle
Le modèle utilise plusieurs resampling des images TEP/CT pour ensuite les utiliser comme entrainement et test dans des 3D U-Nets en utilisant une méthode de cross-validation à 5 folds.


-----------------------------------------------------------
-----------------------------------------------------------
## Définitions :


### Soft voting
Vote où le poids de chaque classifieur associé à la prédiction prise en compte dans le vote

### TTA (Test time augmentation) :
> "Test time augmentation (TTA) is a data augmentation strategy used during the testing phase. It involves applying various augmentations, such as flipping and scaling, to the same image and then merging the predictions of each augmented image to produce a more accurate prediction"

d'après https://mmengine.readthedocs.io/en/latest/advanced_tutorials/test_time_augmentation.html le 28/11/2024

### DSC (Dice Score)
> "the Dice score is equal to twice the size of the intersection divided by the sum of the sizes of the two sets. This means that the Dice score measures the proportion of overlap between the two sets, normalized by the size of the sets."

d'après https://oecd.ai/en/catalogue/metrics/dice-score le 28/11/2024

### Hodgkin VS non-Hodgkin lymphoma
> "Both Hodgkin's lymphoma and non-Hodgkin's lymphoma are types of lymphoma. Lymphoma is a type of cancer that begins in white blood cells called lymphocytes. Lymphocytes are an important part of the body's germ-fighting immune system.
> 
> The main difference between Hodgkin's lymphoma and non-Hodgkin's lymphoma is in the specific lymphocyte each involves.
> 
> The difference between Hodgkin's lymphoma and non-Hodgkin's lymphoma can be seen by looking at the cancer cells under a microscope. If a specific type of cell called a Reed-Sternberg cell is seen, the lymphoma is classified as Hodgkin's. If the Reed-Sternberg cell is not present, the lymphoma is classified as non-Hodgkin's.
> 
> Many subtypes of lymphoma exist. If you have lymphoma, lab tests will be used to examine a sample of your lymphoma cells to determine your specific subtype. Expect to wait a few days to get results from these specialized tests.
> 
> Your type of lymphoma helps to determine your prognosis and your treatment options. The types of lymphoma have very different disease courses and treatment choices. An accurate diagnosis is an essential part of getting the care you need. "

d'après https://www.mayoclinic.org/diseases-conditions/hodgkins-lymphoma/expert-answers/lymphoma/faq-20058546
le 28/11/2024