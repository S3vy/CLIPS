---
Titre: Projet CLIPS
Auteurs: FALK Anthonin & HAMIE Bachar
Date de création: 20/11/2024
---
# Description
Ce projet a pour but d'améliorer les performances du réseau TMTV-Net dévelopé par F. Yousefirizi et al en 2024 qui réalise une segmentation automatiques d'images TEP/CT. Cette amélioration est supposée s'appuyer sur les méthodes de Curriculum Learning que nous avons trouvé dans la litérature. Nous abrégerons l'expression "Curriculum Learning" en CL par la suite.

Ce projet s'inscrit dans le cadre de l'option DATASIM de l'École Centrale de Nantes sur l'année scolaire 2024-2025. 

## Recherche biobliographique

Nous avons débuté ce travail par une étape de réalisation d'un état de l'art des méthodes de CL déjà existantes dans la litérature scientifique. Toutes les sources que nous avons utilisées peuvent être trouvées dans le dossier <code>DOCUMENTATION/ARTICLES</code> et un rapport presque complet de ces méthodes est disponible sous la forme d'un fichier Markdown ici : <code>DOCUMENTATION/NOTES_SUR_LES_ARTICLES/Comparaison_methodes_Curriculum_Learning.md</code>

## Compréhension du code

### Inférence (ie. segmentation d'un patient)

Le lancement de l'inférence se fait grâce au fichier <code>main/main.py</code>, l'appel fonctionne correctement avec les commandes docker mais 

### Entraînement du réseau

## Difficultés rencontrées

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

# Construction du Docker ou de l'environnement venv
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
Pour le PC au CHU, un environnement micromamba, miniconda ou conda est incompatible avec le programme (j'ai vraiment essayé de toutes mes forces).

# Avant le lancement de l'inférence
Avant de pouvoir lancer l'inférence sur un patient, il est nécessaire de télécharger les poids du réseau. On remets ainsi les directives inscrite dans le fichier README du dépôt Git original (il serait bon toutefois de vérifier si le lien change au cours du temps sachant qu'il fonctionne correctement en mars 2025) :

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

```bash
docker run -it -v /home/antho/CLIPS/DONNEES/11011101221002:/input -v /home/antho/CLIPS/DONNEES/Sortie_algo:/output tmtv-net-inference
```

### Sans Docker (avec environnement venv activé)
Le lancement sans Docker demande de ne pas appeller le fichier <code>main/main.py</code> tel qu'il a été écrit mais une version modifiée telle que décrite dans la section **Compréhension du code**.

Avec ça en tête, il faut se placer dans le dossier où se trouve le fichier main.py (pour nous : home/clips/Projet_CLIPS_DATASIM_2025/CLIPS/CODES/CODE_qurit-frizi/main/) puis exécuter (dans le cas de la configuration du PC au CHU) :

```bash
python main.py /home/antho/CLIPS/DONNEES/dicom/11011101221002:/input -v /home/clips/Projet_CLIPS_DATASIM_2025/CLIPS/DONNEES/pred_masks:/output tmtv-net-inference
```

## Pour plusieurs fichiers
### Version avec Docker (ligne de commande proposé par Yahya)
for file in ./dicom/*; do sudo docker run -it --gpus all -v "$file":/input -v '/home/yahya/Documents/Stage TMTV-NET/data/pred_masks':/output tmtv-net-inference-no-sitk; done


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