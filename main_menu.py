import arcade
import arcade.gui
from loading_screen import LoadingView
from save_management import SaveManagement
from enemy_management import EnemyManagement
from sounds import GameSounds
from constants import *

class MainView(arcade.View):
    """Main application class."""

    def __init__(self):
        super().__init__()
        # Create the UI Manager
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.save_management = SaveManagement(SAVE_FILENAME)

        # Create a UI Box Layout to organize the buttons vertically
        self.layout = arcade.gui.UIBoxLayout(vertical=True, spacing=20)

        # Define buttons with styles
        self.layout.add(self.create_button("Resume", self.resume_game))
        self.layout.add(self.create_button("Start New Game", self.start_new_game))
        self.layout.add(self.create_button("Options", self.open_options))
        self.layout.add(self.create_button("Exit", self.exit_game))

        # Add the layout to an anchor widget for centering
        self.anchor_widget = arcade.gui.UIAnchorWidget(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.layout
        )
        self.manager.add(self.anchor_widget)

        self.fullscreen = True  # Le jeu démarre en plein écran
        self.window.set_fullscreen(self.fullscreen)  # Appliquer l'état de plein écran

        self.save_management = SaveManagement(SAVE_FILENAME)
        self.enemies_management = EnemyManagement()

        # Gestion de la musique
        self.sounds = GameSounds()



    def create_button(self, text, action):
        """Create a button and connect it to an action."""
        button = arcade.gui.UIFlatButton(
            text=text,
            width=320,
            style={
                "font_color": arcade.color.WHITE,
                "bg_color": arcade.color.FOREST_GREEN,
                "border_color": arcade.color.GOLDEN_YELLOW,
            },
        )
        button.on_click = action  # Connect the button to the action
        return button

    def resume_game(self, event):
        """Resume the game."""
        print("Resuming game... ")

        self.saves = self.save_management.load_file()

        self.setup_values = {
                "player_x": self.saves[2],
                "player_y": self.saves[3],
                "map_index": self.saves[1],
                "player_pv": self.saves[6],
                "player_has_sword": self.saves[7],
                "last_player_x": self.saves[4],
                "last_player_y": self.saves[5],
                "default_player_texture": TEXTURE_DOWN,
                "player_projectile_type": self.saves[8],
                "enemy_file": ENEMY_FILENAME
        }

        loading_view = LoadingView(setup_values=self.setup_values, resume=True)  # Assurez-vous que GameView est bien défini dans loading_view.py
        self.window.show_view(loading_view)

    def start_new_game(self, event):
        """Start a new game."""
        self.save_management.reset_file()
        self.saves = self.save_management.load_file()
        self.enemies_management.reset_file()

        self.setup_values = {
                "player_x": self.saves[2],
                "player_y": self.saves[3],
                "map_index": self.saves[1],
                "player_pv": self.saves[6],
                "player_has_sword": self.saves[7],
                "last_player_x": self.saves[4],
                "last_player_y": self.saves[5],
                "default_player_texture": TEXTURE_DOWN,
                "player_projectile_type": self.saves[8],
                "enemy_file": ORIGINAL_ENEMY_FILENAME
        }

        loading_view = LoadingView(self.setup_values)  # Assurez-vous que GameView est bien défini dans loading_view.py
        self.window.show_view(loading_view)

    def open_options(self, event):
        """Open options menu."""
        print("Options menu... (not yet implemented)")

    def exit_game(self, event):
        """Exit the game."""
        self.window.close()

    def on_draw(self):
        """Render the screen."""
        self.clear()
        self.manager.draw()

    def on_show_view(self):
        """Set background color when this view is shown."""
        arcade.set_background_color(arcade.color.BLACK)
        self.manager.enable()
        self.sounds.play_music(self.sounds.tittle_screen)

    def on_hide_view(self):
        """Disable UI manager when hidden."""
        self.manager.disable()
        self.sounds.stop_music()

    def on_key_press(self, key, modifiers):
        """Handle key press events."""
        if key == arcade.key.ESCAPE:
            # Fermer le jeu
            self.window.close()
        elif key == arcade.key.ESCAPE:
            self.fullscreen = not self.fullscreen  # Inverser l'état actuel du plein écran
            self.window.set_fullscreen(self.fullscreen)  # Appliquer le changement

# Créer la fenêtre et afficher le menu principal
def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    main_menu = MainView()
    window.show_view(main_menu)
    arcade.run()

if __name__ == "__main__":
    main()