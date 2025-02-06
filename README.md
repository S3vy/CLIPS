---
title: Projet CLIPS
author: FALK Anthonin & HAMIE Bachar
date: 20/11/2024
---
# Description
Ce projet a pour but d'améliorer la segmentation des images PET à l'aide du curriculum learning.


# Construction du Docker ou de l'environnement conda
## Docker
docker build -t tmtv-net-inference .
## Micromamba et pip
```
micromamba create --name <nom_envionnement>
sudo apt install python3-pip
```
Se placer à l'endroit où se trouve le fichier "requirement.txt" et executer
```
pip install -r requirements.txt
```

# Lancement de l'inférence

## Pour un seul patient
### Avec Docker
```
docker run -it -v /home/antho/CLIPS/DONNEES/11011101221002:/input -v /home/antho/CLIPS/DONNEES/Sortie_algo:/output tmtv-net-inference
```

### Sans Docker
Se placer dans le dossier où se trouve le fichier main.py (pour nous : home/clips/Projet_CLIPS_DATASIM_2025/CLIPS/CODES/CODE_qurit-frizi/main/) puis exécuter :

```
python <path/to/python/file>/main.py -it -v <path/to/patient/data/>11011101221002:/input -v <path/to/output>:/output tmtv-net-inference
```
Pour la configuration du PC au CHU :
```
python /home/clips/Projet_CLIPS_DATASIM_2025/CLIPS/CODES/CODE_qurit-frizi/main/main.py -it -v /home/antho/CLIPS/DONNEES/dicom/11011101221002:/input -v /home/clips/Projet_CLIPS_DATASIM_2025/CLIPS/DONNEES/pred_masks:/output tmtv-net-inference
```
Pour la configuration de mon PC personnel :
```
python main.py -it -v /home/antho/CLIPS/DONNEES/dicom/11011101221002:/input -v /home/clips/Projet_CLIPS_DATASIM_2025/CLIPS/DONNEES/pred_masks:/output tmtv-net-inference
```

## Pour plusieurs fichiers
### Version de Yahya (avec docker)
for file in ./dicom/*; do sudo docker run -it --gpus all -v "$file":/input -v '/home/yahya/Documents/Stage TMTV-NET/data/pred_masks':/output tmtv-net-inference-no-sitk; done

### Version projet CLIPS (sans docker)
for file in /home/clips/Projet_CLIPS_DATASIM_2025/CLIPS/DONNEES/dicom/*; do python /home/clips/Projet_CLIPS_DATASIM_2025/CLIPS/CODES/CODE_qurit-frizi/main/main.py -it --gpus all -v "$file":/input -v '/home/clips/Projet_CLIPS_DATASIM_2025/CLIPS/DONNEES/pred_masks':/output 11011101021001; done

# Activation environnement
source /home/clips/Projet_CLIPS_DATASIM_2025/CLIPS_env/bin/activate

