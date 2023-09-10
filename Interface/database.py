import sqlite3

def ajouter_bd():
    try:
        connexion = sqlite3.connect("BD_TPsynthese.db")
        cur = connexion.cursor()
        #print("je suis connecté")
        cur.execute('''
            CREATE TABLE IF NOT EXISTS tentatives (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                noTentative TEXT,
                dateHeureTentative TEXT,
                code TEXT,
                nom TEXT,
                acces TEXT)''')

        connexion.commit()
    except sqlite3.Error as error:
        print(f"Erreur lors de la connection a la bd:  {error}")
    finally:
        if connexion:
            connexion.close()

def ajouter_table(tentative):
    try:
        connexion = sqlite3.connect("BD_TPsynthese.db")
        cur = connexion.cursor() 
        cur.execute('''
            INSERT INTO tentatives (dateHeureTentative,code,noTentative,nom,acces)VALUES (?, ?, ?, ?, ?)''', 
            (tentative.dateHeureTentative, tentative.code, tentative.noTentative, tentative.nom, tentative.acces))
        connexion.commit()
    except sqlite3.Error as error:
        print(f"Erreur lors de l'ajout de la tentative : {error}")
    finally:
        if connexion:
            connexion.close()


""" def selection_tentatives():
    try:
        connexion = sqlite3.connect("BD_TPsynthese.db")
        cur = connexion.cursor()

        cur.execute("SELECT * FROM tentatives") 

        tentatives = cur.fetchall() 
    except sqlite3.Error as error:
        print(f"Erreur lors de la selection de tentative: {error}")
    finally:
        if connexion:
            connexion.close() 

    return tentatives """
