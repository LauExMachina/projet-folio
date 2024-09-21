import paho.mqtt.client as mqtt
import adafruit_dht
import board
import time
import RPi.GPIO as GPIO
import subprocess
import os
import sys

from timing import timing                               # Module personnel importé
from led import led

timer = timing()
moment_now = (f" à {timer[3]}H{timer[4]}, le {timer[2]}/{timer[1]}/{timer[0]}")


def start_broker():                                     # Fonction démarrage du script                              

    try:
 
        subprocess.Popen(['bash', 'mosquitto'])         # Subprocess.Popen pour ne pas bloquer le programme
        
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution du script: {e}")




def sonde():

    sonde = adafruit_dht.DHT11(board.D18)               # Création de l'objet sonde

    broker = "localhost"                                # Renseigne le broker
    port = 1883

    client = mqtt.Client("Sonde")                       # Création de l'objet client
   

    try:                                                # Tentative de connexion
        
        client.connect(broker, port)                    # Connexion du client en dehors du while pour éviter la redondance de connexion
        print("Connexion réussie")
         
        mail_count = 0                                  # Variable qui va stocker le nombre de tour de boucle du while
        
        while True:                                     # Départ de la boucle de collecte et publication des données de la sonde
            
            try:

                temp = sonde.temperature                # Données de type float (penser à convertir au besoin)
                humidity = sonde.humidity

                if temp is not None and humidity is not None:

                    client.publish(f"home/temperature", temp)      # Publication des résultats sur topic
                    client.publish(f"home/humidite", humidity)

                    print("Température ok\n")

                    print(f"Données transmise aux abonnés température : {temp}°C, humidité: {humidity}%")  #Message transmis aux abonnés
                

                    time.sleep(5)                       # Laps de temps de 10 secondes entres les mesures
                    
                    os.system('clear')                  # Effacement de la console pour un confort visuel de la console

                    if temp > 0:                       # Choix de la température qui déclenchera l'alerte
                        
                        alert()                         # Appel de la fonction alert, on renseigne les arguments

                        mail_count += 1                 # Incrémantation de 1; le count étant à 1 plus de mail ne sera envoyé (spamimng)
                    
                    
                    yield temp, humidity                # Récupération des données pour traitement interne, ici yield plutôt que return pour ne pas casse la boucle

                else:
                    print("Données indisponibles")
                    time.sleep(5)                       # Petit laps de temps supplémentaire pour la sonde
            
            except Exception as f:
                 print(f"Problème detecté {f}")

    except ConnectionError as e:
        print(f"Connexion impossible au broker : {e}")

    except KeyboardInterrupt:                               # Intérruption manuelle du script (ctrl + c)
        print(f"Script arrété manuellement")

    finally:

        try:
        
            if mail_count == 0:                                #Pour éviter de spamer, un envoi de 1 mail par alerte (compte fait en amont suivre le paramètre)
            
                subprocess.run(['bash', 'mailSender.sh'])      
                
                print("Mail(s) d'alerte envoyé(s) aux Utilisateur(s)\n")

            else:
                print("Email(s) déjà envoyé(s)\n")                # Dans le cas où un mail à déjà été envoyé

        except Exception as e:
            print(f"Erreur : {e}")
        
        client.disconnect()                                 #Déconnection du client et nettoyage du pin
        print("Client déconnecté\n")
        
        GPIO.cleanup()                                      # Gpio remis en postion neutre (Input, down)
        print("Gpio néttoyés\n")





def alert():                                                # Fonction déclenchement d'alerte
    
    print("Alerte !! Seuil de température dépassé\n")
   

    with open ("logAlert.txt", mode="a") as file:           # Création du fichier si il n'existe pas, mode a pour ne pas écraser les données présentes
        
        file.write(f"Alerte température déclenchée {moment_now}, mails envoyés\n")    # Texte avec heure et date du moment    
    
    led()                                                   # Envoi du script du clignottement de la led pour l'aspect visuel
    
    print("Arrêt automatique du programme par mesure de sécurité\n")
    

    sys.exit(1)                                             # Arrêt brutal du programme par mesure de sécurité (choix os plutôt que syst dans ce cas)
                                                            # Penser à libéré le GPIO après cela
   

    

if __name__ == "__main__":

    print("Patientez ...\n")

    #start_broker()  #La désactivation est voulue ici, implémenté pour servir d'exemple
    
    for temperature, humidity in sonde():                                           # itérerer sur le générateur pour récupérer les valeurs
       
       '''
       Dans le cas où je souhaite faire quelque chose avec ces données,
       comme des calculs de moyennes ou autres manipulations mathématiques
       '''
       pass
    