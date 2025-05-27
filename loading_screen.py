from constants import *
from save_management import SaveManagement

class LoadingView(arcade.View):
    """Loading screen view."""
    def __init__(self, setup_values, resume=False):
        super().__init__()
        self.loading_done = False  # Flag to indicate if loading is done
        self.game_view = None      # Placeholder for the game view
        self.setup_values = setup_values
        self.resume = resume


        self.fullscreen = True  # Le jeu démarre en plein écran
        self.window.set_fullscreen(self.fullscreen)  # Appliquer l'état de plein écran

        # Charger l'image de fond
        self.background_image = arcade.load_texture("Images/zelda-logo.jpg")  # Remplacez par le chemin de votre image

    def on_show_view(self):
        """Set up the loading view."""
        pass  # Pas besoin de 'arcade.set_background_texture()' avec l'image

    def on_draw(self):
        """Render the loading screen."""
        self.clear()
        
        # Dessiner l'image de fond
        arcade.draw_lrwh_rectangle_textured(
            0, 0,                      # Coin inférieur gauche
            self.window.width,         # Largeur de la fenêtre
            self.window.height,        # Hauteur de la fenêtre
            self.background_image      # Image de fond
        )

        # # Dessiner le texte au-dessus de l'image
        # arcade.draw_text(
        #     "The Legend Of Link : A New Zelda Adventure",
        #     SCREEN_WIDTH / 2,
        #     SCREEN_HEIGHT / 2 + 50,
        #     arcade.color.WHITE,
        #     font_size=24,
        #     anchor_x="center"
        # )

    def on_update(self, delta_time):
        """Check if loading is done and switch views."""
        if not self.loading_done:
            if not self.resume:
                self.start_game()
            else:
                self.resume_game()
        else:
            self.window.show_view(self.game_view)

    def start_game(self):
        from main import MyGame
        """Initialize and prepare the main game view."""
        self.game_view = MyGame()
        self.game_view.setup(self.setup_values)  # Appeler la méthode d'initialisation du jeu
        self.loading_done = True

    def resume_game(self):
        from main import MyGame
        """Initialize and prepare the main game view."""
        self.game_view = MyGame()
        self.game_view.setup(self.setup_values)  # Appeler la méthode d'initialisation du jeu
        self.loading_done = True