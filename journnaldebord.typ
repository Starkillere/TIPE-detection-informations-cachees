#align(center)[
  = Carnet de recherche
  _par Ayouba Anrezki \ Initialisation : 12/03/2024 \ MÀJ : 12/03/2024 _
]

#set heading(numbering: "1.1.1 :")

= 12/03/2024 : Définition du sujet.
== Définition du problème
La stéganographie désigne l'art de dissimler de l'information de manière subtile.
Tout la sécurité de cette méthode de dissimulation réside dans la non connaissance des observateur non averties,
de la présence d'une information cachée. La variante informatique de ce procéder consite dans la dissimulation des donnée dans le coprs d'autres donnée.
Si la stéganographie permet de transférer des donnée à l'abrie du regards des observateurs non averties, nous pouvons toujours nous demander si
il n'est pas possible d'affaiblir la sécurité de cette méthode de dissimulation. *Autrement dit est-il possible de distinguer le bruit d'une information cachée ?*
== Idée d'orientation 
Il existe un champs de recherche à part entiere qui s'interresse à la distinction entre donnée pur et donnée issue d'une procéssuce stéganographique qui se nomme #link("https://fr.wikipedia.org/wiki/St%C3%A9ganalyse")[Stéganalyse]
=== Méthodes de distinction
- *Analyse statistique :*  \ Les données qui contiennent simplement du bruit peuvent avoir des caractéristiques statistiques différentes de celles qui cachent des informations. Vous pourriez étudier des mesures telles que l'entropie, la distribution des valeurs de pixels, les corrélations spatiales, etc.

- *Analyse de la fréquence :* \ Les images qui cachent d'autres images peuvent avoir des motifs de fréquence différents de ceux des images contenant seulement du bruit. Les techniques de transformée de Fourier ou d'ondelettes peuvent être utiles pour analyser ces différences.

- *Analyse visuelle :* \ Même si les données semblent similaires visuellement, il peut y avoir des artefacts ou des modèles non perceptibles à l'œil nu. Vous pourriez explorer des techniques de traitement d'image avancées pour mettre en évidence ces différences.

- *Apprentissage automatique :*  \ Vous pourriez également explorer des approches basées sur l'apprentissage automatique, où vous entraînez un modèle à différencier les deux types de données à partir d'un ensemble d'exemples étiquetés.

= L'analyse statistique

= 02/04/2024 : Phénomène aléatoire
== Entropie de Shannon
== Théorie de l'information
= 02/04/2024 :  Meqsure 

#line(length: 500pt)
= 12/09/2024 - Implémentation Ocaml
- Implémentation ocaml des algorithme pour la stéganographie image et

= 19/09/2024 - git init et recher documentaire.
== Définition de la problèmatique
  *Problématique* : Est-il possible de créer un algorithme de stéganalyse géneraliste, i.e un algorithme qui n'a pas connaissance du mode de dissimulation utilisé ?

  *Les differents modes de dissimulation :*
    - Système de substitution : remplacer une partie de la cover (1) par des donnée de l'information à dissimulée.
    - Transformation des paramètre de la cover : modification des paramètre physique de la cover en fonction de l'information à dissimulé (ex: fréquence)
    - Même choses avec le spectre.
    - Méthode statistique : modifier la distribution statistique de la cover en fonction de la stégo.
    - Techniques de distortion : stocker des informations par distorsion du signal et mesurer l'écart par rapport à la couverture originale lors de l'étape de décodage
    - Méthodes de génération de couverture : encoder les informations de manière à cacher un secret la communication se crée.
  
  *Objectif :* Trouver un invariant de dissimulation !

= 26/09/2024 : Prolongement par continuité de la semaine dernière (lecture 10)
- *problèmatique : * Est-il possible d'identifier un paternel, une caractéristique propre aux données issues du processus de stéganographie ?

== Protocole :
 - Étudier les differentes méthodes de stéganograpbhie (substitution, Transformation, spectre, statistique, distortion, géneration de cover)
 - Étudier la réponse stéganalyse à ses algorithmes
 - Identification d'invariant de dissimulation 

== 03/10/2024 : Définition formelle de l'information : 
  [ \
    l1 |(1,0,1) (1,0,1)| \
    l2 |(0,0,0) (0,0,0)| \
  ] \

  Une information est une matrice de tuple de taille n de nombre binaire sur.
  - *Cas de base :*
    - *Information vide (null) : * #pad(x:20pt)[
    On note $epsilon$ l'information vide de taille $|epsilon| = 0$ \   
    $epsilon = mat()$]
    - *Information de base :* #pad(x:20pt)[
      $forall space (b_n) in BB^NN$ fini $L =  mat((b_0b_1...b_n))$ de taille $|L| = n+1$
    ]
    - *Notation* #pad(x:20pt)[
      - On note $cal(M)_(n,p,l) (BB^NN)$ l'ensemble des information de matrice dans $cal(M)_(n,p) (BB^NN)$ dont les tuple sont de $l$ élément.
    ]

    - *Operation sur les informations :*
     - *Taille d'une information :* $"Soit" L in cal(M)_(n,p)(BB^NN) "une information"$, la taille de $L$ est noté $|L| = n×p$
     - *Caractéristiques d'une information :* $"Soit" L in cal(M)_(n,p)(BB^NN) "une information" $
     - *Union/Intersection :* $"Soit" L_1 "et" L_2 "deux information de taille" n$
      - $L_1 union L_2 =$
  
  


=  Vocabulaire (MAJ 12/03/2024)
+ donnée pur : donnée de cachant pas d'autres données issue d'un processuce stéganographique.
+ cover : suport pour la dissimulation d'information cachée.
+ stego : information à cachée.
+

= Lecture en attente :
+ #link("https://utt.hal.science/hal-02470070/document")\
+ #link("https://fr.wikipedia.org/wiki/Entropie_de_Shannon")\
+ #link("https://fr.wikipedia.org/wiki/Th%C3%A9orie_de_l%27information")\
+ #link("https://hal.science/hal-00394108/document")\
+ #link("https://greenteapress.com/thinkdsp/thinkdsp.pdf")\
+ #link(" http://tinyurl.com/thinkdsp08")\ // REP- pour les algo de traitement de signale
+ #link("https://fr.wikipedia.org/wiki/Algorithme_de_Knuth-Morris-Pratt")\
+ #link("https://theses.hal.science/tel-00706171v2/file/RCogranne_soutenance.pdf")
+ #link("https://repository.root-me.org/St%C3%A9ganographie/FR%20-%20Analyse%20st%C3%A9ganographique%20d%27images%20num%C3%A9riques.pdf")
+ #link("https://d1wqtxts1xzle7.cloudfront.net/11025045/22359536_lese_1-libre.pdf?1363619886=&response-content-disposition=inline%3B+filename%3DA_survey_of_steganographic_techniques.pdf&Expires=1726758425&Signature=UWNEvv4JIxHsL-iZcX-PzwvRlbmce0~unnnAUFS2lB~tsuJUbrH1Mzt4ZnO~D1Dhn9DKUo0jtG-BZnkuZYYz5iSvTUuJHJJqcZ65yceho5qgmi7Jpv9OnJsNLxnqAjhHp~frVhRI3yYvhmZRsOL0gdCCCy6O5Bb9XcylGMKZA5k8SZq0Jqme~XdEXRGESCvJy69F2bQ5K~X5IF9j5VaYj7WMOj~n-QC8DG2cJBk-1GRz5NbPu5Udq4R1U-pr2GvYZKJJmqnb7MQoutftG~9-jS~WMxnag3IlAe8g~vlz87mWWLxGle-6fbBg1I-EOa63b3fzUVsFY2bLQo0WgwqNMQ__&Key-Pair-Id=APKAJLOHF5GGSLRBV4ZA")