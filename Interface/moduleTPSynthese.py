class Tentative:
    def __init__(self, dateHeureTentative, code, noTentative, nom, acces):
        self.dateHeureTentative = dateHeureTentative
        self.code = code
        self.noTentative = noTentative
        self.nom = nom
        self.acces = acces # oui ou non
    # nom represente la personne qui tente d'entrer dans le systeme
    def __repr__(self):
         """Affiche tous les attributs de l'objet Tentative"""
         noTentative = self.noTentative + 1
         return f"#{noTentative}, Date-Heure: {self.dateHeureTentative}, Code Entrée: {self.code}, Nom: {self.nom}, acces: {self.acces}@"
    def AfficherCode(self):
        """Affiche les attributs un a la suite de l'autre, séparé par une virgule uniquement"""
        return f"{self.noTentative}, {self.dateHeureTentative}, {self.code}, {self.nom}, {self.acces}"