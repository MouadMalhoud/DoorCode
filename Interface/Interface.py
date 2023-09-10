import tkinter as tk
from tkinter import ttk
import serial
import database
import re
from moduleTPSynthese import Tentative

s = serial.Serial("COM3")

global journal 
journal = []
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TP Synthèse Mouad Malhoud - Porte de sécurité")
        self.geometry("600x400")

        #self.statut = "inactif"

        self.lbl_entry = ttk.Label(self, text="Entrez votre nom:")
        self.lbl_entry.pack()

        self.nom_entry = ttk.Entry(self)
        self.nom_entry.pack()

        self.btn_valider = ttk.Button(self, text="Valider", command=self.update_nom)
        self.btn_valider.pack()
        
        self.lbl_nom = ttk.Label(self, text="")
        self.lbl_nom.pack()

        self.lbl_etat_systeme = ttk.Label(self, text="Entrez votre nom", background="blue")
        self.lbl_etat_systeme.pack()

        self.listbox_tentatives = tk.Listbox(self, width=75, height=15)
        self.listbox_tentatives.pack()

        self.btn_demarrer = ttk.Button(self, text="Entrer un code", state="disabled", command=self.rearmer_systeme)
        self.btn_demarrer.pack()

        self.btn_arreter = ttk.Button(self, text="Écrire tentative", state="disabled", command=self.ecrire_tentative)
        self.btn_arreter.pack()

    def update_nom(self):
        """Fonction qui permet de mettre a jour le label du nom lorsqu'il est non vide"""
        nom = self.nom_entry.get().strip()
        if nom:  
            self.lbl_nom["text"] = f"Bienvenue {nom} !"
            self.lbl_etat_systeme["text"] = f"Système prêt!"
            self.lbl_etat_systeme["background"]= "green"
            self.btn_demarrer["state"] = "normal" 
            s.write(b"afficher_nom\n")
            s.write((nom + "\n").encode())
        

# Les 2 fonctions ci dessous sont relié au label de l'état du système
    def rearmer_systeme(self):
        """Fonction qui permet de changer le label (couleur+texte) lorsque le bouton demarrer est appuyé"""
        s.write(b"rearmer_systeme\n")
        self.statut = "actif"
        self.lbl_etat_systeme["text"] = "Système en cours d'utilisation"
        self.lbl_etat_systeme["background"] = "red"
        self.btn_arreter["state"] = "normal"
        self.btn_demarrer["state"] = "disabled"
        s.write(b"allumer_led_rouge\n")
        
# Ecrire tentative btn
    def ecrire_tentative(self):
        """Fonction qui permet d'écrire la tentative dans la listbox"""
        s.write(b"ecrire_tentative\n")
        database.ajouter_bd()
        self.statut = "inactif"
        self.lbl_etat_systeme["text"] = "Système prêt"
        self.lbl_etat_systeme["background"] = "green"
        self.btn_arreter["state"] = "disabled"
        self.btn_demarrer["state"] = "normal"
        s.write(b"allumer_led_verte\n")
        s.write(b"tentatives\n")
        output = s.read_until().decode().strip()  # read_until() without arguments will read until there's nothing left to read
        tentatives = output.split("@")
        for tentative in tentatives:
            if not tentative.strip():  # the strip() function removes leading/trailing whitespace
                continue
            self.listbox_tentatives.insert(tk.END, tentative)

            noTentative = re.findall("#(\d+),", tentative)
            dateHeure = re.findall("Date-Heure: ([^,]*),", tentative)
            codeEntree = re.findall("Code Entrée: ([^,]*),", tentative)
            nom = re.findall("Nom: ([^,]*),", tentative)
            acces = re.findall("accès: (.*)", tentative)  # Change this regex to match everything after "accès: "

            if noTentative:
                noTentative = int(noTentative[0])  
            if dateHeure:
                dateHeure = dateHeure[0]  
            if codeEntree:
                codeEntree = int(codeEntree[0]) 
            if nom:
                nom = nom[0]  
            if acces:
                acces = acces[0]

            tentative_actuelle = Tentative(dateHeure, codeEntree, noTentative, nom, acces)
            database.ajouter_table(tentative_actuelle)




    def maj_lbl_bon(self):
        """MAJ label en fonction de l'état du système code correct"""
        s.write(b"fin_demarrage\n")
        self.lbl_etat_systeme["text"] = "Système prêt"
        self.lbl_etat_systeme["background"] = "green"



if __name__ == "__main__":
    app = Application()
    app.mainloop()
