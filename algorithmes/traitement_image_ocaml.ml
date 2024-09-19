(*
  Traitement de l'image
  Par : Ayouba Anrezki
  initié le : 12/09/2024
*)

(* On définie un pixel comme un tuple de 3 entier  *)
type pixel = int * int * int

(* On definie une image comme une matrice de pixel *)
type image = pixel array array

(* UTILITAIRE : convertisseur decimale à binaire 

spécification 
  Post-conditions : entier -> un entier naturel dans [|0;255|]
  Pré-condition : la sortie et le binaire d'entier sur 8 bits (Identifier type binaire) *)

type binaire =  bool array

let convertisseur_decimal_binaire  (entier: int) : binaire = 
  let versbin:binaire = [|0;0;0;0;0;0;0;0|] in
  let quotient = ref (entier)/2 in
  let divdante  = ref ()