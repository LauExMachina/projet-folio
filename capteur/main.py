import paho.mqtt.client as mqtt # type: ignore 
import adafruit_dht             # type: ignore
import board                    # type: ignore
from datetime import datetime
import threading
import subprocess
import os
import signal

from led import led

# Client MQTT
client = mqtt.Client("Sonde")  # Création de l'objet client
broker = "mosquitto_broker"    # ou utilise "mosquitto_broker" pour Docker
port = 1883                   

dht_device = adafruit_dht.DHT11(board.D17, use_pulseio=False)    # Initialisation du capteur DHT11

stop_thread = False    # Variable globale pour contrôler l'arrêt du script
active_timers = []     # Liste des timers actifs pour un arrêt propre
lock = threading.Lock()  # Verrou pour protéger les accès concurrents

def sonde():
    try:
        client.connect(broker, port)  # Connexion du client MQTT
        print("Connexion réussie")

        def collect_and_publish():
            global stop_thread
            
            with lock:
                if stop_thread:  # Vérifie si le script doit s'arrêter
                    return

            try:
                temperature = dht_device.temperature    # Lecture des données du capteur
                humidity = dht_device.humidity

                if humidity is not None and temperature is not None:
                    print("Température ok\n", flush=True)
                    print(f"Données transmise aux abonnés température : {temperature:.1f}°C, humidité: {humidity:.1f}%\n")

                    client.publish(f"home/temperature", f"{temperature} °C")  
                    client.publish(f"home/humidite", f"{humidity} %")            

                    if temperature > 35:  # Choix de la température qui déclenchera l'alerte
                        alert()           # Appel de la fonction alert
               
                print("Patientez ...\n")

                # Redémarre le timer pour relancer la collecte après 10 secondes
                timer = threading.Timer(10, collect_and_publish)
                active_timers.append(timer)
                timer.start()

            except (RuntimeError, Exception) as e:
                print(f"Erreur lors de la lecture du capteur : {e}")
                timer = threading.Timer(10, collect_and_publish)
                active_timers.append(timer)
                timer.start()  # Relance après 10 secondes en cas d'erreur

        # Lance la collecte initiale
        print("Démarrage de la sonde...")
        collect_and_publish()

    except ConnectionError as e:
        print(f"Connexion impossible au broker : {e}")
    
    except KeyboardInterrupt:  # Interruption manuelle du script (ctrl + c)
        print("Script arrêté manuellement")
        stop_script()

def alert():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    print("Alerte !! Seuil de température dépassé\n")

    with open("logAlert.txt", mode="a") as file:
        file.write(f"Alerte température déclenchée le {current_time}, mails envoyés\n")

    print("Fichier log/Alert implémenté\n")

    subprocess.run(['bash', 'mailSender.sh'])
    print("Mail(s) d'alerte envoyé(s) aux Utilisateur(s)\n")

    led()  # Clignotement LED pour signaler l'alerte
    print("Arrêt automatique du programme par mesure de sécurité\n")

    stop_script()

def stop_script():
    global stop_thread
    
    with lock:
        stop_thread = True  # Empêche les timers de redémarrer
        
    # Arrêter et vider les timers actifs
    for timer in active_timers:
        timer.cancel()
    
    active_timers.clear()
    
    try:
        client.disconnect()    # Déconnexion propre du client MQTT
        print("Client déconnecté proprement\n")
    
    except Exception as e:
        print(f"Erreur lors de la déconnexion du client : {e}")

    print("Sortie du programme")
    os._exit(0)

# Gestion du signal d'interruption pour un arrêt propre
def signal_handler(sig, frame):
    print("Signal reçu, arrêt du script...")
    stop_script()

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    sonde()
