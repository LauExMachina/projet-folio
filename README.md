Bonjour,


Le but de ce projet est d'alimenter mon portfolio de de présenter mes compétences, ceci est un système de surveillance capable de relever la température et l'humidité d'une pièce à vivre à intervalle régulier, d'envoyer des alertes mails, 
un signal lumineux et d’alimenter un fichier en cas de dépassement de seuil. Les données sont lisibles en temps réel via Node-Red. Il est conçu pour être un projet vitrine, d
émontrant les concepts fondamentaux de la domotique et de l'Internet des objets (IoT).

1. Création de l'environnement :

- Configuration d'un environnement virtuel Python sous Linux.

- Installation des dépendances nécessaires pour travailler avec un Raspberry Pi et le capteur DHT11.

2. Configuration du broker MQTT :

- Utilisation de Mosquitto pour distribuer les données vers plusieurs abonnés dans une topologie en étoile.

3. Développement du script client :

- Écriture de scripts Python pour lire les données d'un capteur de température et d'humidité du DHT11.

- Relevé des données toutes les 10 secondes avec gestion des exceptions pour traiter les échecs de lecture.

- Affichage des informations sur deux topics MQTT distincts : `home/temperature` et `home/humidity`.

4. Implémentation d'une alerte :

- Définition d'un seuil critique de température, en cas d'alerte :

- Une LED clignote 5 fois.

- Un mail unique est envoyé à partir d'une liste d'adresses contenues dans fichier .txt via un script bash msmtp.

- La date et l'heure de l'alerte est implémentée dans fichier .txt (création du fichier si non présent).

- Libération des GPIO

- Déconnexion du client

- Et pour finir,  l'arrêt complet automatique du programme.

5. Visualisation des données avec Node-RED :

- Configuration d'un tableau de bord avec Node-RED, en utilisant l'outil Chart pour afficher les courbes de température et d'humidité en temps réel.

- Les alertes sont également enregistrées dans un fichier `.txt`, avec l'heure et la date à chaque déclenchement.

6. Création du script abonné :

- Un second script Python est développé pour s'abonner aux topics MQTT et recevoir les informations.

- La fonction `on_message` est utilisée pour réagir aux messages envoyés par le broker.

  Merci.

7. Nettoyage des GPIO :

- Lorsque le script est arrêté manuellement une déconnexion client propre est effectuée, les GPIO sont libérés, un email d'alerte d'arrêt du programme est envoyé à des adresses choisies.

