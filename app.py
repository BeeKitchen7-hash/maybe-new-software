#!/usr/bin/env python3
import sys
import os
import json
import requests
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QListWidget, QListWidgetItem, QLabel,
    QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor
from urllib.parse import urljoin

class DownloadWorker(QThread):
    progress_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(list)
    error_signal = pyqtSignal(str)
    
    def __init__(self, roblox_id):
        super().__init__()
        self.roblox_id = roblox_id
        self.download_dir = Path("downloads") / self.roblox_id
        
    def run(self):
        try:
            self.progress_signal.emit(f"Recherche des fichiers pour l'ID: {self.roblox_id}...")
            
            # Créer le dossier de téléchargement
            self.download_dir.mkdir(parents=True, exist_ok=True)
            
            # Appel API à rbxdl
            api_url = f"https://rbxdl.johnmarctumulak.com/api/download/{self.roblox_id}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            self.progress_signal.emit("Connexion au serveur...")
            response = requests.get(api_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                except:
                    # Si la réponse n'est pas JSON, c'est peut-être un fichier
                    data = {"file": response.content}
                
                # Sauvegarder le fichier ou les données
                if isinstance(data, dict):
                    file_path = self.download_dir / f"{self.roblox_id}_data.json"
                    with open(file_path, 'w') as f:
                        json.dump(data, f, indent=2)
                    self.progress_signal.emit(f"Fichier téléchargé: {file_path}")
                else:
                    file_path = self.download_dir / f"{self.roblox_id}.rbx"
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    self.progress_signal.emit(f"Fichier téléchargé: {file_path}")
                
                # Récupérer la liste des fichiers téléchargés
                downloaded_files = list(self.download_dir.iterdir())
                self.finished_signal.emit(downloaded_files)
                
            else:
                self.error_signal.emit(f"Erreur API: Code {response.status_code}")
                
        except requests.exceptions.Timeout:
            self.error_signal.emit("Erreur: Délai d'attente dépassé. Le serveur ne répond pas.")
        except requests.exceptions.ConnectionError:
            self.error_signal.emit("Erreur: Impossible de se connecter au serveur.")
        except Exception as e:
            self.error_signal.emit(f"Erreur: {str(e)}")


class RobloxSpoofApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()
        self.setWindowTitle("Roblox Downloader")
        self.setGeometry(100, 100, 700, 600)
        
    def init_ui(self):
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Style noir et rouge
        central_widget.setStyleSheet("""
            QWidget {
                background-color: #000000;
                color: #FF0000;
            }
            QLineEdit {
                background-color: #1a1a1a;
                color: #FF0000;
                border: 2px solid #FF0000;
                padding: 8px;
                font-size: 12px;
            }
            QPushButton {
                background-color: #FF0000;
                color: #000000;
                border: none;
                padding: 10px 20px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #CC0000;
            }
            QPushButton:pressed {
                background-color: #990000;
            }
            QListWidget {
                background-color: #1a1a1a;
                color: #FF0000;
                border: 2px solid #FF0000;
            }
            QLabel {
                color: #FF0000;
            }
        """)
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Titre
        title = QLabel("ROBLOX DOWNLOADER")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Section de recherche
        search_layout = QHBoxLayout()
        
        search_label = QLabel("ID ROBLOX:")
        search_label.setFont(QFont("Arial", 11))
        search_layout.addWidget(search_label)
        
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Entrez l'ID Roblox...")
        self.id_input.setFont(QFont("Arial", 11))
        self.id_input.returnPressed.connect(self.search_and_download)
        search_layout.addWidget(self.id_input)
        
        self.search_button = QPushButton("SEARCH")
        self.search_button.setFont(QFont("Arial", 11, QFont.Bold))
        self.search_button.setMinimumWidth(100)
        self.search_button.clicked.connect(self.search_and_download)
        search_layout.addWidget(self.search_button)
        
        main_layout.addLayout(search_layout)
        
        # Label pour le statut
        self.status_label = QLabel("Prêt...")
        self.status_label.setFont(QFont("Arial", 10))
        main_layout.addWidget(self.status_label)
        
        # Liste des fichiers téléchargés
        files_title = QLabel("FICHIERS TÉLÉCHARGÉS:")
        files_title.setFont(QFont("Arial", 11))
        main_layout.addWidget(files_title)
        
        self.file_list = QListWidget()
        self.file_list.setFont(QFont("Arial", 10))
        self.file_list.setMinimumHeight(300)
        main_layout.addWidget(self.file_list)
        
        # Layout pour les boutons d'action
        action_layout = QHBoxLayout()
        
        self.open_folder_button = QPushButton("OUVRIR DOSSIER")
        self.open_folder_button.setFont(QFont("Arial", 10, QFont.Bold))
        self.open_folder_button.clicked.connect(self.open_downloads_folder)
        action_layout.addWidget(self.open_folder_button)
        
        self.delete_button = QPushButton("SUPPRIMER FICHIER")
        self.delete_button.setFont(QFont("Arial", 10, QFont.Bold))
        self.delete_button.clicked.connect(self.delete_selected_file)
        action_layout.addWidget(self.delete_button)
        
        self.refresh_button = QPushButton("RAFRAÎCHIR")
        self.refresh_button.setFont(QFont("Arial", 10, QFont.Bold))
        self.refresh_button.clicked.connect(self.refresh_file_list)
        action_layout.addWidget(self.refresh_button)
        
        main_layout.addLayout(action_layout)
        
        central_widget.setLayout(main_layout)
        self.refresh_file_list()
        
    def search_and_download(self):
        roblox_id = self.id_input.text().strip()
        
        if not roblox_id:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un ID Roblox valide!")
            return
        
        # Désactiver le bouton pendant le téléchargement
        self.search_button.setEnabled(False)
        self.id_input.setEnabled(False)
        
        # Créer et démarrer le worker
        self.worker = DownloadWorker(roblox_id)
        self.worker.progress_signal.connect(self.update_status)
        self.worker.finished_signal.connect(self.on_download_finished)
        self.worker.error_signal.connect(self.on_download_error)
        self.worker.start()
        
    def update_status(self, message):
        self.status_label.setText(message)
        
    def on_download_finished(self, files):
        self.status_label.setText(f"Téléchargement terminé! {len(files)} fichier(s) trouvé(s).")
        self.refresh_file_list()
        self.search_button.setEnabled(True)
        self.id_input.setEnabled(True)
        QMessageBox.information(self, "Succès", "Fichiers téléchargés avec succès!")
        
    def on_download_error(self, error_message):
        self.status_label.setText(f"Erreur: {error_message}")
        self.search_button.setEnabled(True)
        self.id_input.setEnabled(True)
        QMessageBox.critical(self, "Erreur", error_message)
        
    def refresh_file_list(self):
        self.file_list.clear()
        downloads_dir = Path("downloads")
        
        if not downloads_dir.exists():
            downloads_dir.mkdir(parents=True, exist_ok=True)
        
        # Récupérer tous les fichiers
        all_files = []
        for subdir in downloads_dir.iterdir():
            if subdir.is_dir():
                for file in subdir.iterdir():
                    all_files.append(file)
        
        if not all_files:
            item = QListWidgetItem("Aucun fichier téléchargé")
            item.setForeground(QColor("#FF6600"))
            self.file_list.addItem(item)
        else:
            for file in sorted(all_files, key=lambda x: x.stat().st_mtime, reverse=True):
                file_size = file.stat().st_size / 1024  # KB
                display_text = f"{file.name} ({file_size:.2f} KB) - {file.parent.name}"
                item = QListWidgetItem(display_text)
                item.setData(Qt.UserRole, str(file))
                self.file_list.addItem(item)
        
    def delete_selected_file(self):
        current_item = self.file_list.currentItem()
        
        if not current_item:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un fichier à supprimer!")
            return
        
        if "Aucun fichier" in current_item.text():
            return
        
        file_path = current_item.data(Qt.UserRole)
        
        reply = QMessageBox.question(
            self,
            "Confirmation",
            f"Êtes-vous sûr de vouloir supprimer:\n{Path(file_path).name}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                os.remove(file_path)
                self.refresh_file_list()
                QMessageBox.information(self, "Succès", "Fichier supprimé!")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible de supprimer: {str(e)}")
                
    def open_downloads_folder(self):
        downloads_dir = Path("downloads").resolve()
        downloads_dir.mkdir(parents=True, exist_ok=True)
        os.system(f"xdg-open '{downloads_dir}'")


def main():
    app = QApplication(sys.argv)
    window = RobloxSpoofApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
