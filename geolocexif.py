import os
import sys
import threading
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog, QPushButton, QMessageBox, QStackedWidget, QTextEdit
from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtCore import Qt, QObject, Signal
from PySide2.QtWebEngineWidgets import QWebEngineView
import exifread
from GPSPhoto import gpsphoto
from pyautogui import screenshot

LARGEUR_FENETRE = 1250
HAUTEUR_FENETRE = 670
LARGEUR_BOUTON = 340
HAUTEUR_BOUTON = 50

class Signaux(QObject):
    afficher_donnees_exif_signal = Signal(str)

class Fenetre(QWidget):
    def __init__(self):
        super().__init__()
        self.chemin_fichier = ""
        self.setWindowTitle("BreakingTech GeoLocExif")
        self.setGeometry(200, 200, LARGEUR_FENETRE, HAUTEUR_FENETRE)
        self.principal_layout = QVBoxLayout()
        self.principal_layout.setAlignment(Qt.AlignCenter)  # Centrer les éléments horizontalement
        self.stacked_widget = QStackedWidget()
        self.principal_layout.addWidget(self.stacked_widget)
        self.setLayout(self.principal_layout)
        self.signaux = Signaux()
        self.creer_vue_principale()

    def creer_vue_principale(self):
        widget_principal = QWidget()
        layout_principal = QVBoxLayout()

        layout_haut = QHBoxLayout()

        # Logo geolocexif.jpg à gauche
        logo_layout = QVBoxLayout()
        logo_label = QLabel()
        logo_pixmap = QPixmap("geolocexif.jpg")
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(logo_label)
        layout_haut.addLayout(logo_layout)

        # Image importée par l'utilisateur à droite du logo
        self.lbl_image_selectionnee = QLabel()
        layout_haut.addWidget(self.lbl_image_selectionnee)

        layout_boutons = QVBoxLayout()

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
        layout_boutons.addWidget(self.btn_parcourir)

        self.btn_geolocaliser = QPushButton("Géolocaliser")
        self.btn_geolocaliser.clicked.connect(self.geolocaliser)
        self.btn_geolocaliser.setFixedSize(LARGEUR_BOUTON, HAUTEUR_BOUTON)
        layout_boutons.addWidget(self.btn_geolocaliser)
        self.btn_geolocaliser.setEnabled(False)
        if not self.chemin_fichier:
            self.btn_geolocaliser.setStyleSheet("""
QPushButton {
    background-color: #FFFFFF;
    color: #9F9FA0;
    border-radius: 5px;
}
""")
        
        self.btn_sauvegarder = QPushButton("Sauvegarder les données")
        self.btn_sauvegarder.clicked.connect(self.sauvegarder_donnees)
        self.btn_sauvegarder.setFixedSize(LARGEUR_BOUTON, HAUTEUR_BOUTON)
        layout_boutons.addWidget(self.btn_sauvegarder)
        self.btn_sauvegarder.setEnabled(False)
        if not self.chemin_fichier:
            self.btn_sauvegarder.setStyleSheet("""
QPushButton {
    background-color: #FFFFFF;
    color: #9F9FA0;
    border-radius: 5px;
}
""")

        self.btn_quitter = QPushButton("Quitter")
        self.btn_quitter.clicked.connect(self.quitter_application)
        self.btn_quitter.setStyleSheet("""
QPushButton {
    background-color: #C92A2A;
    color: white;
    border-radius: 5px;
}

QPushButton:hover {
    background-color: #F03E3E;
}
""")
        self.btn_quitter.setFixedSize(LARGEUR_BOUTON, HAUTEUR_BOUTON)
        layout_boutons.addWidget(self.btn_quitter)

        layout_haut.addLayout(layout_boutons)
        layout_haut.addStretch()  # Ajouter de l'espace à droite
        layout_principal.addLayout(layout_haut)

        self.txt_infos_exif_col1 = QTextEdit()
        self.txt_infos_exif_col1.setStyleSheet("color: white;")
        self.txt_infos_exif_col1.setReadOnly(True)
        self.txt_infos_exif_col2 = QTextEdit()
        self.txt_infos_exif_col2.setStyleSheet("color: white;")
        self.txt_infos_exif_col2.setReadOnly(True)
        self.txt_infos_exif_col3 = QTextEdit()
        self.txt_infos_exif_col3.setStyleSheet("color: white;")
        self.txt_infos_exif_col3.setReadOnly(True)
        self.txt_infos_exif_col4 = QTextEdit()
        self.txt_infos_exif_col4.setStyleSheet("color: white;")
        self.txt_infos_exif_col4.setReadOnly(True)

        layout_donnees_exif = QHBoxLayout()

        layout_col1 = QVBoxLayout()
        self.label_group1 = QLabel("Informations sur l'image", alignment=Qt.AlignCenter)
        self.label_group1.setStyleSheet("color: white;")
        layout_col1.addWidget(self.label_group1)
        layout_col1.addWidget(self.txt_infos_exif_col1)
        layout_donnees_exif.addLayout(layout_col1)

        layout_col2 = QVBoxLayout()
        self.label_group2 = QLabel("Réglages de l'appareil photo", alignment=Qt.AlignCenter)
        self.label_group2.setStyleSheet("color: white;")
        layout_col2.addWidget(self.label_group2)
        layout_col2.addWidget(self.txt_infos_exif_col2)
        layout_donnees_exif.addLayout(layout_col2)

        layout_col3 = QVBoxLayout()
        self.label_group3 = QLabel("Données temporelles", alignment=Qt.AlignCenter)
        self.label_group3.setStyleSheet("color: white;")
        layout_col3.addWidget(self.label_group3)
        layout_col3.addWidget(self.txt_infos_exif_col3)
        layout_donnees_exif.addLayout(layout_col3)

        layout_col4 = QVBoxLayout()
        self.label_group4 = QLabel("Géolocalisation", alignment=Qt.AlignCenter)
        self.label_group4.setStyleSheet("color: white;")
        layout_col4.addWidget(self.label_group4)
        layout_col4.addWidget(self.txt_infos_exif_col4)
        layout_donnees_exif.addLayout(layout_col4)

        layout_principal.addLayout(layout_donnees_exif)

        widget_principal.setLayout(layout_principal)
        self.stacked_widget.addWidget(widget_principal)
        self.setStyleSheet("background-color: black;")

    def geolocaliser(self):
        if self.chemin_fichier == "":
            self.afficher_message_erreur("Veuillez d'abord parcourir une photo")
            return

        try:
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

            self.btn_screenshot = QPushButton("Screenshot GoogleMap")
            self.btn_screenshot.clicked.connect(self.screenshot_googlemap)
            self.btn_screenshot.setStyleSheet("""
QPushButton {
    background-color: #099268;
    color: white;
    border-radius: 5px;
}

QPushButton:hover {
    background-color: #20C997;
}
""")
            self.btn_screenshot.setFixedSize(LARGEUR_BOUTON, HAUTEUR_BOUTON)
            layout_boutons.addWidget(self.btn_screenshot)

            self.btn_quitter_carte = QPushButton("Quitter")
            self.btn_quitter_carte.clicked.connect(self.quitter_application)
            self.btn_quitter_carte.setStyleSheet("""
QPushButton {
    background-color: #C92A2A;
    color: white;
    border-radius: 5px;
}

QPushButton:hover {
    background-color: #F03E3E;
}
""")
            self.btn_quitter_carte.setFixedSize(LARGEUR_BOUTON, HAUTEUR_BOUTON)
            layout_boutons.addWidget(self.btn_quitter_carte)

            layout.addLayout(layout_boutons)
            widget_carte.setLayout(layout)
            self.stacked_widget.addWidget(widget_carte)
            self.stacked_widget.setCurrentWidget(widget_carte)
        except Exception as e:
            self.afficher_message_erreur(str(e))

    def screenshot_googlemap(self):
        save_path, _ = QFileDialog.getSaveFileName(self, "Enregistrer le screenshot", "", "JPEG Files (*.jpg)")
        if save_path:
            self.web_view.grab().save(save_path, "jpg")

    def afficher_vue_principale(self):
        self.stacked_widget.setCurrentIndex(0)

    def afficher_message_erreur(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Erreur")
        msg.setInformativeText(message)
        msg.setWindowTitle("Erreur")
        msg.exec_()

    def quitter_application(self):
        sys.exit()

    def sauvegarder_donnees(self):
        if self.chemin_fichier == "":
            self.afficher_message_erreur("Veuillez d'abord parcourir une photo")
            return

        nom_fichier = os.path.basename(self.chemin_fichier)
        nom_fichier_sans_extension = os.path.splitext(nom_fichier)[0]
        nom_fichier_donnees = f"{nom_fichier_sans_extension}_donnees_exif.txt"
        
        save_path, _ = QFileDialog.getSaveFileName(self, "Enregistrer les données Exif", nom_fichier_donnees, "Text Files (*.txt)")

        if save_path:
            chemin_sauvegarde = save_path

            try:
                with open(chemin_sauvegarde, "w") as f:
                    f.write(self.txt_infos_exif_col1.toPlainText() + "\n")
                    f.write(self.txt_infos_exif_col2.toPlainText() + "\n")
                    f.write(self.txt_infos_exif_col3.toPlainText() + "\n")
                    f.write(self.txt_infos_exif_col4.toPlainText() + "\n")
                self.afficher_message_information("Données Exif sauvegardées avec succès")
            except Exception as e:
                self.afficher_message_erreur(str(e))

    def parcourir(self):
        chemin_fichier, _ = QFileDialog.getOpenFileName(self, "Choisir une photo", "", "Images (*.jpg *.jpeg *.png *.gif)")
        if chemin_fichier:
            self.chemin_fichier = chemin_fichier
            self.afficher_image()
            self.effacer_donnees_exif()
            threading.Thread(target=self.afficher_donnees_exif).start()
            self.btn_geolocaliser.setEnabled(True)
            self.btn_geolocaliser.setStyleSheet("""
QPushButton {
    background-color: #1971C2;
    color: white;
    border-radius: 5px;
}

QPushButton:hover {
    background-color: #228BE6;
}
""")
            self.btn_sauvegarder.setEnabled(True)
            self.btn_sauvegarder.setStyleSheet("""
QPushButton {
    background-color: #099268;
    color: white;
    border-radius: 5px;
}

QPushButton:hover {
    background-color: #20C997;
}
""")

    def afficher_image(self):
        pixmap = QPixmap(self.chemin_fichier)
        if pixmap.width() > 200:
            pixmap = pixmap.scaledToWidth(200, Qt.SmoothTransformation)
        self.lbl_image_selectionnee.setPixmap(pixmap)
        self.lbl_image_selectionnee.setAlignment(Qt.AlignCenter)

    def afficher_message_information(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Information")
        msg.setInformativeText(message)
        msg.setWindowTitle("Information")
        msg.exec_()

    def effacer_donnees_exif(self):
        self.txt_infos_exif_col1.clear()
        self.txt_infos_exif_col2.clear()
        self.txt_infos_exif_col3.clear()
        self.txt_infos_exif_col4.clear()

    def afficher_donnees_exif(self):
        donnees_exif = self.recuperer_donnees_exif(self.chemin_fichier)
        groupes_exif = {
            "Informations sur l'image": [],
            "Réglages de l'appareil photo": [],
            "Données temporelles": [],
            "Géolocalisation": []
        }
        for tag, valeur in donnees_exif.items():
            if "MakerNote" not in tag:
                if "Image" in tag:
                    groupes_exif["Informations sur l'image"].append(f"{self.traduire_propriete(tag)}: <font color='yellow'>{valeur}</font>\n")
                elif "GPS" in tag:
                    groupes_exif["Géolocalisation"].append(f"{self.traduire_propriete(tag)}: <font color='yellow'>{valeur}</font>\n")
                elif "EXIF" in tag:
                    groupes_exif["Réglages de l'appareil photo"].append(f"{self.traduire_propriete(tag)}: <font color='yellow'>{valeur}</font>\n")
                else:
                    groupes_exif["Données temporelles"].append(f"{self.traduire_propriete(tag)}: <font color='yellow'>{valeur}</font>\n")
        
        col_index = 0
        for titre_groupe, donnees_groupe in groupes_exif.items():
            if donnees_groupe:
                for donnee in donnees_groupe:
                    if col_index == 0:
                        self.txt_infos_exif_col1.append(donnee)
                    elif col_index == 1:
                        self.txt_infos_exif_col2.append(donnee)
                    elif col_index == 2:
                        self.txt_infos_exif_col3.append(donnee)
                    else:
                        self.txt_infos_exif_col4.append(donnee)
                    col_index = (col_index + 1) % 4


    def traduire_propriete(self, tag):
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
            "EXIF UserComment": "Commentaire de l'utilisateur",
            "Image ImageWidth": "Largeur de l'image",
            "Image ImageLength": "Longueur de l'image",
            "Image SamplesPerPixel": "Échantillons d'images par pixel",
            "Thumbnail XResolution":"Vignette XResolution",
            "Thumbnail JPEGInterchangeFormatLength":"Longueur du format d'échange JPEG des vignettes",
            "Image BitsPerSample":"Bits d'image par échantillon",
            "Thumbnail YResolution":"Vignette YResolution",
            "JPEGThumbnail":"Miniature JPEG",
            "Image PhotometricInterpretation":"Image Interprétation photométrique",
            "Thumbnail ResolutionUnit":"Unité de résolution des vignettes"
        }
        return traductions.get(tag, tag)

    def recuperer_donnees_exif(self, chemin_fichier):
        with open(chemin_fichier, 'rb') as f:
            tags = exifread.process_file(f)
            return {tag: str(value) for tag, value in tags.items()}

def main():
    app = QApplication([])
    fenetre = Fenetre()
    fenetre.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()