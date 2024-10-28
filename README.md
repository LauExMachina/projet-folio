I Descriptif, II Notes importantes, III Détails du projet, IV En


# I Descriptif

**Système de Surveillance de Température**

Ce projet utilise un capteur de température pour surveiller les valeurs relevées et envoyer des alertes par e-mail en cas de dépassement des seuils définis. Il s'appuie sur Docker Compose pour orchestrer les services nécessaires, notamment un broker MQTT (Mosquitto) et un subscriber.

## Fichiers clés

- `docker-compose.yml` : Définit et orchestre les services Docker (capteur, Mosquitto, subscriber).
- `Dockerfile` : Définit les paramètres de l'image.
- `mosquitto.conf`: Fichier de configuration du broker utilisé dans la configuration Docker Compose.
- `capteur.py` : Script qui relève les données de température et publie sur le broker MQTT.
- `subscriber.py` : Souscrit aux messages MQTT du capteur et envoie des alertes par e-mail si les seuils de température sont dépassés.


## II Notes importantes

**Configuration msmtp** : 

Assurez-vous de configurer votre fichier msmtp.exemple, présent dans le répertoire projet du capteur. Si vous changez le nom du fichier, pensez à mettre à jour le Dockerfile en conséquence, afin que les emails d'alerte puissent être envoyés correctement.


- **Problème potentiel avec Mosquitto** :

  Si vous rencontrez l'erreur suivante :

  ```bash
  ERROR: for mosquitto_broker  Cannot start service mosquitto_broker: driver failed programming external connectivity on endpoint mosquitto_broker (40164ad98c9edf0fbcbec3e3dd279f85c59a70e345703bb365ce33ce4e87efdc): Error starting userland proxy: listen tcp4 0.0.0.0:1883: bind: address already in use
  ```

  Cela signifie que Mosquitto est déjà en cours d'exécution sur le port 1883. Pour résoudre ce problème :

  1. Arrêtez le service Mosquitto :
    
     ```bash
     sudo systemctl stop mosquitto
     ```

  2. Relancez Docker Compose :

     ```bash
     docker-compose up -d
     ```

- **Visualisation des logs** :

  Pour suivre les logs de l'ensemble des services, exécutez la commande suivante à la racine du projet :
  ```bash
  docker-compose logs -f
  ```

# III Détails du projet

Mon projet de Système de Surveillance Domotique est l'aboutissement théorique et pratique de près de trois ans d'études en autodidacte et en formation dans le domaine de la programmation. Ce projet est aussi un accomplissement personnel et une vitrine de ma compétence dans ce domaine.


**Objectif :**

Le but de ce projet est de créer un système de surveillance capable de mesurer la température et l'humidité d'une pièce de vie à intervalles réguliers. En cas de dépassement des seuils définis, le programme envoie des alertes par e-mail à partir d'une liste prédéfinie, active un signal lumineux, et enregistre les événements dans un fichier log. Les données sont consultables en temps réel via Node-RED. Les scripts sont écrits en Python et Bash, et sont déployés avec Docker. Les services sont ensuite orchestrés avec Docker Compose.


**Étapes du projet :**

1. Création de l'environnement :

   - Configuration d’un environnement virtuel Python sous Linux pour la création des scripts.

   - Installation des modules nécessaires pour le Raspberry Pi et le capteur DHT11.


2. Développement du script client :

   - Écriture d’un script Python pour lire les données du capteur DHT11 (température et humidité).

   - Relevé des données toutes les 10 secondes, avec gestion des exceptions en cas d'échec de lecture.

- Publication des données sur deux topics MQTT distincts : `home/temperature` et `home/humidite`.


3. Création du script abonné :

   - Développement d’un second script Python pour s'abonner aux topics via paho-mqtt et recevoir les informations envoyées par le capteur.


4. Implémentation d’une alerte :

   - Dans le script client, définition d’un seuil critique de température pour déclencher des actions en cas de dépassement :

  - Une LED clignote 5 fois pour signaler l'alerte.

  - Un mail unique est envoyé à une liste d’adresses contenue dans un fichier `.txt`, via un script Bash utilisant msmtp.

  - Horodatage : la date et l’heure de l’alerte sont enregistrées dans un fichier `.txt` (création automatique si le fichier n'existe pas).

  - Déconnexion du client MQTT.

  - Arrêt propre et automatique du programme.


5. Exportation des projets dans Docker :

   - Création d’images Docker pour les différents projets (client, abonné, broker).


6. Lancement des conteneurs via Docker Compose :

   - Utilisation de Docker Compose pour lancer simultanément les services.


7. Visualisation des données avec Node-RED :

   - Configuration d’un tableau de bord Node-RED pour afficher les données de température et d'humidité en temps réel, en utilisant l'outil   Chart pour visualiser les courbes.


**Perspectives et Scalabilité**

Bien que ce projet ait été réalisé avec un matériel minimal (Raspberry Pi, breadboard, LED, sonde), il est conçu pour être évolutif. D'autres capteurs ou composants pourraient être ajoutés sans difficulté, tel un avertisseur sonore, tant que le broker permet la gestion de clients supplémentaires.

Une base de données pourrais être implémenter aussi pour récupérer les données ou pour stocker les adresses email via SQLite.

**Note personnelle**

"Ce projet est le fruit de mon propre travail et de mes recherches dans le cadre de mon apprentissage du développement en domotique. Il reste quelques aspects que je continue à optimiser, ce qui reflète mon approche continue d'amélioration. Je suis toujours ouvert à des retours constructifs pour perfectionner mes compétences et mes projets."


# IV En

# Temperature Monitoring System

This project uses a temperature sensor to monitor recorded values and send email alerts if defined thresholds are exceeded. It relies on Docker Compose to orchestrate the necessary services, including an MQTT broker (Mosquitto) and a subscriber.

## Key Files

- `docker-compose.yml`: Defines and orchestrates the Docker services (sensor, Mosquitto, subscriber).
- `Dockerfile`: Defines the image settings.
- `mosquitto.conf`: Configuration file for the broker used in the Docker Compose setup.
- `capteur.py`: Script that reads temperature data and publishes it to the MQTT broker.
- `subscriber.py`: Subscribes to MQTT messages from the sensor and sends email alerts if temperature thresholds are exceeded.


## Important Notes

**msmtp Configuration**:

Ensure you configure your `msmtp.example` file, located in the sensor project's directory. If you change the file name, make sure to update the Dockerfile accordingly, so that alert emails can be sent properly.

- **Potential Issue with Mosquitto**:

  If you encounter the following error:

  ```bash
  ERROR: for mosquitto_broker  Cannot start service mosquitto_broker: driver failed programming external connectivity on endpoint mosquitto_broker (40164ad98c9edf0fbcbec3e3dd279f85c59a70e345703bb365ce33ce4e87efdc): Error starting userland proxy: listen tcp4 0.0.0.0:1883: bind: address already in use
  ```

  This means that Mosquitto is already running on port 1883. To resolve this issue:

  1. Stop the Mosquitto service:
    
     ```bash
     sudo systemctl stop mosquitto
     ```

  2. Restart Docker Compose:

     ```bash
     docker-compose up -d
     ```

- **Viewing Logs**:

  To follow the logs of all services, run the following command from the project root:
  ```bash
  docker-compose logs -f
  ```


# II. Project Details

My Home Automation Monitoring System project is the theoretical and practical culmination of nearly three years of self-taught study and training in the field of programming. This project is also a personal achievement and a showcase of my skills in this domain.


**Objective:**

The goal of this project is to create a monitoring system capable of measuring the temperature and humidity of a living space at regular intervals. If defined thresholds are exceeded, the program sends email alerts from a predefined list, activates a visual signal, and logs the events in a log file. The data can be viewed in real-time via Node-RED. The scripts are written in Python and Bash, and are deployed using Docker. The services are then orchestrated with Docker Compose.


**Project Steps:**

1. Environment Setup:

   - Configuring a virtual Python environment on Linux for script development.

   - Installing the necessary modules for the Raspberry Pi and the DHT11 sensor.

2. Client Script Development:

   - Writing a Python script to read data from the DHT11 sensor (temperature and humidity).

   - Collecting data every 10 seconds, with exception handling for read failures.

   - Publishing data to two separate MQTT topics: `home/temperature` and `home/humidity`.

3. Subscriber Script Creation:

   - Developing a second Python script to subscribe to the topics via paho-mqtt and receive the information sent by the sensor.

4. Alert Implementation:

   - In the client script, defining a critical temperature threshold to trigger actions if exceeded:

     - An LED blinks 5 times to signal the alert.

     - A unique email is sent to a list of addresses contained in a `.txt` file via a Bash script using msmtp.

     - Timestamp: the date and time of the alert are recorded in a `.txt` file (automatically created if the file does not exist).

     - MQTT client disconnection.

     - Clean and automatic shutdown of the program.

5. Exporting Projects to Docker:

   - Creating Docker images for the different projects (client, subscriber, broker).

6. Launching Containers via Docker Compose:

   - Using Docker Compose to simultaneously launch the services.

7. Data Visualization with Node-RED:

   - Setting up a Node-RED dashboard to display temperature and humidity data in real-time, using the Chart tool to visualize the graphs.


**Scalability and Future Prospects**

Although this project was built with minimal hardware (Raspberry Pi, breadboard, LED, sensor), it is designed to be scalable. Additional sensors or components, such as a sound alarm, could be added without difficulty as long as the broker can handle additional clients.

A database could also be implemented to collect the data or store email addresses using SQLite.


**Personal Note**

"This project is the result of my own work and research as part of my learning journey in home automation development. There are still a few aspects that I continue to optimize, reflecting my ongoing approach to improvement. I am always open to constructive feedback to enhance my skills and projects."