# -*- coding: utf-8 -*-

import psycopg2
import pandas as pd
import os
# Connexion à la base de données

try:
    conn = psycopg2.connect(
        dbname="gestion_notes",
        user="postgres",
        password="JusT4lonE",
        host="localhost",
        client_encoding="utf-8" 
    )
    print("Connexion réussie!")
except psycopg2.Error as e:
    print(f"Erreur de connexion à la base de données: {e}")
#finally:
#    if conn is not None:
#        conn.close()s
# Création d'un curseur
#try:
#    cursor = conn.cursor()
#    print(f"le cursor est active")
#except psycopg2.Error as e:
#    print(f"Erreur lors de la création du cursor : {e}")

    
# Fonction pour ajouter une note d'étudiant
def ajouter_note(nom, math, physique, science, anglais, algorithme, jpe):
    try:
       cursor = conn.cursor()
       cursor.execute("INSERT INTO notes_module (nom, math, physique, science, anglais, algorithme, jpe) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                      (nom, math, physique, science, anglais, algorithme, jpe))
       conn.commit()
    except psycopg2.Error as e:
        print(f"Erreur lors de l'insertion des notes : {e}")
#    finally:
#        if cursor is not None:
#            print ("fermer le cursor ")
#            cursor.close()


# Utilisation des fonctions
ajouter_note("naruto uzomaki", 9, 5, 11, 2, 1, 4)
ajouter_note("sakura tsu", 13, 10, 11, 15 , 13, 14)
ajouter_note("hinata hyuga",15 , 9, 10, 11, 13, 14)
ajouter_note('itachi ushiwa', 12, 14, 15, 11, 13, 15)   

# Fonction pour extraire les données des étudiants avec une moyenne supérieure à 10
def extraire_etudiants_moyenne(sign,seuil):
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM  notes_module WHERE (math + physique + science + anglais + algorithme + jpe) / 6 {sign} {seuil}")
        data = cursor.fetchall()
        return data
    except psycopg2.Error as e:
        print(f"Erreur lors de l'extraction des etudiants : {e}")
        return None
    
# Extraire les étudiants avec une moyenne supérieure à 10

etudiants_moyenne_sup_10 = extraire_etudiants_moyenne('>',10)
etudiants_moyenne_inf_10 = extraire_etudiants_moyenne('<',10)

# Fermeture des connexions
# Fermeture du curseur
#if cursor is not None:
#    print("fermer le cursor si ce n'est pas le cas ")
#    cursor.close()

## Fermeture de la connexion
if conn is not None:
    print("fermer le connexion si ce n'est pas le cas ")
    conn.close()
#cursor.close()
#conn.close()


# Fonction pour exporter les données vers un fichier CSV tout en gérant les duplications
def exporter_vers_csv(chemin_fichier, nouvelles_donnees):
    # Si le fichier CSV existe déjà, ajoutez les nouvelles données sans dupliquer les informations
    if os.path.exists(chemin_fichier):
        donnees_existantes = pd.read_csv(chemin_fichier)
        nouvelles_donnees = pd.concat([donnees_existantes, nouvelles_donnees]).drop_duplicates().reset_index(drop=True)

    nouvelles_donnees.to_csv(chemin_fichier, index=False)

# Chemin des fichiers CSV
chemin_fichier_sup_10 = "C:\\Users\\Lenovo\\moyenne\\etudiants_moyenne_sup_10.csv"
chemin_fichier_inf_10 = "C:\\Users\\Lenovo\\moyenne\\etudiants_moyenne_inf_10.csv"

# Exportation des données vers les fichiers CSV en gérant les duplications
exporter_vers_csv(chemin_fichier_sup_10, pd.DataFrame(etudiants_moyenne_sup_10, columns=["id", "nom", "math", "physique", "science", "anglais", "algorithme", "jpe"]))
exporter_vers_csv(chemin_fichier_inf_10, pd.DataFrame(etudiants_moyenne_inf_10, columns=["id", "nom", "math", "physique", "science", "anglais", "algorithme", "jpe"]))



## Exportation des données vers un fichier CSV
#df_sup_10= pd.DataFrame(etudiants_moyenne_sup_10, columns=["id", "nom", "math", "physique", "science", "anglais", "algorithme", "jpe"])
###print(df)
##df_sup_10.to_csv("C:\\Users\\Lenovo\\moyenne\\etudiants_moyenne_sup_10.csv", index=False)
#
#
#df_inf_10 = pd.DataFrame(etudiants_moyenne_inf_10, columns=["id", "nom", "math", "physique", "science", "anglais", "algorithme", "jpe"])
#
#df_inf_10.to_csv("C:\\Users\\Lenovo\\moyenne\\etudiants_moyenne_inf_10.csv", index=False)





# Fonction pour exporter les données vers un fichier CSV tout en gérant les duplications
def exporter_vers_csv(chemin_fichier, nouvelles_donnees, colonnes_sans_id):
    # Si le fichier CSV existe déjà, ajoutez les nouvelles données sans dupliquer les informations
    if os.path.exists(chemin_fichier):
        donnees_existantes = pd.read_csv(chemin_fichier)
        nouvelles_donnees = pd.concat([donnees_existantes, nouvelles_donnees]).drop_duplicates(subset=colonnes_sans_id).reset_index(drop=True)

    nouvelles_donnees.to_csv(chemin_fichier, index=False)

# Chemin des fichiers CSV
chemin_fichier_sup_10 = "C:\\Users\\Lenovo\\moyenne\\etudiants_moyenne_sup_10.csv"
chemin_fichier_inf_10 = "C:\\Users\\Lenovo\\moyenne\\etudiants_moyenne_inf_10.csv"

# Colonnes à ignorer (ici, toutes les colonnes sauf 'id')
colonnes_sans_id = ["nom", "math", "physique", "science", "anglais", "algorithme", "jpe"]

# Exportation des données vers les fichiers CSV en gérant les duplications
exporter_vers_csv(chemin_fichier_sup_10, pd.DataFrame(etudiants_moyenne_sup_10, columns=["id"] + colonnes_sans_id), colonnes_sans_id)
exporter_vers_csv(chemin_fichier_inf_10, pd.DataFrame(etudiants_moyenne_inf_10, columns=["id"] + colonnes_sans_id), colonnes_sans_id)
