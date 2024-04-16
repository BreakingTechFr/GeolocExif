import os
import sys
import threading
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog, QPushButton, QMessageBox, QStackedWidget, QTextEdit
from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtCore import Qt, QObject, Signal
from PySide2.QtWebEngineWidgets import QWebEngineView
import exifread
from GPSPhoto import gpsphoto

LARGEUR_FENETRE = 1200
HAUTEUR_FENETRE = 720
LARGEUR_BOUTON = 340
HAUTEUR_BOUTON = 50

class Signaux(QObject):
    afficher_donnees_exif_signal = Signal(str)

class Fenetre(QWidget):
    def __init__(self):
        super().__init__()
        self.chemin_fichier = ""
        self.setWindowTitle("BreakingTech GeoLocExif")
        self.setGeometry(300, 300, LARGEUR_FENETRE, HAUTEUR_FENETRE)
        self.principal_layout = QVBoxLayout()
        self.stacked_widget = QStackedWidget()
        self.principal_layout.addWidget(self.stacked_widget)
        self.setLayout(self.principal_layout)
        self.signaux = Signaux()
        self.signaux.afficher_donnees_exif_signal.connect(self.afficher_donnees_exif_event)
        self.creer_vue_principale()

    def creer_vue_principale(self):
        widget_principal = QWidget()
        layout = QVBoxLayout()  

        # Charger et appliquer l'icône de l'application
        chemin_icone = os.path.join(os.path.dirname(__file__), "icone.icns")
        icone_application = QIcon(chemin_icone)
        self.setWindowIcon(icone_application)

        self.lbl_logo = QLabel()
        chemin_image = os.path.join(os.path.dirname(__file__), "img", "geolocexif.jpg")
        self.lbl_logo.setPixmap(QPixmap(chemin_image))
        self.lbl_logo.setAlignment(Qt.AlignCenter)  
        self.lbl_image_selectionnee = QLabel()
        self.lbl_image_selectionnee.setAlignment(Qt.AlignCenter)
        self.txt_infos_exif = QTextEdit()
        self.txt_infos_exif.setStyleSheet("color: white;")
        self.txt_infos_exif.setReadOnly(True)
        self.btn_parcourir = QPushButton("Choisir une photo...")
        self.btn_parcourir.clicked.connect(self.parcourir)
        self.btn_parcourir.setStyleSheet("""
QPushButton {
    background-color: #4B4F52;
    color: white;
    border-radius: 5px;
}

QPushButton:hover {
    background-color: #868E96;
}
""")
        self.btn_parcourir.setFixedSize(LARGEUR_BOUTON, HAUTEUR_BOUTON)
        self.btn_parcourir.setObjectName("boutonParcourir")
        self.btn_rechercher = QPushButton("Geolocaliser")
        self.btn_rechercher.clicked.connect(self.geolocaliser)
        self.btn_rechercher.setFixedSize(LARGEUR_BOUTON, HAUTEUR_BOUTON)
        self.btn_quitter = QPushButton("Quitter")
        self.btn_quitter.clicked.connect(self.quitter_application)
        self.btn_quitter.setStyleSheet("""
QPushButton {
    background-color: #4B4F52;
    color: white;
    border-radius: 5px;
}

QPushButton:hover {
    background-color: #868E96;
}
""")
        self.btn_quitter.setFixedSize(LARGEUR_BOUTON, HAUTEUR_BOUTON)

        self.btn_sauvegarder = QPushButton("Sauvegarder les données")
        self.btn_sauvegarder.clicked.connect(self.sauvegarder_donnees)
        self.btn_sauvegarder.setFixedSize(LARGEUR_BOUTON, HAUTEUR_BOUTON)

        layout.addWidget(self.lbl_logo)
        
        layout_image = QHBoxLayout()
        layout_image.addWidget(self.txt_infos_exif)
        layout_image.addWidget(self.lbl_image_selectionnee)
        layout.addLayout(layout_image)

        layout_boutons = QHBoxLayout()
        layout_boutons.addWidget(self.btn_parcourir)
        layout_boutons.addSpacing(20)
        layout_boutons.addWidget(self.btn_rechercher)
        layout_boutons.addSpacing(20)
        layout_boutons.addWidget(self.btn_sauvegarder)
        layout_boutons.addSpacing(20)
        layout_boutons.addWidget(self.btn_quitter)
        layout.addLayout(layout_boutons)  
        widget_principal.setLayout(layout)
        self.stacked_widget.addWidget(widget_principal)
        self.setStyleSheet("background-color: black;")

        # Griser le bouton Geolocaliser
        self.btn_rechercher.setStyleSheet("background-color: #FFFFFF; color: #9F9FA0; border-radius: 5px;")
        self.btn_rechercher.setEnabled(False)
        self.btn_sauvegarder.setStyleSheet("background-color: #FFFFFF; color: #9F9FA0; border-radius: 5px;")
        self.btn_sauvegarder.setEnabled(False)

    def geolocaliser(self):
        if self.chemin_fichier == "":
            self.afficher_message_erreur("Veuillez d'abord parcourir une photo")
            return

        try:
            # Utiliser GPSPhoto pour récupérer les coordonnées GPS de l'image
            coords = gpsphoto.getGPSData(self.chemin_fichier)
            if not coords:
                self.afficher_message_erreur("Les coordonnées GPS ne sont pas disponibles pour cette image")
                return
            
            latitude = coords['Latitude']
            longitude = coords['Longitude']

            # Afficher les coordonnées sur la carte Google Maps
            widget_carte = QWidget()
            layout = QVBoxLayout()
            self.web_view = QWebEngineView()
            self.web_view.load(f"http://maps.google.com/?q={latitude},{longitude}")
            layout.addWidget(self.web_view)

            layout_boutons = QHBoxLayout()
            self.btn_retour = QPushButton("Retourner au menu")
            self.btn_retour.clicked.connect(self.afficher_vue_principale)
            self.btn_retour.setStyleSheet("""
QPushButton {
    background-color: #4B4F52;
    color: white;
    border-radius: 5px;
}

QPushButton:hover {
    background-color: #868E96;
}
""")
            self.btn_retour.setFixedSize(LARGEUR_BOUTON, HAUTEUR_BOUTON)
            layout_boutons.addWidget(self.btn_retour)
            layout_boutons.addSpacing(20)

            self.btn_screenshoot = QPushButton("Screenshoot GoogleMap")
            self.btn_screenshoot.clicked.connect(self.screenshoot_google_map)
            self.btn_screenshoot.setStyleSheet("""
QPushButton {
    background-color: #4B4F52;
    color: white;
    border-radius: 5px;
}

QPushButton:hover {
    background-color: #868E96;
}
""")
            self.btn_screenshoot.setFixedSize(LARGEUR_BOUTON, HAUTEUR_BOUTON)
            layout_boutons.addWidget(self.btn_screenshoot)

            self.btn_quitter = QPushButton("Quitter")
            self.btn_quitter.clicked.connect(self.quitter_application)
            self.btn_quitter.setStyleSheet("""
QPushButton {
    background-color: #4B4F52;
    color: white;
    border-radius: 5px;
}

QPushButton:hover {
    background-color: #868E96;
}
""")
            self.btn_quitter.setFixedSize(LARGEUR_BOUTON, HAUTEUR_BOUTON)
            layout_boutons.addWidget(self.btn_quitter)

            layout.addLayout(layout_boutons)

            widget_carte.setLayout(layout)
            self.stacked_widget.addWidget(widget_carte)
            self.stacked_widget.setCurrentWidget(widget_carte)
            widget_carte.setStyleSheet("background-color: black;")

        except Exception as e:
            self.afficher_message_erreur("Erreur lors de la récupération des données GPS de l'image")

    def screenshoot_google_map(self):
        if not hasattr(self, 'web_view'):
            return

        def capture_callback(image):
            file_path, _ = QFileDialog.getSaveFileName(self, "Enregistrer l'image", "", "Images (*.jpg)")
            if file_path:
                try:
                    image.save(file_path, "JPG")
                except Exception as e:
                    self.afficher_message_erreur("Une erreur s'est produite lors de l'enregistrement de la capture d'écran.")

        self.web_view.grab().toImage().save('screenshot.jpg')
        image = QPixmap('screenshot.jpg')
        capture_callback(image)

    def parcourir(self):
        dialogue_fichier = QFileDialog()
        dialogue_fichier.setFileMode(QFileDialog.ExistingFile)
        dialogue_fichier.setNameFilter("Images (*.jpeg *.jpg *.tiff *.tif *.raw)")
        
        if dialogue_fichier.exec_():
            fichiers_selectionnes = dialogue_fichier.selectedFiles()
            if not fichiers_selectionnes:
                return
            self.chemin_fichier = fichiers_selectionnes[0]
            image_selectionnee = QPixmap(self.chemin_fichier)
            if image_selectionnee.isNull():  # Vérifier si l'image n'a pas pu être chargée
                self.afficher_message_erreur("Erreur lors de l'importation de l'image.\nCette image n'est pas compatible avec le programme.")
                return
            self.afficher_donnees_exif()

    def recuperer_donnees_exif(self, chemin_image):
        with open(chemin_image, 'rb') as f:
            tags = exifread.process_file(f)
        # Filtrer les tags MakerNote
        tags_filtres = {tag: valeur for tag, valeur in tags.items() if "MakerNote" not in tag}
        return tags_filtres

    def afficher_donnees_exif(self):
        def afficher_donnees_thread():
            donnees_exif = self.recuperer_donnees_exif(self.chemin_fichier)
            infos_exif = ""
            # Groupes de données Exif
            groupes_exif = {
                "======== Image ========": [],
                "======== Appareil Photo ========": [],
                "======== GPS ========": [],
                "Autres": []
            }
            # Classification des tags Exif
            for tag, valeur in donnees_exif.items():
                if "MakerNote" not in tag:  # Ne pas inclure les tags MakerNote
                    if "Image" in tag:
                        groupes_exif["======== Image ========"].append(f"{self.traduire_propriete(tag)}: <font color='yellow'>{valeur}</font>\n")
                    elif "GPS" in tag:
                        groupes_exif["======== GPS ========"].append(f"{self.traduire_propriete(tag)}: <font color='yellow'>{valeur}</font>\n")
                    elif "EXIF" in tag:
                        groupes_exif["======== Appareil Photo ========"].append(f"{self.traduire_propriete(tag)}: <font color='yellow'>{valeur}</font>\n")
                    else:
                        groupes_exif["Autres"].append(f"{self.traduire_propriete(tag)}: <font color='yellow'>{valeur}</font>\n")
            # Concaténer les données de chaque groupe
            for titre_groupe, donnees_groupe in groupes_exif.items():
                if donnees_groupe:
                    infos_exif += f"<b>{titre_groupe}</b><br>"  # Utiliser <b> pour mettre en gras le titre du groupe
                    for donnee in donnees_groupe:
                        infos_exif += f"{donnee}<br>"  # Ajouter chaque propriété Exif avec un saut de ligne
                    infos_exif += "<br>"  # Ajouter un saut de ligne entre chaque groupe
            self.signaux.afficher_donnees_exif_signal.emit(infos_exif)

        threading.Thread(target=afficher_donnees_thread).start()

    def afficher_donnees_exif_event(self, infos_exif):
        self.txt_infos_exif.setHtml(infos_exif)
        image_selectionnee = QPixmap(self.chemin_fichier).scaled(300, 300, Qt.KeepAspectRatio)
        self.lbl_image_selectionnee.setPixmap(image_selectionnee)
        self.btn_rechercher.setEnabled(True)
        self.btn_sauvegarder.setEnabled(True)
        self.btn_rechercher.setStyleSheet("""
QPushButton {
    background-color: #4B4F52;
    color: white;
    border-radius: 5px;
}

QPushButton:hover {
    background-color: #868E96;
}
""")
        self.btn_sauvegarder.setStyleSheet("""
QPushButton {
    background-color: #4B4F52;
    color: white;
    border-radius: 5px;
}

QPushButton:hover {
    background-color: #868E96;
}
""")

    def afficher_message_erreur(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Erreur")
        msg_box.setText(message)
        msg_box.exec_()

    def traduire_propriete(self, tag):
        # Traduire les noms des propriétés Exif en français si nécessaire
        traductions = {
            "Image Make": "Fabricant de l'image",
            "Image Model": "Modèle de l'image",
            "Image Orientation": "Orientation de l'image",
            "Image XResolution": "Résolution X de l'image",
            "Image YResolution": "Résolution Y de l'image",
            "Image ResolutionUnit": "Unité de résolution de l'image",
            "Image Software": "Logiciel de l'image",
            "Image DateTime": "Date/Heure de l'image",
            "Image HostComputer": "Ordinateur Hôte de l'image",
            "Image TileWidth": "Largeur de la vignette de l'image",
            "Image TileLength": "Longueur de la vignette de l'image",
            "Image YCbCrPositioning": "Positionnement YCbCr de l'image",
            "Image ExifOffset": "Décalage Exif de l'image",
            "Image GPSInfo": "Infos GPS de l'image",
            "EXIF ExifImageWidth": "Largeur de l'image",
            "EXIF ExifImageLength": "Longueur de l'image",
            "Appareil Photo ExposureTime": "Temps d'exposition",
            "Appareil Photo FNumber": "Numéro F",
            "Appareil Photo ExposureProgram": "Programme d'exposition",
            "Appareil Photo ISOSpeedRatings": "Sensibilité ISO",
            "Appareil Photo ExifVersion": "Version Exif",
            "Appareil Photo DateTimeOriginal": "Date/Heure d'origine",
            "Appareil Photo DateTimeDigitized": "Date/Heure de numérisation",
            "Appareil Photo OffsetTime": "Décalage horaire",
            "Appareil Photo OffsetTimeOriginal": "Décalage horaire d'origine",
            "Appareil Photo OffsetTimeDigitized": "Décalage horaire de numérisation",
            "Appareil Photo ComponentsConfiguration": "Configuration des composants",
            "Appareil Photo ShutterSpeedValue": "Vitesse d'obturation",
            "Appareil Photo ApertureValue": "Valeur d'ouverture",
            "Appareil Photo BrightnessValue": "Valeur de luminosité",
            "Appareil Photo ExposureBiasValue": "Compensation d'exposition",
            "Appareil Photo MeteringMode": "Mode de mesure",
            "Appareil Photo Flash": "Flash",
            "Appareil Photo FocalLength": "Longueur focale",
            "Appareil Photo SubjectArea": "Zone de sujet",
            "Appareil Photo SubSecTimeOriginal": "Temps SubSec d'origine",
            "Appareil Photo SubSecTimeDigitized": "Temps SubSec de numérisation",
            "Appareil Photo FlashPixVersion": "Version FlashPix",
            "Appareil Photo ColorSpace": "Espace colorimétrique",
            "Appareil Photo SensingMethod": "Méthode de détection",
            "Appareil Photo SceneType": "Type de scène",
            "Appareil Photo ExposureMode": "Mode d'exposition",
            "Appareil Photo WhiteBalance": "Balance des blancs",
            "Appareil Photo FocalLengthIn35mmFilm": "Longueur focale en 35mm",
            "Appareil Photo SceneCaptureType": "Type de capture de scène",
            "Appareil Photo LensSpecification": "Spécification de l'objectif",
            "Appareil Photo LensMake": "Fabricant de l'objectif",
            "Appareil Photo LensModel": "Modèle de l'objectif",
            "Appareil Photo Tag 0xA460": "Tag 0xA460",
            "GPS GPSLatitudeRef": "Référence de latitude",
            "GPS GPSLatitude": "Latitude",
            "GPS GPSLongitudeRef": "Référence de longitude",
            "GPS GPSLongitude": "Longitude GPS",
            "GPS GPSAltitudeRef": "Référence d'altitude",
            "GPS GPSAltitude": "Altitude GPS",
            "GPS GPSSpeedRef": "Référence de vitesse",
            "GPS GPSSpeed": "Vitesse GPS",
            "GPS GPSImgDirectionRef": "Référence de direction d'image",
            "GPS GPSImgDirection": "Direction d'image",
            "GPS GPSDestBearingRef": "Référence de cap de destination",
            "GPS GPSDestBearing": "Cap de destination",
            "GPS Tag 0x001F": "Tag 0x001F",
            "GPS GPSDate": "Date GPS",
            "GPS GPSTimeStamp":"Horodatage",
            "EXIF ExposureTime": "Temps d'exposition",
            "EXIF FNumber": "Numéro F",
            "EXIF ExposureProgram": "Programme d'exposition",
            "EXIF ISOSpeedRatings": "Valeurs de sensibilité ISO",
            "EXIF ExifVersion": "Version Exif",
            "EXIF DateTimeOriginal": "Date/Heure d'origine",
            "EXIF DateTimeDigitized": "Date/Heure de numérisation",
            "EXIF OffsetTime": "Heure de décalage",
            "EXIF OffsetTimeOriginal": "Heure de décalage d'origine",
            "EXIF OffsetTimeDigitized": "Heure de décalage de numérisation",
            "EXIF ComponentsConfiguration": "Configuration de composants",
            "EXIF ShutterSpeedValue": "Valeur de vitesse d'obturation",
            "EXIF ApertureValue": "Valeur d'ouverture",
            "EXIF BrightnessValue": "Valeur de luminosité",
            "EXIF ExposureBiasValue": "Valeur de correction d'exposition",
            "EXIF MeteringMode": "Mode de mesure",
            "EXIF Flash": "Flash",
            "EXIF FocalLength": "Longueur focale",
            "EXIF SubjectArea": "Zone sujet",
            "EXIF SubSecTimeOriginal": "Sous-seconde d'origine",
            "EXIF SubSecTimeDigitized": "Sous-seconde de numérisation",
            "EXIF FlashPixVersion": "Version FlashPix",
            "EXIF ColorSpace": "Espace couleur",
            "EXIF SensingMethod": "Méthode de détection",
            "EXIF SceneType": "Type de scène",
            "EXIF ExposureMode": "Mode d'exposition",
            "EXIF WhiteBalance": "Balance des blancs",
            "EXIF FocalLengthIn35mmFilm": "Longueur focale en film 35 mm",
            "EXIF SceneCaptureType": "Type de capture de scène",
            "EXIF LensSpecification": "Spécification de l'objectif",
            "EXIF LensMake": "Fabricant de l'objectif",
            "EXIF LensModel": "Modèle de l'objectif",
            "EXIF Tag 0xA460": "Tag 0xA460",
        }
        return traductions.get(tag, tag)

    def sauvegarder_donnees(self):
        if self.chemin_fichier == "":
            self.afficher_message_erreur("Veuillez d'abord parcourir une photo")
            return

        try:
            # Demander à l'utilisateur l'emplacement de sauvegarde
            chemin_fichier_sauvegarde, _ = QFileDialog.getSaveFileName(self, "Enregistrer les données Exif", "", "Fichiers texte (*.txt)")

            if chemin_fichier_sauvegarde:
                # Sauvegarder les données Exif dans un fichier texte
                donnees_exif = self.recuperer_donnees_exif(self.chemin_fichier)
                with open(chemin_fichier_sauvegarde, 'w') as f:
                    for tag, valeur in donnees_exif.items():
                        tag_fr = self.traduire_propriete(tag)  # Traduire le tag en français
                        f.write(f"{tag_fr}: {valeur}\n")

        except Exception as e:
            self.afficher_message_erreur("Une erreur s'est produite lors de la sauvegarde des données Exif")

    def afficher_message_information(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Information")
        msg_box.setText(message)
        msg_box.exec_()

    def afficher_vue_principale(self):
        self.stacked_widget.setCurrentIndex(0)

    def quitter_application(self):
        sys.exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = Fenetre()
    fenetre.show()
    sys.exit(app.exec_())
