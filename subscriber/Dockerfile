# Utiliser une image Python spécifique pour ARM
FROM arm64v8/python:3.9

WORKDIR /subscribe

# Installer les dépendances nécessaires
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    apt-utils \
    msmtp \
    ca-certificates \
    build-essential \
    gcc \
    make \
    mosquitto \
    mosquitto-clients \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers nécessaires dans le conteneur
COPY requirements.txt requirements.txt
COPY . /subscribe

# Installer les dépendances Python
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Exécuter directement le script Python
ENTRYPOINT ["python3", "main.py"]
