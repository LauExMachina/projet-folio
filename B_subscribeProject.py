import paho.mqtt.client as mqtt
import os


def on_message(client, userdata, message):

    print(f"Message reçu : {message.payload.decode()} sur le topic {message.topic}\n")  #Afichage messages abonnement
    
    
broker = "localhost"                                                # Identification du broker
port = 1883

try:

    client = mqtt.Client("Subscriber")                              # Création de l'objet abonné

    client.on_message = on_message                                  # Configuration du callBack

    client.connect(broker, port)                                    # Connexion de l'abonné

    client.subscribe("home/temperature")                            # Subscription aux topics
    client.subscribe("home/humidite")

    client.loop_forever()

except Exception as f:                                              # Exceptions
        print(f"Erreur rencontrée : {f}")

except KeyboardInterrupt:
        print("Arrêt manuel du script")

except ConnectionError as e:
    print(f"Erreur de connexion détectée: {e}")


finally:
    client.disconnect()                                            # Déconnexion du client
    print("Abonné Déconnecté")
