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

=  Vocabulaire (MAJ 12/03/2024)
donnée pur : donnée de cachant pas d'autres données issue d'un processuce stéganographique.

= Lecture en attente :
#link("https://utt.hal.science/hal-02470070/document")\
#link("https://fr.wikipedia.org/wiki/Entropie_de_Shannon")\
#link("https://fr.wikipedia.org/wiki/Th%C3%A9orie_de_l%27information")\
#link("https://hal.science/hal-00394108/document")\
#link("https://greenteapress.com/thinkdsp/thinkdsp.pdf")\
#link(" http://tinyurl.com/thinkdsp08")\ // REP- pour les algo de traitement de signale
#link("https://fr.wikipedia.org/wiki/Algorithme_de_Knuth-Morris-Pratt")\
#link("https://theses.hal.science/tel-00706171v2/file/RCogranne_soutenance.pdf")
#link("https://repository.root-me.org/St%C3%A9ganographie/FR%20-%20Analyse%20st%C3%A9ganographique%20d%27images%20num%C3%A9riques.pdf")