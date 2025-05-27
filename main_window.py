import arcade
from main_menu import MainView  # Importez la classe MainView du fichier main_menu.py
from save_management import SaveManagement
from constants import *

def main():
    """Main function."""
    # Créez la fenêtre avec fullscreen activé
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=True)
    main_menu = MainView()  # Créez la vue du menu principal
    window.show_view(main_menu)  # Affichez la vue du menu principal
    arcade.run()

if __name__ == "__main__":
    main()