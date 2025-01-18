#line(length: 500pt)
#align(center)[
  = Définition mathématiques de l'information.
]

#grid(
  columns: (1fr, 1fr),
  align(left)[
    _par AYOUBA Anrezki_
  ],
  align(right)[
    _15/01/2025_
  ]
)
#line(length: 500pt)
#set heading(numbering: "1.1.1")

= Les algorithmes de dissimulation et d'extraction.
== LSB
== DTC
== MPA
= Base de données
== Prototypage :
```typ
- hote_data 
        -> id
        -> path
        -> type
        -> méthode 
        -> taille
        -> Note // des note que je pourrai ajoputer

- hide_data // la donnée a caché
        -> id
        -> content
        -> type // toujour du texte
        -> id_hoteData // l'id de l'hote qui lui est associé
        -> taille
        -> Note

- cover_data
        -> id
        -> path
        -> type 
        -> id_hideDat // identifiant de la donnée caché

- data // donnée de l'etude 
        -> id
        -> id_coverData // identifiant de la conver
        -> Entropie_des_données_cachées
        -> Variance des données porteuses
        -> tests de normalité
        -> Résistance_à_la_compression
        -> Résistance_au_bruit
        -> test_du_khi_carree
        -> spectre
        -> transformation_en_serie_de_fourrier
        -> transformation_en ondelette
        -> La_transformée_de_Laplace,
        -> La_transformée_en_Z,
        -> La_DCT_pour_la _ompression,
        -> L_analyse_de_la_densité_spectrale_de_puissance
```
Note a moi même : récuper juste des donnée sur le net et impose leur le traitement et bim
