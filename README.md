# GeoLocExif

Ce programme permet de parcourir une photo, extraire les données GPS de ses métadonnées EXIF et ouvrir une carte Google Maps affichant l'emplacement géographique de la photo.

## Fonctionnalités

- Affichage des données Exif des images sélectionnées.
- Géolocalisation des images avec des informations GPS.
- Sauvegarde des données Exif dans un fichier texte.
- Capture d'écran de la carte Google Maps affichant la géolocalisation.

## Prérequis

- Python 3.6
- Un gestionnaire de packages Python tel que pip
- Les bibliothèques Python répertoriées dans `requirements.txt`.

## Installation

1. Clonez ce dépôt :
git clone https://github.com/BreakingTechFr/GeolocExif.git

2. Accédez au répertoire du projet :
cd GeolocExif

3. Créez un environnement virtuel avec Python 3.6 :
python3.6 -m venv virtual3.6

3. Activez l'environnement virtuel avec Python 3.6 :
Activez l'environnement virtuel. Selon votre système d'exploitation, la commande peut varier :
Sur macOS et Linux :
cd virtual3.9
source virtual3.9/bin/activate

Sur Windows (PowerShell) :
cd virtual3.9
.\virtual3.9\Scripts\Activate.ps1

4. Mettre a jour Pip :
pip install --upgrade pip

2. Installez les dépendances :
pip install -r requirements.txt

## Utilisation

Exécutez le script `geoexif.py` :
python geoexif.py

- Cliquez sur le bouton "Choisir une photo..." pour sélectionner une photo.
- Une fois la photo sélectionnée, cliquez sur le bouton "Geolocaliser" pour ouvrir une carte Google Maps montrant l'emplacement géographique de la photo.

## Auteur

[BreakingTech](https://github.com/BreakingTechFr)

