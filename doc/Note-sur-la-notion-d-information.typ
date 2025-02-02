#line(length: 500pt)
#align(center)[
  = Note sur la notion d'information et ébauche d'une définition formelle
]
\
#grid(
  columns: (1fr, 1fr),
  align(left)[
    _par AYOUBA Anrezki_
  ],
  align(right)[
    _06/01/2025_
  ]
)
#line(length: 500pt)
#set heading(numbering: "1.1.1")
#pad(x:20pt)[
  *Qu'est-ce qu'une information ?* 
  Une information désigne tout élément qui réduit l'incertitude ou apporte un contenu signifiant dans un contexte donné. Elle peut prendre plusieurs formes : symboles, messages, signaux, données, etc.
]

Dans le cadre de mes recherches en stéganalyse, je travaille autour de la problématique de trouver un invariant de dissimulation commun à toute information qui en dissimule une autre, quel que soit l'algorithme de dissimulation utilisé. Pour cela, il m'a été nécessaire de donner une définition formelle et mathématique de ce qu'est une information.

= Approche Matricielle
Dans une première tentative pour définir cette notion, j'avais conceptualisé l'information comme la matrice de ses valeurs codées en binaire. Cependant, cette définition s'est révélée trop lourde et peu efficace pour les algorithmes actuels. Cela m'a obligé à revoir cette approche et à chercher une nouvelle définition de l'information.

= Approfondissement de l'approche matricielle

*Comment définir une information ?* 

Les images, vidéos, sons et autres médias peuvent être vus comme des signaux numériques, c'est-à-dire des fonctions discrètes associant des indices (souvent temporels ou spatiaux) à des valeurs (intensité, couleur, amplitude sonore, etc.). En adoptant cette abstraction, une information peut être représentée de manière formelle comme une fonction mathématique :

$ f: ZZ^n -> RR^n $

- Avec $(n,m) in NN^2$ où :
  - $n$ représente la dimension des indices (par exemple, les coordonnées temporelles ou spatiales).
  - $m$ représente le nombre de valeurs associées à chaque indice.

= Vers une unification des représentations

Cette abstraction matricielle permet de représenter différents types d'informations sous une même forme. En stéganalyse, cela ouvre la possibilité de rechercher des invariants communs dans des algorithmes de dissimulation appliqués à différents médias. La représentation matricielle pourrait également être affinée ou enrichie par des outils comme :

- La *théorie des tenseurs*, pour capturer des relations complexes.
- Des *transformations mathématiques* comme les ondelettes ou la transformée de Fourier, pour extraire des invariants pertinents.
- L'*apprentissage automatique*, où des représentations vectorielles peuvent être apprises automatiquement à partir de données variées.

Ainsi, la définition formelle d'une information comme une fonction discrète ouvre de nombreuses perspectives pour des recherches approfondies en stéganalyse et au-delà.
