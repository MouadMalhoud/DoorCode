from machine import Pin, I2C, PWM
import I2C_LCD
from keypad import KeyPad
from time import sleep
import sys
import utime
from moduleTPSynthese import Tentative



#import database as database

####################################
CODE = "1234"
####################################


#Déclaration du module et de l'objet
i2c= I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0] # scan adresse de connexion
lcd = I2C_LCD.I2CLcd(i2c, I2C_ADDR, 2, 16)
#Déclaration led
led_verte = Pin(2, Pin.OUT)
led_rouge = Pin(3, Pin.OUT)
#Déclaration keypad
keyPad = KeyPad(13, 12, 11, 10, 9, 8, 7, 6)
#Déclaration du buzzer
buzzer = PWM(Pin(15))
buzzer.freq(500)
#Déclaration bouton validation
btn_valider = Pin(27, Pin.IN, Pin.PULL_UP)

def allumer_buzzer():
    """Fonction qui permet d'allumer le buzzer - bruit alarme"""
    buzzer.duty_u16(1000)

def eteindre_buzzer():
    """Fonction qui permet d'eteindre le buzzer"""
    buzzer.duty_u16(0)

def clignoter_led(led):
    """Fonction qui fait clignoter 3x la led recu en param."""
    #allumer_buzzer()
    for i in range(4):
        allumer_buzzer()
        led.on()
        sleep(0.25)
        led.off()
        sleep(0.25)
    eteindre_buzzer()

def allumer_led_verte():
    led_verte.on()
    led_rouge.off()

def allumer_led_rouge():
    led_verte.off()
    led_rouge.on()
    #allumer_buzzer()
    sleep(2.5)
    #eteindre_buzzer()

sons = {
"E5": 659,
"G5": 784,
"B5": 988,
"A5": 880
}

musique = ["E5","G5","B5","A5","E5","G5","B5","A5","P"]

journal = [] # Collection pour toutes les tentatives
noTentative = 0

def jouer_son(freq):
    buzzer.duty_u16(1000)
    buzzer.freq(freq)

def musique_acces(musique):
    """Fonction qui permet de jouer une melodie lorsque le code de l'alarme est valide"""
    for i in range(len(musique)):
        if (musique[i] == "P"):
            eteindre_buzzer()
        else:
            jouer_son(sons[musique[i]])
        sleep(0.3)
    eteindre_buzzer()

def afficher_message(msg):
    """Fonction qui me permet de clear et d'afficher un message dans l'ecran lcd"""
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr(msg)

def entrer_code():
    """Fonction qui permet d'entrer le code"""
    led_rouge.value(1)
    code = ""
    afficher_message("Entrez le code  (4):  ")
    while len(code) < 4 :
        key = keyPad.scan()  
        sleep(0.1)
        if key is not None: 
            code += str(key) 
            afficher_message("Entrez le code  (4): "+ code)
            while keyPad.scan() is not None: 
                pass
        sleep(0.1)  
    while not btn_valider.value() == 0: 
        pass
    while not btn_valider.value() == 1: 
        pass
    return code

code_valide = False

def verifier_code(code):
    """Fonction qui permet de verifier que le code est bon
        Si bon -> Fait une musique et allume led verte
        Si mauvais -> Fait un bruit d'erreur et allume led rouge
    """
    global noTentative
    if code == CODE: # Code valide
        led_verte.value(1)
        led_rouge.value(0)
        musique_acces(musique)
        lcd.clear()
        afficher_message("Acces autorise")
        sleep(2)
        led_verte.value(0)
        return True
    else: # Code invalide
        led_verte.value(0)
        clignoter_led(led_rouge)
        lcd.clear()
        afficher_message("Acces refuse")
        sleep(2)
        
def format_time():
    """Permet de formatté la date (mieux lisible)"""
    local_time = utime.localtime()
    year = local_time[0]
    month = local_time[1]
    day = local_time[2]
    hour = local_time[3]
    minute = local_time[4]
    second = local_time[5]
    temps_format = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(year, month, day, hour, minute, second)
    return temps_format
led_rouge.value(1)
afficher_message("Code d'acces    porte niveau 3")
nom = ""

while True:
    led_verte.value(0)
    led_rouge.value(1)
    commande = sys.stdin.readline().strip()
    if commande == "allumer_led_verte":
        allumer_led_verte()
    elif commande == "allumer_led_rouge":
        allumer_led_rouge()
    elif commande == "afficher_nom":
        nom = sys.stdin.readline().strip()
        afficher_message("Bonjour: " + nom)
        sleep(2.5)
        afficher_message("Code d'acces    porte niveau 3")
    elif commande == "rearmer_systeme": # Démarrage systeme protection
        #led_rouge.value(0)
        #led_verte.value(1)

        code = entrer_code()
        ouvert = verifier_code(code)
        if ouvert:
            afficher_message("Ouverture!")
            led_verte.on()
            acces="autorisé"
            t = Tentative(format_time(), code, noTentative, nom, acces)
            journal.append(t)
            #database.ajouter_table(t)
            noTentative += 1
            sleep(3)
            #commande = "maj_lbl_bon"
            #sleep(0.1)
            #commande = "desactiver_systeme"
        else:
            acces="échoué"
            t = Tentative(format_time(), code, noTentative, nom, acces)
            journal.append(t)
            #database.ajouter_table(t)
            noTentative += 1
            pass
    elif commande == "ecrire_tentative": # ecrit la tentative dans la listbox 
        #led_rouge.value(1)
        #led_verte.value(0)
        afficher_message("Sys. de securite est inactif.")
    elif commande == "tentatives":
        for tentative in journal:
            print(journal[noTentative-1])
