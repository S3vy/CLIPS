---
title: Projet CLIPS
author: FALK Anthonin & HAMIE Bachar
date: 20/11/2024
---
# Description
Ce projet a pour but d'améliorer la segmentation des images PET à l'aide du curriculum learning.

# Structure de ce dépôt
- **CODES** : Ces sont les fichiers qui correspondent au code de TMTV-Net
    - **CODE_qurit-frizi** : Le code original de TMTV-Net (disponible à l'adresse https://github.com/qurit-frizi/TMTV-Net). Nous y avons cependant ajouté quelques fichiers, notamment *main_modif.py* dans le dossier <code>main/</code>. Comme son nom l'indique, c'est une version modifiée de *modif.py* qui est le fichier original. La seule grosse modification que ce fichier a reçu est celle qui permet de l'éxécuter directement avec python, sans passer par Docker.

    - **CODE_Yahya** : Le code utilisé par Yayha (stagiaire ayant travaillé pendant 5 mois sur le projet). Nous n'avons noté aucune différence avec le code originale mais il est possible qu'il y en ait et que nous nous en somme pas aperçu. Nous avons donc préféré le garder dans le doute.

- **DOCUMENTATION** : 
    - **ARTICLES** : Les articles que nous avons lu en lien avec le sujet. Parmis ces articles se trouve celui de la publication originale de TMTV-Net et les autres traitent du sujet du Curriculum Lerning.

    - **DOCS_Yahya** :

    - **NOTES_SUR_LES_ARTICLES** :

- **DONNEES** :
    - **dicom** :
    - **pred_masks** :
    - **metriques.txt** :

- **INFORMATION_PROBLEMES_SEGMENTATION**

- **REUNIONS**


# Construction du Docker ou de l'environnement conda
## Docker
Création de l'envionnement : se placer dans le folder <code>main/</code> puis exécuter :

```bash
docker build -t tmtv-net-inference .
```

## venv
Création de l'environnment : se placer en dehors de tout fichier de code (dans un nouveau dossier facile à retrouver de préférence) puis exécutez :

```bash
python -m venv C:/path/to/new/virtual/environment
```

où <code>C:/path/to/new/virtual/environment</code> peut être remplacé par <code>.</code> si vous êtes déjà à l'endroit souhaité.

Activation de l'environnement (dans notre cas):

```bash
source /home/clips/Projet_CLIPS_DATASIM_2025/CLIPS_env/bin/activate
```

Après avoir activé l'environnement pour la première fois, il vous faudra installer les librairies nécessaires. Pour cela, naviguez jusqu'au dossier <code>main/</code> puis éxécuter :

```bash
sudo apt-get install python3-pip

pip install -r requirements.txt
```

## Attention
Pour le PC au CHU, un environnement micromamba, miniconda ou conda est incompatible avec le programme (j'ai vraiment essayé de toutes mes forces)

# Avant le lancement de l'inférence
Avant de pouvoir lancer l'inférence sur un patient, il est nécessaire de télécharger les poids du réseau. On remets ainsi les directives inscrite dans le fichier README du dépôt Git original :

```
This repository includes large models that are hosted on Google Drive due to their size. To download the models, follow these steps:

Click on the following link to access the model files:

https://drive.google.com/file/d/1zfGIV_1k6YgijsEJUO9jVccN9Z67eJgi/view?usp=drive_link

Once the Google Drive page opens, click on the "Download" button to download the model file to your local machine.

After downloading, please place the model files in a folder named "models" within the "main/src" directory.
```

# Lancement de l'inférence

## Pour un seul patient
### Avec Docker
```
docker run -it -v /home/antho/CLIPS/DONNEES/11011101221002:/input -v /home/antho/CLIPS/DONNEES/Sortie_algo:/output tmtv-net-inference
```

### Sans Docker
Se placer dans le dossier où se trouve le fichier main.py (pour nous : home/clips/Projet_CLIPS_DATASIM_2025/CLIPS/CODES/CODE_qurit-frizi/main/) puis exécuter :

Pour la configuration du PC au CHU :
```
python /home/clips/Projet_CLIPS_DATASIM_2025/CLIPS/CODES/CODE_qurit-frizi/main/main.py -it -v /home/antho/CLIPS/DONNEES/dicom/11011101221002:/input -v /home/clips/Projet_CLIPS_DATASIM_2025/CLIPS/DONNEES/pred_masks:/output tmtv-net-inference
```

## Pour plusieurs fichiers
### Version de Yahya (avec docker)
for file in ./dicom/*; do sudo docker run -it --gpus all -v "$file":/input -v '/home/yahya/Documents/Stage TMTV-NET/data/pred_masks':/output tmtv-net-inference-no-sitk; done

### Version projet CLIPS (sans docker)

# Petites commandes utiles
Obtenir la liste des fichiers et de leur détails :
```bash
ll
```

Affichage des propriétées d'un fichier dicom :
```bash
dcmdump PI_001_fd643c2091824b33803d2555c95fd571.dcm
```
Rechercher un mot dans tous les fichiers dans un dossier :
```
Utiliser l'outil 'Search (ctrl+shift+F)' de VS Code (représenté par une loupe)
```