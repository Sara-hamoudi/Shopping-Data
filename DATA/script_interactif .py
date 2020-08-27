# -*- coding: utf-8 -*-
import json

# on telecharge les json
with open('tranche_age.json', 'r', encoding='utf-8') as f:
    tranche_age = json.load(f)
    
with open('genre.json', 'r', encoding='utf-8') as f:
    genre = json.load(f)
    
with open('genre_et_class_age.json', 'r', encoding='utf-8') as f:
    genre_et_classe_age = json.load(f)

want_to_stay = True
while want_to_stay:
    type_recherche = input("Tapez a pour rechercher par age, g pour rechercher par genre,"
                           "ag pour les deux \n")
    
    if type_recherche == "a":
        classe_age = input("Pour quelle classe d'age voulez-vous des informations ? pour 18-25, "
             " tapez 1, pour 26-40, tapez 2, pour 41-60 tapez 3 \n")
        if classe_age == "1":
            print(tranche_age["18-25"])
        elif classe_age == "2":
            print(tranche_age["26-40"])
        else :
            print(tranche_age["41-60"])
            
            
            
    
    want_to_stay = "o" == input("Voulez-vous recommencer ? Si oui, taper o. Si non, "
                                "tapez q ou n'importe quelle autre lettre \n")
    

