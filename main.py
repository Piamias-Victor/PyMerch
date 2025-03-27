import sys
from PyQt5.QtWidgets import QApplication
from views.main_window import MainWindow
from controllers.pharmacy_controller import PharmacyController
from controllers.data_controller import DataController
from utils.config import load_config

def main():
    """Point d'entrée principal de l'application"""
    app = QApplication(sys.argv)
    
    # Chargement de la configuration
    config = load_config()
    
    # Initialisation des contrôleurs
    data_controller = DataController()
    pharmacy_controller = PharmacyController(data_controller)
    
    # Création et affichage de la fenêtre principale
    main_window = MainWindow(pharmacy_controller)
    main_window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()