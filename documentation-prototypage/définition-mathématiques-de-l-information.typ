#align(center)[
  = Définition mathématiques de l'information.
]

#grid(
  columns: (1fr, 1fr),
  align(left)[
    _par AYOUBA Anrezki_
  ],
  align(right)[
    _10/10/2024_
  ]
)

#line(length: 500pt)

#set heading(numbering: "1.1.1")

On s'intéresse ici à donner une définition inductive de ce qu'est une information pour pouvoir, sans perte de généralité, effectuer de la Stéganographie/Stéganalyse sur une information sans avoir à spécifier son type (image, texte, vidéo...).

= Définition :
On définit une information comme une application $f : ZZ^n -> RR^n$, où :
- $n$ représente la dimension des indices (par exemple, coordonnées spatiales ou temporelles).
- $m$ représente le nombre de composantes associées à chaque indice (par exemple, intensité ou couleur).

Pour rendre cette définition opérationnelle, on représente l'application $f$ sous sa forme dite *matricielle* dans la base canonique de $RR^m$. La représentation matricielle est construite de sorte que :

= Opérations sur la représentation matricielle
- Les opérations matricielles usuelles (addition, multiplication) restent valables pour cette représentation matricielle.
- Il existe un algorithme permettant de convertir une information définie par une application $f$ en sa forme matricielle dans une base canonique, et inversement.
- La représentation matricielle d'une information par un algorithme donné est unique.

= Définition inductive d'une information :
== Cas de base :
=== L'information vide :
On définit l'information vide comme étant l'information de base de taille $0$, notée $epsilon$. Elle correspond à la matrice contenant uniquement des $0$-uplets.


= Note :
- Toute information possède une unique représentation matricielle par un algorithme donné.
- La structure matricielle permet d'unifier la représentation des différents types d'informations, facilitant leur traitement algorithmique dans le cadre de la Stéganographie et de la Stéganalyse.
