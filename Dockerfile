# Utiliser une image officielle de Python comme base
FROM python:3.12-slim

# Créer un répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt pour installer les dépendances
COPY requirements.txt .

# Installer les dépendances à partir de requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Le reste sera monté par Docker Compose, donc pas besoin de copier les fichiers du projet ici
CMD ["python"]
