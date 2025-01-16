# Comparaison entre les différentes méthodes de Curriculum Learning
Auteurs : Anthonin Falk et Bachar Hamie

## Consignes

Pour chaque méthode de Curriculum Learning, il faut :
- Résumé de la méthode
- Les points forts
- Les points faibles
- Dans quel cas cette méthode s'applique (taille du dataset, le nombre de classe à prédire, le nombre de données)
- Est-ce que ces cas d'application sont proche de notre cas à nous
- Les performances de la méthode : comment est calculé le score, quelles améliorations le Curriculum Learning a-t-il appaorté ?

## La liste des articles/morceaux d'articles à lire
La liste des méthodes à regarder :
(Le mieux est de lire l'introductuion du papier avant les sections spécifiée ci-dessous)

### Pour Bachar :
- Bootsraping score dans le papier "Curriculum_Learning_for_Improved_Tumor_Segmentation_in_PET_Imaging.pdf"
- Self-paced score dans le papier "Curriculum_Learning_for_Improved_Tumor_Segmentation_in_PET_Imaging.pdf" et le papier "A Survey on Curriculum Learning"
- Curriculum by Smoothing dans le papier : "NeurIPS-2020-curriculum-by-smoothing-Paper.pdf"
- Predefined CL dans le papier "A Survey on Curriculum Learning", section 4.2.1 et 4.2.2

### Pour Anthonin :
- Self-Paced Learning dans le papier "A Survey on Curriculum Learning", section 4.3.1
- Transfer Teacher dans le papier "A Survey on Curriculum Learning", section 4.3.2
- RL Teacher dans le papier "A Survey on Curriculum Learning", section 4.3.3
- Other Automatic CL dans le papier "A Survey on Curriculum Learning", section 4.3.4

### Comment bien choisir la méthode
Pour nous aider à bien choisir la méthode qu'il nous faut, lire :
- La section 4.4 "How to Choose A Proper CL Method" dans le papier "A Survey on Curriculum Learning"
- La section 5 "Discussions" dans le papier "A Survey on Curriculum Learning"

## Résumé pour chaque méthode

### 1 - CL avec Bootsraping score
#### Résumé de la méthode
blabla
#### Les points forts
blabla
#### Les points faibles
blabla
#### Dans quel cas cette méthode s'applique (taille du dataset, le nombre de classe à prédire, le nombre de données)
blabla
#### Est-ce que ces cas d'application sont proche de notre cas à nous
blabla
#### Les performances de la méthode : comment est calculé le score, quelles améliorations le Curriculum Learning a-t-il appaorté ?
blabla

### 2 - Self-paced Learning
(reprendre la structure de 1 - CL avec Bootsraping score)

### 3 - Curriculum by Smoothing
(reprendre la structure)

### 4 - Predefined CL
(reprendre la structure)

### 5 - Self-Paced Learning (SPL)
*Source : "A Survey on Curriculum Learning"*
#### 5.1 - Résumé de la méthode
Le but est de demander au réseau de commencer par s'entrainer sur les cas ayant les coûts les plus faibles (ie. ceux dont la valeur associée dans la fonction de perte est faible). Voir le schéma b de la figure 2 du document pour une représentation imagée.

**Première méthode (classique) :**
> Dans les faits, on va entrainer successivement le réseau sur toutes les données mais en associant des poids à chaque entrée.
> Dans une boucle, on a une phase de détermination des poids de chaque entrée (rassemblés dans un vecteur $v$ qui est mis à jour) puis une phase d'entrainement sur toutes les données (mise à jour des poids $w$). De plus, lorsque l'on défini une méthode de Curiculum Learning (CL) on défini toujours une fonction objectif d'apprentissage que l'on cherche à minimiser. Dans notre cas cette fonction est :
>
> $$ \min_{w,v \in [0,1]^N} \mathbb{E}(w,v;\lambda) \sum_{i=1}^N v_i l_i + g(v;\lambda) $$
>
> * Mise à jour de $v$ :
> On cherche
> 
> $$ v^*_i = \arg \min_{v_i\in[0,1]} v_i l_i + g(v_i;\lambda) \text{ pour } i = 1,2,...,n$$
> 
> 
> où
> 
> $$ g(v;\lambda) = -\lambda \sum_{i=1}^{N} v_i $$
> 
> est une norme l1 négative. $\lambda$ est un hyperparamètre : le paramètre d'âge qui contrôle la vitesse d'apprentissage. $l_i$ représente la valeur de la perte associée au couple $(x_i,y_i)$ qui est une donnée d'entrainement.
> 
> *Lorsque l'on regarde dans les faits, on a simplement $v^*_i$ qui vaut 1 si $l_i < \lambda$ et qui vaut 0 sinon. $\lambda$ est donc un seuil.*
> 
>* Mise à jour de $w$ :
>On cherche
>
>$$w^* = \arg \min_w \sum_{i=1}^N v^*_i l_i$$
>
>c'est-à-dire entrainer le réseau en mettant des poids devant chaque entrée.
>
> Ces deux étapes sont répétées tandis que la valeur de $\lambda$ augmente graduellement afin d'ajouter des exemples plus difficiles. Voir l'algorithme 2 (p.4564) de l'article pour plus de détails.
> * Mise à jour de $\lambda$ :
    On choisit une valeur initiale de $\lambda$ appelée $\lambda_0$ puis on la met à jour à chaque itération en la multipliant par une valeur plus grande que 1 ou en ajoutant une valeur positive. À la fin, 

**Deuxième méthode (théorique) :**
> La fonction objectif d'apprentissage montrée plus haut est équivalente à la fonction objectif latente suivante :
> 
> $$ \sum_{i=1}^N F_{\lambda}(l_i) = \sum_{i=1}^N \int_0^{l_i} v_i^*(\tau,\lambda) d\tau $$
> 
> où $v^*$ correspond à la solution de la partie précédente.
> 
> Un autre article propose alors une méthode d'optimisation de cette nouvelle fonction objectif grâce à des méthodes de machine learning qui permettraient d'atteindre des points critiques de cette dernière.

**Troisième méthode (SP-regularizers):**
> La méthode classique pose un problème car elle ne permet d'obtenir que des poids "durs" (0 ou 1) alors que deux exemples "simples" (ou "difficiles") ont peu de chances d'être aussi important l'un que l'autre dans l'apprentissage. On souhaite donc avoir des poids $v_i^*$ qui soient entre 0 et 1 pour refléter leur "importance" par rapport aux autres.
> 
> Pour cela il faut changer la partie régularisante de la fonction objectif d'apprentissage initiale (ie. $g(v;\lambda)$). L'article fournit alors différentes fonction de régularisation et ce qu'elles représente en terme de poids $v_i^*$, calculé à partir de $\lambda$ et $l_i$.

#### 5.2 - Les points forts
* La détermination de l'échelle de difficulté est semi-automatique et adapatée aux poids du réseau ce qui permet de rendre la courbe d'apprentissage dynamique car on peut la recalculer au cours de l'apprentissage.
* La méthode est basée sur l'apprentissage du réseau lui-même, l'objectif de l'entrainement "classique" et de la courbe d'apprentissage sont les mêmes, ce qui rend la méthode très facile à mettre en place.
#### 5.3 - Les points faibles
blabla
#### 5.4 - Dans quel cas cette méthode s'applique (taille du dataset, le nombre de classe à prédire, le nombre de données)
blabla
#### 5.5 - Est-ce que ces cas d'application sont proche de notre cas à nous
blabla
#### 5.6 - Les performances de la méthode : comment est calculé le score, quelles améliorations le Curriculum Learning a-t-il appaorté ?
blabla