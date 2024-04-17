# GeoLocExif

<img width="1250" alt="2024-04-17_04-05-03" src="https://github.com/BreakingTechFr/GeolocExif/assets/128238555/a2fe54b0-d6cf-4473-885a-08bd839c6c53">

Ce programme permet de parcourir une photo, extraire les données GPS de ses métadonnées EXIF et ouvrir une carte Google Maps affichant l'emplacement géographique de la photo.

## Fonctionnalités

- Affichage des données Exif des images sélectionnées en *.jpg *.jpeg *.png *.gif
- Géolocalisation des images avec des informations GPS
- Sauvegarde des données Exif dans un fichier texte *.txt
- Sauvegarde une capture d'écran de la carte Google Maps affichant la géolocalisation en *.jpg

<img width="1250" alt="2024-04-17_04-05-35" src="https://github.com/BreakingTechFr/GeolocExif/assets/128238555/155ec1fe-a523-451c-ae9d-50bae5c27533">

## Prérequis

- Python 3.6
- Un gestionnaire de packages Python tel que pip
- Les bibliothèques Python répertoriées dans `requirements.txt`.

## Installation

1. Clonez ce dépôt :
```shell
git clone https://github.com/BreakingTechFr/GeolocExif.git
```

2. Accédez au répertoire du projet :
```shell
cd GeolocExif
```

4. Créez un environnement virtuel avec Python 3.6 :
```shell
python3.6 -m venv virtual3.6
```

3. Activez l'environnement virtuel avec Python 3.6 :
Activez l'environnement virtuel. Selon votre système d'exploitation, la commande peut varier :
Sur macOS et Linux :
cd virtual3.6
```shell
cd virtual3.6
```
```shell
source virtual3.6/bin/activate
```

Sur Windows (PowerShell) :
```shell
cd virtual3.6
```
```shell
.\virtual3.6\Scripts\Activate.ps1
```

4. Mettre a jour Pip :
```shell
pip install --upgrade pip
```

2. Installez les dépendances :
```shell
pip install -r requirements.txt
```

## Utilisation

Exécutez le script `geoexif.py` :
```shell
python geoexif.py
```

- Cliquez sur le bouton "Choisir une photo..." pour sélectionner une photo.
- Une fois la photo sélectionnée, cliquez sur le bouton "Geolocaliser" pour ouvrir une carte Google Maps montrant l'emplacement géographique de la photo.

## Auteur

[BreakingTech](https://github.com/BreakingTechFr)

