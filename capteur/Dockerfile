# Utiliser une image Python spécifique pour ARM 64
FROM arm64v8/python:3.9

WORKDIR /capteur

# Installer les dépendances nécessaires
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    apt-utils \
    python3 \
    python3-pip \
    msmtp \
    ca-certificates \
    build-essential \
    gcc \
    make \
    libgpiod-dev \
    mosquitto \
    mosquitto-clients \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Si nécessaire, créer le groupe 'gpio' avec le GID 993 et définir les permissions via udev
# Remplace *** par le bon GID pour le groupe gpio si nécessaire
# RUN groupadd -g 993 gpio && echo 'SUBSYSTEM=="gpio", GROUP="gpio", MODE="0660"' >> /etc/udev/rules.d/99-gpio.rules

# Copier les fichiers nécessaires dans le conteneur
COPY requirements.txt requirements.txt
COPY . /capteur
COPY .msmtprc.exemple /root/.msmtprc
RUN chmod 600 /root/.msmtprc

# Installer les dépendances Python
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Démarrer le script Python
ENTRYPOINT ["python3", "main.py"]
