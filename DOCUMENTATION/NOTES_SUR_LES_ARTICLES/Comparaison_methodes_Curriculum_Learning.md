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

**Première méthode : Classique**
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

**Deuxième méthode : Théorique**
> La fonction objectif d'apprentissage montrée plus haut est équivalente à la fonction objectif latente suivante :
> 
> $$ \sum_{i=1}^N F_{\lambda}(l_i) = \sum_{i=1}^N \int_0^{l_i} v_i^*(\tau,\lambda) d\tau $$
> 
> où $v^*$ correspond à la solution de la partie précédente.
> 
> Un autre article propose alors une méthode d'optimisation de cette nouvelle fonction objectif grâce à des méthodes de machine learning qui permettraient d'atteindre des points critiques de cette dernière.

**Troisième méthode : Soft SP-regularizers**
> La méthode classique pose un problème car elle ne permet d'obtenir que des poids "durs" (0 ou 1) alors que deux exemples "simples" (ou "difficiles") ont peu de chances d'être aussi important l'un que l'autre dans l'apprentissage. On souhaite donc avoir des poids $v_i^*$ qui soient entre 0 et 1 pour refléter leur "importance" par rapport aux autres.
> 
> Pour cela il faut changer la partie régularisante de la fonction objectif d'apprentissage initiale (ie. $g(v;\lambda)$).
L'article fournit alors (Tableau 5) différentes fonctions de régularisation et ce qu'elles représente en terme de poids $v_i^*$, calculé à partir de $\lambda$ et $l_i$. On peut également trouver en Figure 6 la courbe $v_i^*$ en fonction de $l_i$, à $\lambda$ fixé (=0.8), pour chaque méthode de régularisation. Les auteurs ne proposent pas de méthode pour choisir la meilleure régularisation adaptée à un problème mais précise que l'on peut soi-même créer une fonction régularisante si elle respecte la définition n°4 et qu'il existe des fonctiosn régularisantes implicites (contrairement à celles du Tableau 5 qui sont explicites) qui ont des meilleurs propriétés de robustesse et par conséquence permet aux algorithme de mieux performer. Ces fonctions implicites dérive de fonctions de perte : Huber, Cauchy, L1-L2 et Welsch.

**Quatrième méthode : Prior-embedded SPL**
> Le but de cette méthode est d'inclure de la connaissance à priori dans le choix des valeurs des paramètres $v_i$ comme la mise à 0 de certains $v_i$ pour les cas que l'on sait difficile. Pour cela, on peut soit modifier la fonction de régularisation soit imposer une contrainte à certains $v_i^*$. L'article indique qu'il existe en général 4 types de connaissances à priori qui soient utiles pour le choix des $v_i^*$ (référence 73 de l'article) :
> 1. A priori sur les valeures aberrants : des exemples avec une grande valeur de perte
> 2. A priori sur la régularité temporelle/spatiale : des exemples proches spatialement ou temporellement tendent à avoir des pertes similaires
> 3. A priori sur l'importance de certains échantillons : on sait à l'avance que certains exemples sont plus importants que d'autres.
> 4. A priori de diversité : certains exemples doivent être répartis de manière régulière dans les données pour aider l'algorithme à mieux apprendre.
>
> Les auteurs précisent ensuite des exemples de méthodes à appliquer pour les connaissances a priori de type 3 et 4.
> Pour le type 3, les auteurs proposent plusieurs manière d'implémenter des solutions :
> 1. Modifier la fonction objectif d'apprentissage pour :
> $$ \min_{w,v \in [0,1]^N} \mathbb{E}(w,v;\lambda, \Psi) \sum_{i=1}^N v_i l_i + g(v;\lambda) \text{ s.c. } v \in \Psi$$
> Où $\Psi$ est une *région d'apprentissage* qui doit être convexe et qui admet au moins une solution. Un exemple de $\Psi$ est $\{v | a^{\top} v \leq c\}$ où $c$ est une constante et $a$ un vecteur à $N$ dimensions représentant l'ordre dans lequel les exemples doivent être appris ( $a_i < a_j$ pour chaque paire d'exemple $(i,j)$ où l'exemple $i$ doit être appris l'exemple $j$ ). Voir la référence 67 du document pour plus de précisions
> 2. Modifier la fonction objectif d'apprentissage pour :
> $$ \min_{w,v \in [0,1]^N} \mathbb{E}(w,v;\lambda) \sum_{i=1}^N v_i l_i + h(v; \eta, \lambda) $$
> où
> $$h(v;\eta,p) = \eta \sum_{i=1}^N p_i v_i $$
> où $p_i$ indique valeur de priorité de l'exemple $i$ : plus elle est grande plus l'exemple est simple et la valeur de $v_i$ sera grande. Pour obtenir ce genre de $p_i$ on peut utiliser les différentes mesure de difficulté introduite dans la section 4.2.1 de l'article.
> 3. La méthode SPFTN de la référence 137 de l'article peut combiner les méthodes d'a priori 3 et 4 grâce à la somme pondérée des termes dans les références 134 et 135.
> L'inconvénient de ces méthodes est que l'on a pas de solutions explicites de $v^*$ comme dans le tableau 5. À la place, il faut appliquer une méthode de descente de gradient (voir référence 42) ou d'autres techniques standard comme CVX toolbox (voir référence 134).

**Cinquième méthode : Autres améliorations de SPL**
1. Mise à Jour de $\lambda$
> Depuis le début de cette partie, on considère que lambda varie soi de manière additive soit de manière multiplicative mais toujours de la même façon. Cela peut poser problème car cette méthode peut inclure des exemples trop difficiles trop tôt.
> On cherche donc d'autres méthodes pour mettre à jour $\lambda$. Une solution serait de reprendre une méthode analogue au planificateur Baby Step (section 4.2.2). Le but serait de définir une séquence $\bf{N} = \left\{ N_1,N_2,...,N_T \right\}$ telle que $\forall s<t N_s < N_t$ et $N_T=N$ où $N_t$ correspond au nombre d'exemple à apprendre à la $t-ieme$ epoch. On modifie alors la valeur de $\lambda$ pour assurer que l'on ai bien exactement $N_t$ exemples dont le poids $v_i$ est non nul. La référence 65 propose :
> $$ \lambda_t =
> \left\{ \begin{array}{ll}
> \lambda_0 & t=0 \\
> \lambda_{t-1} + \alpha \cdot \eta_t & 1 \leq t \leq \tau \\
> \lambda_{t-1} & t>\tau
> \end{array} \right. $$
> où $\eta_t$ est égale à la performance du réseau, par exemple l'accuracy (si $\eta_t$ est grand alors on inclura plus d'exemples difficiles et inversement).
> 
> On peut aussi faire du méta-apprentissage de $\lambda$ sur un jeu de données de validation d'exemples de haute et mauvaise qualité, ce qui automatise complètement la mise à jour de $\lambda$
2. Paramètre d'initialisation et paramètre d'arrêt
> L'initialisation et l'arrêt de l'algorithme d'apprentissage représentent des hyperparamètres dont dépendent fortement les résultats du modèle apprenant, il est donc important de ne pas les oublier, bien qu'il soit très difficile d'avoir une vue d'ensemble de l'otimisation en fonction de ces deux paramètres et de $\lambda$. Les références 26 et 61 de l'article proposent donc de ne pas uriliser l'algorithme d'optimisation classique de $v$ et $w$ et de reformuler le problème du self-paced learning comme un problème multiobjectif, ce qui permet d'obtenir un lot de solutions avec des critères d'arrêt différents en n'éxécutant le nouvel algorithme qu'une seul fois et également d'améliorer la robustesse du SPL même avec une mauvaise initilisation.


#### 5.2 - Les points forts
* La détermination de l'échelle de difficulté est semi-automatique (voir presque complètement automatique) et adaptée aux poids du réseau ce qui permet de rendre la courbe d'apprentissage dynamique car on peut la recalculer au cours de l'apprentissage.
* La méthode est basée sur l'apprentissage du réseau lui-même, l'objectif de l'entrainement "classique" et de la courbe d'apprentissage sont les mêmes, ce qui rend la méthode très facile à mettre en place.
* Il est possible de donner de l'information à priori sur les exemples à partir desquels le réseau va apprendre.
* C'est une méthode déjà bien explorée, il existe beaucoup de références auxuquelles nous pourrons surmeent nous comparer.
#### 5.3 - Les points faibles
* Si l'on veut trouver une solution de très bonne qualité (optimisation de plusieurs hyperparamètres), il faudra implémenter des algorithmes complexes, ce qui nous prendra du temps
* Nécessite une deuxième optimisation (dans le cas des régularisations implicites) à chaque epoch, ce qui peut prendre du temps.
* Si le réseau n'est pas suffisemment entrainé, il ne peut pas estimer quels cas sont réellement difficiles à apprendre et quels cas sont abordable.
#### 5.4 - Dans quel cas cette méthode s'applique (taille du dataset, le nombre de classe à prédire, le nombre de données)
Cette méthode est utilisée dans de nombreux domaines :

"CV tasks of visual category discovery [57], segmentation learning [55], [137], image classification [109], object detection [108], [134], reranking in multimedia retrieval [40], person ReID [143] etc., and traditional machine learning tasks of matrix factorization [141], feature selection [142], cross-modal matching [63], co-training [70], clustering [22], [127], [128]"

Mais pas d'exemples précis dans le documents, il faudra lire les références pour plus de détails sur les bases de données employées.
#### 5.5 - Est-ce que ces cas d'application sont proche de notre cas à nous
blabla
#### 5.6 - Les performances de la méthode : comment est calculé le score, quelles améliorations le Curriculum Learning a-t-il appaorté ?
blabla

### 6 - Transfer Teacher
#### 6.1 Résumé de la méthode
Le but est de guider le réseau que l'on cherche à entraîner grâce à un réseau qui servira de professeur. Ce dernier sera pré-entrainé avant le réseau original et on s'appuie sur ses connaissances pour calculer la difficulté liée à chaque exemple. Des exemples de réseaux professeurs sont dans le tableau 6 du document. La plupart s'appuie une méthode qui lie la perte de chaque exemple à travers ce réseau à l'importance du même exemple pour le réseau original. Le principe est le suivant : plus la perte est faible, plus l'exemple est facile à apprendre. On note ici quelques stratégies :

* Stratégie de boostraping (référence 33) :
> On pré-entraine le même réseau sur les données d'entrainement originale mais en appliquant du boostraping. La différence avec le SPL est que le mesureur de difficulté est mature pour le cas du Transfer Teacher avec boostraping alors que la méthode SPL concerne directement le réseau étudiant.

* Stratégie de révision croisée :
> On partitionne les données d'entrainement en $N$ sous-datasets et on entraine des réseaux professeurs sur chacune de ces partitions. Puis, pour chaque exemple de la $i$ème partition, on demande aux $N-1$ professeurs de donner la difficulté de celui-ci (ie. la perte du réseau pour cet exemple).

* Startégie d'incertitude :
> Dans les modèles de langage, le réseau donne en plus des mots une probabilité qui peut servir de fonction de classement d'importance des exemples.

#### 6.2 Les points forts
* Méthode automatique
* A fonctionné sur des exemples similaires
#### 6.3 Les points faibles
* Difficile à d'ajouter de l'information à priori
#### 6.4 Dans quel cas cette méthode s'applique (taille du dataset, le nombre de classe à prédire, le nombre de données)
blabla
#### 6.5 Est-ce que ces cas d'application sont proche de notre cas à nous
blabla
#### 6.6 Les performances de la méthode : comment est calculé le score, quelles améliorations le Curriculum Learning a-t-il appaorté ?
blabla