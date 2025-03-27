---
Titre: Projet CLIPS
Auteurs: FALK Anthonin & HAMIE Bachar
Date de création: 20/11/2024
---
# Description
Ce projet a pour but d'améliorer les performances du réseau TMTV-Net dévelopé par F. Yousefirizi et al en 2024 qui réalise une segmentation automatiques d'images TEP/CT. Cette amélioration est supposée s'appuyer sur les méthodes de Curriculum Learning que nous avons trouvé dans la litérature. Nous abrégerons l'expression "Curriculum Learning" en CL par la suite.

Ce projet s'inscrit dans le cadre de l'option DATASIM de l'École Centrale de Nantes sur l'année scolaire 2024-2025. 

## Recherche biobliographique

Nous avons débuté ce travail par une étape de réalisation d'un état de l'art des méthodes de CL déjà existantes dans la litérature scientifique. Toutes les sources que nous avons utilisées peuvent être trouvées dans le dossier <code>DOCUMENTATION/ARTICLES</code> et un rapport presque complet de ces méthodes est disponible sous la forme d'un fichier Markdown ici : <code>DOCUMENTATION/NOTES_SUR_LES_ARTICLES/Comparaison_methodes_Curriculum_Learning.md</code>. Il y a également les slides que nous avons réalisés pour une présentation qui sont stocké à cet endroit : <code>REUNIONS/presentation CLIPS 17 janvier.pdf</code>

## Compréhension du code

### Inférence (ie. segmentation d'un patient)

Lors des derniers essais sur mon ordinateur personnel, j'ai du modifier l'appel d'une fonction de pydicom afin de faire fonctionner l'inférence : dans le fichier <code>"/home/antho/CLIPS/CODES/CODE_qurit-frizi/main/src/DicomNiftiConversion.py</code> aux lignes 70 et 94 j'ai changé la fonction **read_file** par **dcmread** et cela résout le problème.

Nous ne nous sommes pas trop penchés sur le code de l'inférence car il fonctionnait déjà très bien, ce qui nous importait concernait plutôt la partie entraînement.

### Entraînement du réseau

Pour l'entrainement nous avons trouvé trois fichiers correspondant à l'enytrainement du réseau de neurones.

Le premier est <code>CODES/CODE_qurit-frizi/main/src/trainer.py</code>, il contient uniquement des fonctions utiles pour la suite de l'entrainement.

Le deuxième est <code>CODES/CODE_qurit-frizi/main/src/trainer_v2.py</code>, il contient la classe **TrainerV2** qui est le coeur du fonctionnement de l'entrainement du réseau. La fonction principale de cette classe est la fonction **fit**. Dans cette fonction, la partie qui nous intéresse pour le Curriculum Learning est la section débutant à la ligne 371 par :
```py
for epoch in range(num_epochs):
                logger.info('started training epoch {}'.format(epoch))
                run_eval = (epoch == 0 and not self.skip_eval_epoch_0) or (epoch + 1) % eval_every_X_epoch == 0

                outputs_epoch, history_epoch = self.run_epoch_fn(
                    options,
                    datasets,
                    optimizers,
                    model,
                    losses,
                    schedulers,
                    per_step_scheduler_fn,
                    history,
                    callbacks_per_batch,
                    callbacks_per_batch_loss_terms,
                    run_eval=run_eval,
                    force_eval_mode=False)
                history.append(history_epoch)
                ...
```
Ce qu'on voudrait faire, pour modifier l'ordre dans lequel les données sont vue par le réseau, c'est ajouter une ligne de code juste avant "outputs_epoch, history_epoch = self.run_epoch_fn(" qui créerait un dataset courant, modifié à chaque epoch. Cela pourrait donner :
```py
for epoch in range(num_epochs):
                logger.info('started training epoch {}'.format(epoch))
                run_eval = (epoch == 0 and not self.skip_eval_epoch_0) or (epoch + 1) % eval_every_X_epoch == 0

                current_dataset = curriculum_learning(epoch,current_dataset,global_dataset,history,losses,...)

                outputs_epoch, history_epoch = self.run_epoch_fn(
                    options,
                    current_dataset,
                    optimizers,
                    ...
```

Le troisième est <code>CODES/CODE_qurit-frizi/main/src/segmentation/trainer.py</code>, c'est le fichier qui fait appel à la classe **TrainerV2** afin de l'utiliser pour entrainer un réseau de neurones. La foncion de ce fichier qui fait appel à **TrainerV2** s'appelle **run_trainer** (ligne 57). Cette fonction (comme beaucoup d'autres dans le code), fait donc appel à un objet de type **Dataset**, qui est défini comme étant (d'après la documentation de la fonction **fit** de la classe **TrainerV2** ligne 198):
```py
datasets:  a functor returning a dictionary of datasets. Alternatively, datasets infos can be specified.
            `inputs_fn` must return one of:

            * datasets: dictionary of dataset
            * (datasets, datasets_infos): dictionary of dataset and additional infos

            We define:

            * datasets: a dictionary of dataset. a dataset is a dictionary of splits.
                a split is a dictionary of batched features.
            * Datasets infos are additional infos useful for the debugging of the
                dataset (e.g., class mappings, sample UIDs). Datasets infos are
                typically much smaller than datasets should be loaded in
                loadable in memory
```
Avec une telle description, nous espérions trouver un exemple de la fonction **run_trainer** dans le code afin d'avoir exemple de la formation d'un **Dataset** à partir de données réelles, mais nous n'en avons pas trouvé. Nous avons tout de même recherché les fonction permettant la création d'un objet de type **Dataset** mais nous n'avons pu trouver que le fichier <code>CODES/CODE_qurit-frizi/main/src/datasets.py</code> qui ne nous as pas vraiment aidé à comprendre. Nous sommes donc restés bloqués face à ce problème où seule l'équipe de Vancouver ayant développé le code aurait pu nous aider, car ce code est bien trop trop avancé pour nous. Cependant, nous n'avons eu aucune réponse de leur part sur ce sujet, ce qui nous a empêcher de continuer à avancer au delà de ce point dans notre compréhension du code.

## Difficultés rencontrées

- La création de l'environnement : ne pas utiliser autre chose que venv au CHU, cela fait perdre beaucoup de temps pour rien (mais si la personne qui reprend le projet réussit à utiliser conda je pense que cela serait tout de même mieux que venv)

- Le code est "trop" bien structuré dans le sens où chaque fichier contient des informations complémentaires et le nom de chaque fichier n'est pas suffisant pour savoir quel fichier appel un autre. Un schéma explicatif aurait été très utile pour rapidement comprendre les dépendances de tous les fichiers entre eux. L'ajout d'un en-tête en haut de chaque fichier pourrait également servir à connaire rapidement le contenu de chaque fichier au lieu de perdre du temps à essayer de comprendre soi-même le sens de chaque fonction ainsi que l'endroit où elle est utilisée.


# Structure de ce dépôt
- **CODES** : Ces sont les fichiers qui correspondent au code de TMTV-Net
    - **CODE_qurit-frizi** : Le code original (version du 19 décembre 2024) de TMTV-Net (disponible à l'adresse https://github.com/qurit-frizi/TMTV-Net). Nous y avons cependant ajouté quelques fichiers, notamment *main_modif.py* dans le dossier <code>main/</code>. Comme son nom l'indique, c'est une version modifiée de *modif.py* qui est le fichier original. La seule grosse modification que ce fichier a reçu est celle qui permet de l'éxécuter directement avec python, sans passer par Docker.

    - **CODE_Yahya** : Le code utilisé par Yayha (stagiaire ayant travaillé pendant 5 mois sur le projet). Nous n'avons noté aucune différence avec le code originale mais il est possible qu'il y en ait et que nous nous en somme pas aperçu. Nous avons donc préféré le garder dans le doute.

- **DOCUMENTATION** : 
    - **ARTICLES** : Les articles que nous avons lu en lien avec le sujet. Parmis ces articles se trouve celui de la publication originale de TMTV-Net et les autres traitent du sujet du Curriculum Lerning.

    - **DOCS_Yahya** : La documentation produite par Yahya pendant son stage. Nous ne l'avons pas assez consulté à mon avis, il serait bon de la relire une fois complètement, d'autant plus qu'elle est assez courte.

    - **NOTES_SUR_LES_ARTICLES** : Nos prise de note sur les articles que nous avons lut pendant notre étape d'état de l'art des méthode de Curriculum Learning.

- **DONNEES** : Le dossier contenant les données utilisées
    - **dicom** : Le dossier contient, pour chaque patient, un dossier à son nom/numéro. Chaque dossier patient contient au moins deux sous-dossiers : un pour l'image CT et un pour l'image TEP.
    - **pred_masks** : Le dossier pour stcoker les masques prédits par TMTV-Net à partir des données du dossier **dicom**
    - **metriques.txt** : Un exemple de fichier métrique sortie par le code de Yahya afin de l'exploiter pour en créer un fichier csv.

- **INFORMATION_PROBLEMES_SEGMENTATION** : Le dossier contenant toutes les informations utiles pour savoir quel patient a bien ou n'a pas bie été segmenté par TMTV-Net la première fois.

- **REUNIONS** : Le dossier contenant toutes les slides de présentation durant notre projet afin d'avoir un suivi de l'évolution du travail.

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

Le lancement de l'inférence se fait grâce au fichier <code>main/main.py</code>. L'appel fonctionne correctement avec les commandes utilisant Docker mais il a fallu légèrement modifier le code pour l'appeler en ligne de commande bash sans passer par Docker.

L'inférence prend en général quelques minutes (environ 5) avec Docker mais avec un environnement virtuel venv cela prend beaucoup plus de temps (parfois une demi-heure) sans garantie de résultats et sans que nous sachions vraiment pourquoi. Peut-être que cela est dû à l'utilisation de venv plutôt qu'une autre manière de gérer les environnement comme conda, miniconda ou micromamba, lais c'est un problème que nous n'avons pas réussi à régler en raison des pare-feux du CHU.

Cependant, ces problèmes sont à nuancer car des essais de dernière minute avec la version finale de <code>main_modif.py</code> sur un PC personnel utilisant un GPU et un environnement micromamba permettent d'obtenir un résultats en moins de deux minutes. Il se peut donc que cette rapidité soit le fruit des dernières améliorations du code appelant l'inférence. Il faudrait confirmer cela en téléchargeant la dernière version du code <code>main_modif.py</code> sur le GitHub puis en executant les commandes décrites ci-dessous pour réaliser l'inférence avec venv sur le PC du CHU.

## Pour un seul patient
### Avec Docker

```bash
docker run -it -v /home/antho/CLIPS/DONNEES/11011101221002:/input -v /home/antho/CLIPS/DONNEES/Sortie_algo:/output tmtv-net-inference
```

### Sans Docker (avec environnement venv activé)
Le lancement sans Docker ne fonctionne pas avec le fichier <code>main/main.py</code> tel qu'il a été écrit originellement. Afin que cela fonctionne, nous avons créé une version modifiée qui peut être appelée via python avec la commande décrite ci-dessous.

Le code modifié (<code>main/main_modif.py</code>) utilise la librairie argparse dans les dernières lignes de code afin d'avoir accès au chemin vers les fichiers d'entrée et le chemin où déposer les fichiers de sortie.

A la fin du code, on peut trouver la partie suivante :
```python
if __name__ == '__main__':
    ...
```
C'est la section qui permet le lancement du code via une ligne de commande dans linux.
On exploite cette strcture afin d'ajouter un moyen de récuperer les fichiers d'entrée, et on écrit (ligne 1205) :
```python
parser.add_argument('--input_dir', help='path to PET and CT volume') #HERE
```
Ces modifications sont faites dans le code disponible sur ce Git, il n'y a donc plus qu'à éxécuter la partie suivante :

Pour l'execution, il faut se placer dans le dossier où se trouve le fichier main.py (pour nous : home/clips/Projet_CLIPS_DATASIM_2025/CLIPS/CODES/CODE_qurit-frizi/main/) puis exécuter (dans le cas de la configuration de mon PC personnel) :

```bash
python3 main_modif.py --input_dir /home/antho/CLIPS/DONNEES/dicom/11011101281001 --output_path /home/antho/CLIPS/DONNEES/Sortie_algo/
```

## Pour plusieurs fichiers
### Version avec Docker (ligne de commande proposée par Yahya)
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