import arcade.gui
from constants import *
from PIL import Image, ImageOps, ImageDraw
import io

#### Menu Pause
class PauseMenu(arcade.View):
    """Pause menu class."""
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view  # Reference to the game view
        self.manager = arcade.gui.UIManager()  # UI Manager
        self.manager.enable()
        self.window.set_mouse_visible(True)

        # Create a UI box layout for vertical organization
        self.layout = arcade.gui.UIBoxLayout(vertical=True, spacing=20)

        # Add buttons to the layout
        resume_button = arcade.gui.UIFlatButton(text="Resume", width=300)
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

        self.was_low_health_playing = self.game_view.low_health_sound_playing
        if self.was_low_health_playing:
            self.game_view.stop_all_sounds()

    def on_show_view(self):
        self.pause_background = None
        
        buffer = io.BytesIO()
        arcade.get_image().save(buffer, format="PNG")
        buffer.seek(0)

        # Open the captured image
        image = Image.open(buffer)

        # Resize the image to exactly match the window dimensions
        resized_image = image.resize((self.window.width, self.window.height), Image.Resampling.LANCZOS)

        # Convert the grayscale image back to a texture
        self.pause_background = arcade.Texture(
            name="pause_background",
            image=resized_image
        )

        # Supprimer la texture précédente si elle existe
        from datetime import datetime

        # Générer un nom unique basé sur l'heure actuelle
        unique_name = f"pause_background_{datetime.now().timestamp()}"
        self.pause_background = arcade.Texture(
            name=unique_name,
            image=resized_image
        )

    def on_resume_click(self, event):
        """Handle resume button click."""
        # Reprendre la musique des wizzrobes si nécessaire
        for wizzrobe in self.game_view.wizzrobes:
            if wizzrobe.state == "poursuite" and not wizzrobe.musique_en_cours:
                wizzrobe.sounds.play_music(wizzrobe.sounds.wizzrobe_theme)
                wizzrobe.musique_en_cours = True
        self.window.show_view(self.game_view)
        self.window.set_mouse_visible(False)


    def on_option_click(self,event):
        print("Options menu... (not yet implemented)")

    def on_quit_click(self, event):
        from main_menu import MainView
        """Handle quit button click."""
        self.game_view.stop_all_sounds()
        main_menu = MainView()
        self.window.show_view(main_menu)

    def on_draw(self):
        """Draw the pause menu."""
        self.clear()

        if self.pause_background:
            arcade.draw_lrwh_rectangle_textured(
                0, 0, self.window.width, self.window.height, self.pause_background
            )
        
        # Draw a semi-transparent black overlay
        arcade.draw_rectangle_filled(
            self.window.width / 2, self.window.height / 2,
            self.window.width, self.window.height,
            color=(0, 0, 0, 150)  # Semi-transparent black
        )
        self.manager.draw()

    def on_hide_view(self):
        """Disable UI manager when hiding this view."""
        self.manager.disable()