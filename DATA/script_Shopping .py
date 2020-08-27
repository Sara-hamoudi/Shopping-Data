# -*- coding: utf-8 -*-


# Import des librairies
# !!! On importe pas mal de librairies pour lire du html, ce qui n'est pas utile si on 
# a directement des fichiers csv
import pandas as pd
import html2text
import codecs
from io import StringIO
import re
import json

# on commence par lire les 3 fichiers html (si on avait un seul fichier csv, ce serait bien plus simple)
data_csv = pd.DataFrame(columns=['name', 'email', 'age', 'gender', 'product'])
for filename in ["data_sample.csv.html", "data_sample2.csv.html", "data_sample3.csv.html"]:
    f=codecs.open(filename, 'r')
    data = f.read()
    h = html2text.HTML2Text()
    text_csv = re.sub('<.+>', '', data)
    text = h.handle(data)
    df = pd.read_csv(StringIO(text_csv[2:]), sep=';', names=['name', 'email', 'age', 'gender', 'product'])
    data_csv = data_csv.append(df)
data_csv.reset_index(inplace = True, drop=True)
print(data_csv.head())

# on a maintenant un beau dataframe, mais il reste a traiter deux choses:
# la lecture a creer une modification de nom a corriger
# !!!!!!!!!!!! A revoir si on a un csv en entree et non du html
data_csv["product"].replace({"Arts &amp": "Arts and Craft"}, inplace=True)
# on cree la classe d'age
data_csv["classe_age"] = data_csv.age.apply(
        lambda x: "18-25"*(x<26) +  "26-40"*((x>25)&(x<41)) + "41-60"*(x>40)
        )


###################### CREATION DES JSON ######################


############
# Par classe d'age
############

# On va creer un dictionnaire que l'on va remplir au fur et a mesure
by_class_age = {"type": "Tranche d'age"}

# ici, on fait les statistiques par classe d'age et type de produit considere
df_groupby1 =  data_csv.groupby(["classe_age", "product"])["name"].count()
# pour chaque categorie d'age
for age_cat in ["18-25", "26-40", "41-60"]:
    # on garde que les donnees correspondantes en changeant les noms de colonnes
    considered_classe = df_groupby1[age_cat].reset_index().rename({"name":"population"}, axis=1)
    # on ajoute les donnees dans le dictionnaire, avec la clef correspondant a la categorie d'age
    by_class_age[age_cat] = considered_classe.to_dict(orient="records")
    
# maintenant, on enregistre le fichier json dans le meme doc que notre code
with open('tranche_age.json', 'w', encoding='utf-8') as f:
    json.dump(by_class_age, f, ensure_ascii=False, indent=4)

############
# Par genre
############

# meme fonctionnement qu'au dessus, avec genre au lieu de classe_age
by_gender = {"type": "Genre"}

df_groupby2 = data_csv.groupby(["gender", "product"])["name"].count()
for gender in ["male", "female"]:
    considered_classe = df_groupby2[gender].reset_index().rename({"name":"population"}, axis=1)
    by_gender[gender] = considered_classe.to_dict(orient="records")
    
# de meme, on enregistre le fichier json
with open('genre.json', 'w', encoding='utf-8') as f:
    json.dump(by_gender, f, ensure_ascii=False, indent=4)

############
# Par classe d'age 
# et genre
############
    
# meme fonctionnement global avec qqs petites diffs
by_class_age_and_gender = {"type": "Tranche d'age"}

# on commence par regrouper par classe d'age, genre ET produit
df_groupby3 = data_csv.groupby(["classe_age", "product", "gender"])["name"].count()
# ensuite, pour chaque classe d'age
for age_cat in ["18-25", "26-40", "41-60"]:
    # on garde que les donnees correspondantes a la classe d'age
    considered_classe = df_groupby3[age_cat].reset_index().rename({"name":"population"}, axis=1)
    # on cree une liste vide pour chaque classe d'age comme ce qui est voulu dans l'exemple
    by_class_age_and_gender[age_cat] = []
    # on rempli la liste vide de chaque classe d'age en traitant une a une chaque categorie de produit
    for prod_category in set(data_csv["product"]):
        df = considered_classe[considered_classe["product"] == prod_category]
        # ici, on cree le dictionnaire sous le format voulu dans l'exemple
        by_class_age_and_gender[age_cat].append(
            {"name": prod_category, 
             "population": int(df.population.sum()), # somme des hommes et femmes
             "male": int(df[df["gender"]=="male"].population.values[0]),  # hommes
             "female": int(df[df["gender"]=="female"].population.values[0]) # femmes
            }
        )
        
# de meme, on enregistre le fichier json
with open('genre_et_class_age.json', 'w', encoding='utf-8') as f:
    json.dump(by_class_age_and_gender, f, ensure_ascii=False, indent=4)