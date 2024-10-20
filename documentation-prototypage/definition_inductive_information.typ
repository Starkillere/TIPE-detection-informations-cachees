#line(length: 500pt)
#align(center)[
  = Définition inductive de l'information par des matrices de n-uplet de nombres réel
]
\
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
On s'interesse ici à donner une définition inductive de ce qu'est une information pour pour pouvoir sans perte de géneralité faire de la Stéganographie/Steganalyse sur une information sans avoir a spécifier sont type (image, texte, vidéo...)

= Définition : 
On définie une information comme étant une matrice de n-uplet de nombres (réel).
Une information est définie sous sa forme dite *matricielle* de tel sorte que : \
Si $M in M_(l,p)$ est la représentation matricielle d'une information tel que le n-uplet de nombres à la position (1,1) de $M$ soit de taille $n$ alors :
- Tout les éléments de la matrice i.e les autre uplet sont aussi de taille $n$
- La taille $M$ noté $|M|$ est donnée par : $|M| = n×l×p$
- tout les n-uplet contient le même type d'éléments et ces éléments sont tous de même type

On définie aussi des opération sur ces matrice  :
- Les opération matricielle usuelle resptent valable pour la représentation matricielle
- Il existe un algorithme permetant de faire le lien entre le lien entre une information est sa forme matricielle.
- La représentation matricielle d'une information par un algorithme donné est unique
= Définition inductive d'une information :
== Cas de bases :
=== L'information vide :
On définit l'information vide comme étant l'information de base de taille $0$ noté $epsilon$, c'est la matrice avec $n×p$ 0-uplet.
=== Les briques de base de l'information
pour tout $x in RR$, $[(x)]$ est la représentation matricielle d'une information par un algorithme.


= Note à moi même : 
Toutes information posséde une unique représentation matricielle par un algorithme donné.
