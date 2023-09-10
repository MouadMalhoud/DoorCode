import unittest
from moduleTPSynthese import Tentative


class TestTentative(unittest.TestCase):
# création tentative
    def creer_tentative(self):
        self.tentative = Tentative("2023-05-19 22:30:00", 1234, 0, "mouad", "autorisé")
#1
    def test_repr(self):
        self.creer_tentative()
        expected = "#1, Date-Heure: 2023-05-19 22:30:00, Code Entrée: 1234, Nom: mouad, acces: autorisé@"
        self.assertEqual(self.tentative.__repr__(), expected)
#2
    def test_AfficherCode(self):
        self.creer_tentative()
        expected = "0, 2023-05-19 22:30:00, 1234, mouad, autorisé"
        self.assertEqual(self.tentative.AfficherCode(), expected)

#3
    def test_code_incorrect(self):
        """Fonction qui teste si le code erroné n'a pas l'accès autorisé"""
        self.creer_tentative()
        self.tentative.code = 4321
        if self.tentative.code != 1234:
            self.assertFalse(self.tentative.acces != "autorisé")



if __name__ == '__main__':
    unittest.main()