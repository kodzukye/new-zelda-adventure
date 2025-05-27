import arcade.gui
from constants import *
from save_management import SaveManagement
from loading_screen import LoadingView
from PIL import Image, ImageOps, ImageDraw
import io

class DeathMenu(arcade.View):
    """Death menu class."""
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view  # Reference to the game view
        self.manager = arcade.gui.UIManager()  # UI Manager
        self.manager.enable()
        self.window.set_mouse_visible(True)

        # Placeholder for background texture
        self.grayscale_background = None

        # Create a UI box layout for vertical organization
        self.layout = arcade.gui.UIBoxLayout(vertical=True, spacing=20)

        # Add buttons to the layout
        resume_button = arcade.gui.UIFlatButton(text="Respawn to last checkpoint", width=300)
        resume_button.on_click = self.on_resume_click
        self.layout.add(resume_button)

        option_button = arcade.gui.UIFlatButton(text="Option", width=300)
        option_button.on_click = self.on_option_click
        self.layout.add(option_button)

        quit_button = arcade.gui.UIFlatButton(text="Quit to Main Menu", width=300)
        quit_button.on_click = self.on_quit_click
        self.layout.add(quit_button)

        # Anchor the layout to the center of the screen
        self.anchor = arcade.gui.UIAnchorWidget(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.layout
        )
        self.manager.add(self.anchor)

    def on_show_view(self):
        """Prepare the grayscale background when showing the view."""
        # Capture the game view as an image
        buffer = io.BytesIO()
        arcade.get_image().save(buffer, format="PNG")
        buffer.seek(0)

        # Open the captured image
        image = Image.open(buffer)

        # Resize the image to exactly match the window dimensions
        resized_image = image.resize((self.window.width, self.window.height), Image.Resampling.LANCZOS)

        # Convert the resized image to grayscale
        grayscale_image = ImageOps.grayscale(resized_image)

        # Supprimer la texture précédente si elle existe
        from datetime import datetime

        # Générer un nom unique basé sur l'heure actuelle
        unique_name = f"grayscale_background_{datetime.now().timestamp()}"
        self.grayscale_background = arcade.Texture(
            name=unique_name,
            image=grayscale_image
        )

    def on_resume_click(self, event):
        """Handle resume button click."""
        print("Resume menu... (not yet implemented)")

        self.save_management = SaveManagement(SAVE_FILENAME)
        self.saves = self.save_management.load_file()

        self.setup_values = {
                "player_x": self.saves[2],
                "player_y": self.saves[3],
                "map_index": self.saves[1],
                "player_pv": 25,
                "player_has_sword": self.saves[7],
                "last_player_x": self.saves[4],
                "last_player_y": self.saves[5],
                "default_player_texture": TEXTURE_DOWN,
                "player_projectile_type": self.saves[8],
                "enemy_file": self.saves[9]
        }

        self.game_view.stop_all_sounds()

        loading_view = LoadingView(setup_values=self.setup_values, resume=True)  # Assurez-vous que GameView est bien défini dans loading_view.py
        self.window.show_view(loading_view)

    def on_option_click(self, event):
        print("Options menu... (not yet implemented)")
        self.game_view.stop_all_sounds()

    def on_quit_click(self, event):
        from main_menu import MainView
        """Handle quit button click."""
        self.game_view.stop_all_sounds()
        main_menu = MainView()
        self.window.show_view(main_menu)

    def on_draw(self):
        """Draw the Death menu."""
        self.clear()

        # Draw the grayscale background
        if self.grayscale_background:
            arcade.draw_lrwh_rectangle_textured(
                0, 0, self.window.width, self.window.height, self.grayscale_background
            )

        # Draw a semi-transparent black overlay
        arcade.draw_rectangle_filled(
            self.window.width / 2, self.window.height / 2,
            self.window.width, self.window.height,
            color=(0, 0, 0, 150)  # Semi-transparent black
        )

        # Draw the UI manager on top
        self.manager.draw()

    def on_hide_view(self):
        """Disable UI manager when hiding this view."""
        self.manager.disable()
