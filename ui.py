import arcade
from constants import *
from projectile import LightProjectile, PoisonProjectile, ExplosionProjectile

class Heart(arcade.Sprite):
    """ Class to represent a heart with different states. """
    def __init__(self, state):
        super().__init__()
        self.state = state  # state is 0 (full), 1 (3/4), 2 (1/2), 3 (1/4), 4 (empty)
        self.scale = 0.3  # Modifier cette valeur pour changer la taille des cœurs
        self.update_texture()

    def update_texture(self):
        """ Update the heart texture based on its state. """
        textures = [
            r"SpritesTempo/heart_full.png",
            r"SpritesTempo/heart_3_4.png",
            r"SpritesTempo/heart_half.png",
            r"SpritesTempo/heart_1_4.png",
            r"SpritesTempo/heart_empty.png",
        ]
        self.texture = arcade.load_texture(textures[self.state])

class UI:
    """ Class to handle displaying UI elements like health and projectile limit """
    def __init__(self, player):
        self.player = player
        self.projectile_limit = 100  # Limite initiale pour l'envoi des projectiles
        self.current_projectile_points = 100  # Points actuels pour envoyer des projectiles
        self.time_since_last_regen = 0

    def update(self, delta_time):
        """ Met à jour la barre de progression des projectiles et les points de vie """
        if self.current_projectile_points < 100:
            self.time_since_last_regen += delta_time
            
             # Récupérer l'instance du projectile actuel
            current_projectile_type = self.player.projectile_type

            if hasattr(current_projectile_type, 'cooldown') and hasattr(current_projectile_type, 'cost'):
                if self.time_since_last_regen >= current_projectile_type.cooldown:
                    self.current_projectile_points = min(self.current_projectile_points + current_projectile_type.cost, 100)
                    self.time_since_last_regen = 0

    def draw(self, camera_position, game):
        self.game = game
        # Dessin des éléments de l'interface utilisateur en fonction de la position de la caméra
        self.draw_hearts(camera_position, game)
        self.draw_projectile_bar(camera_position)
        
    def draw_projectile_bar(self, camera_position):    
        
        # Dessin de la barre de projectiles
        bar_width = 200
        filled_width = bar_width * (self.current_projectile_points / 100)
        
        # Fond de la barre
        arcade.draw_rectangle_filled(
            camera_position[0] + 150,  # Position X relative à la caméra
            camera_position[1] + 50,   # Position Y relative à la caméra
            bar_width, 
            10, 
            arcade.color.GRAY
        )

        if self.player.projectile_type is LightProjectile: 
            # Partie remplie de la barre
            arcade.draw_rectangle_filled(
                camera_position[0] + 150 - (bar_width - filled_width) / 2,
                camera_position[1] + 50,
                filled_width, 
                10, 
                arcade.color.ORANGE
            )

        elif self.player.projectile_type is PoisonProjectile: 
            # Partie remplie de la barre
            arcade.draw_rectangle_filled(
                camera_position[0] + 150 - (bar_width - filled_width) / 2,
                camera_position[1] + 50,
                filled_width, 
                10, 
                arcade.color.BLUE
            )        

        elif self.player.projectile_type is ExplosionProjectile : 
            # Partie remplie de la barre
            arcade.draw_rectangle_filled(
                camera_position[0] + 150 - (bar_width - filled_width) / 2,
                camera_position[1] + 50,
                filled_width, 
                10, 
                arcade.color.VIOLET
            )

    def draw_hearts(self, camera_position, game):
        self.game = game
        # Position de départ pour les cœurs, ajustée selon la position de la caméra
        heart_x = camera_position[0] + 50
        heart_y = camera_position[1] + self.game.window.height - 50

        # Points de vie restants du joueur
        remaining_health = self.player.pv

        # Affichage des cœurs en fonction des points de vie du joueur
        for i in range(self.player.max_hearts):
            if remaining_health >= 100:
                state = 0  # Cœur plein
            elif remaining_health >= 75:
                state = 1  # 3/4 plein
            elif remaining_health >= 50:
                state = 2  # Moitié plein
            elif remaining_health >= 25:
                state = 3  # 1/4 plein
            else:
                state = 4  # Cœur vide

            # Crée et dessine le cœur avec l'état calculé
            heart = Heart(state)
            heart.center_x = heart_x + i * 25
            heart.center_y = heart_y
            heart.draw()

            # Réduire les points de vie restants pour le prochain cœur
            remaining_health -= 100