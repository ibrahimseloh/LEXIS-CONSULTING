# Utilisation de l'image Python officielle
FROM python:3.9-slim

# Mettre à jour apt et installer libgl1-mesa-glx
RUN apt-get update && apt-get install -y libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copier tous les fichiers du projet dans le conteneur
COPY . /app/

# Exposer le port pour Streamlit
EXPOSE 8501

# Définir la commande pour démarrer l'application Streamlit
CMD ["streamlit", "run", "main.py"]
