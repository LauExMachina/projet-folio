import paho.mqtt.client as mqtt #type: ignore
import time
import os
import threading

# Subscriber

DELAI_INACTIVITE = 10  # Temps en secondes avant d'afficher "En attente de données"
dernier_message = time.time()  # Variable pour stocker l'heure du dernier message reçu

def on_connect(client, userdata, flags, rc):
    
    if rc == 0:
        print("✅ Connexion au broker réussie")
    else:
        print(f"❌ Échec de la connexion au broker (code retour : {rc})")

def on_disconnect(client, userdata, rc):
    
    print("⚠️ Déconnecté du broker")

def on_message(client, userdata, message):
    
    global dernier_message
    dernier_message = time.time()  # Mettre à jour l'heure du dernier message
    print(f"📩 Message reçu : {message.payload.decode()} sur le topic {message.topic}")

def verifier_inactivite():
    
    global dernier_message
    
    if time.time() - dernier_message > DELAI_INACTIVITE:
        
        print("⏳ En attente de données ...", flush=True)
        os.system('clear')   # Mettre à jour seulement si nécessaire pour éviter des appels inutiles à 'clear'
    
    threading.Timer(10, verifier_inactivite).start()  # Dans une boucle on va privilégier le Thread plutot que le sleep

def main():
    
    broker = "mosquitto_broker"  # Identification du broker
    port = 1883

    client = mqtt.Client("subscriber")  # Création de l'objet abonné

    try:
        # Association des callbacks à des fonctions pour personnaliser les réactions aux événements MQTT
        client.on_connect = on_connect        # Callback pour la connexion
        client.on_disconnect = on_disconnect  # Callback pour la déconnexion
        client.on_message = on_message        # Callback pour les messages

        client.connect(broker, port)  # Connexion de l'abonné

        client.subscribe("home/#", qos=1)  # Subscription aux topics via un wildcard

        client.loop_start()  # Lancer la boucle dans un thread séparé (non bloquant)

        verifier_inactivite()  # Lancer la surveillance de l'inactivité

    except Exception as e:
        print(f"❌ Erreur : {e}")

    except KeyboardInterrupt:
        print("🛑 Arrêt manuel du script")
        client.loop_stop()   # Arrêter la boucle MQTT
        client.disconnect()  # Déconnexion du client
        print("✅ Abonné Déconnecté proprement")

if __name__ == "__main__":
    main()
