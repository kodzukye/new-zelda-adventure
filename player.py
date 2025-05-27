import arcade
from constants import *
from projectile import *
from sword import Sword
from ui import Heart


class Player(arcade.Sprite):
    """ Player Class """
    MAX_HEALTH = 1000  # Limite maximum des points de vie

    def __init__(self, game, default_texture=TEXTURE_RIGHT):
        super().__init__()
        self.scale = SPRITE_SCALING
        self.textures = []
        self.pv = 100  # Points de vie du joueur initial
        self.max_hearts = self.MAX_HEALTH // 100  # Maximum de cœurs affichés
        self.hearts = []  # Liste des cœurs
        self.projectile_type = LightProjectile
        self.projectile_type.name = 'light'
        self.invincible_timer = 0
        self.is_invincible = False # État d'invincibilité

        self.has_sword = False  # Le joueur ne commence pas avec l'épée
        self.is_attacking = False
        self.attack_reset_scheduled = False
        self.textures_with_sword = []

        self.current_direction = default_texture

        self.game = game
        
        self.attack_active = False  # Marqueur pour savoir si l'attaque est en cours
        
        # Charger les textures du joueur avec l'épée
        self.textures_with_sword.append(arcade.load_texture(r"SpritesTempo/zelda_with_master_sword_left.png"))
        self.textures_with_sword.append(arcade.load_texture(r"SpritesTempo/zelda_with_master_sword_right.png"))
        self.textures_with_sword.append(arcade.load_texture(r"SpritesTempo/zelda_with_master_sword_up.png"))
        self.textures_with_sword.append(arcade.load_texture(r"SpritesTempo/zelda_with_master_sword_down.png"))


        # Charger les textures du joueur
        texture = arcade.load_texture(r"Sprites/Main Character/zelda_idle_left.png")
        self.textures.append(texture)
        texture = arcade.load_texture(r"Sprites/Main Character/zelda_idle_right.png")
        self.textures.append(texture)
        texture = arcade.load_texture(r"Sprites/Main Character/zelda_idle_up.png")
        self.textures.append(texture)
        texture = arcade.load_texture(r"Sprites/Main Character/zelda_idle_down.png")
        self.textures.append(texture)

        # Le joueur fait face à droite par défaut
        self.texture = self.textures[default_texture]
        
        # Initialiser les cœurs
        self.update_hearts()
        # variable pour gérer le clignotement
        self.hit_timer = 0

    def add_heart(self):
        """ Ajouter un cœur au joueur """
        new_heart = Heart(0)  # 0 = plein
        # Modifier l'espacement en ajustant la multiplication pour espacer les cœurs
        new_heart.center_x = 50 + len(self.hearts) * 25  # Augmentez ici l'espacement
        new_heart.center_y = self.game.window.height - 50
        self.hearts.append(new_heart)

    def update_hearts(self):
        """ Mettre à jour les cœurs en fonction des PV actuels """
        self.hearts.clear()  # Vider les cœurs existants
        
        # Calculer le nombre de cœurs pleins et partiels
        total_hearts = self.pv // 100
        remaining_health = self.pv % 100

        # Ajouter les cœurs pleins
        for _ in range(total_hearts):
            self.add_heart()

        # Ajouter un cœur partiel s'il reste des PV
        if remaining_health > 0:
            partial_heart = Heart(0)
            partial_heart.center_x = 50 + len(self.hearts) * 25
            partial_heart.center_y = self.game.window.height  - 50
            if remaining_health >= 75:
                partial_heart.state = 1  # 3/4 plein
            elif remaining_health >= 50:
                partial_heart.state = 2  # 1/2 plein
            elif remaining_health >= 25:
                partial_heart.state = 3  # 1/4 plein
            else:
                partial_heart.state = 4  # Vide
            partial_heart.update_texture()
            self.hearts.append(partial_heart)

    def take_damage(self, damage):
        """ Réduire les PV et mettre à jour les cœurs en fonction des dégâts """
        if not self.is_invincible:
            self.pv -= damage
            if self.pv < 0:
                self.pv = 0
            self.update_hearts()  # Mettre à jour les cœurs après avoir pris des dégâts
            self.is_invincible = True
            self.invincible_timer = 1

    def heal(self, heal_amount):
        """ Soigner le joueur et mettre à jour les cœurs """
        self.pv += heal_amount
        if self.pv > self.MAX_HEALTH:
            self.pv = self.MAX_HEALTH
        self.update_hearts()  # Mettre à jour les cœurs après guérison

    def draw_hearts(self):
        """ Dessiner les cœurs à l'écran """
        for heart in self.hearts:
            heart.draw()

    def on_hit(self):
        # Définir la couleur en rouge (rouge = 255, vert = 0, bleu = 0)
        self.color = (255, 0, 0)
        self.hit_timer = 0.5  # Le sprite restera rouge pendant 0.2 secondes

    def acquire_sword(self):
        """ Le joueur récupère l'épée et change de texture """
        self.has_sword = True

    def attack(self, enemies):
        """ Déclenche l'animation d'attaque et inflige des dégâts aux ennemis dans une portée spécifique devant le joueur """
        if self.has_sword and not self.is_attacking:
            self.is_attacking = True  # Met à jour l'état d'attaque
            self.attack_active = True  # Marqueur pour savoir si l'attaque est en cours
            
            # Changer le sprite pour l'animation d'attaque en fonction de la direction actuelle
            if self.texture == self.textures[TEXTURE_LEFT]:
                self.texture = self.textures_with_sword[TEXTURE_LEFT_ATTACK]
                detection_x_start, detection_x_end = self.center_x - 100, self.center_x - 20
                detection_y_start, detection_y_end = self.center_y - 10, self.center_y + 10
            elif self.texture == self.textures[TEXTURE_RIGHT]:
                self.texture = self.textures_with_sword[TEXTURE_RIGHT_ATTACK]
                detection_x_start, detection_x_end = self.center_x + 20, self.center_x + 100
                detection_y_start, detection_y_end = self.center_y - 10, self.center_y + 10
            elif self.texture == self.textures[TEXTURE_UP]:
                self.texture = self.textures_with_sword[TEXTURE_UP_ATTACK]
                detection_x_start, detection_x_end = self.center_x - 10, self.center_x + 10
                detection_y_start, detection_y_end = self.center_y + 20, self.center_y + 100
            elif self.texture == self.textures[TEXTURE_DOWN]:
                self.texture = self.textures_with_sword[TEXTURE_DOWN_ATTACK]
                detection_x_start, detection_x_end = self.center_x - 10, self.center_x + 10
                detection_y_start, detection_y_end = self.center_y - 100, self.center_y - 20

            # Inflige des dégâts aux ennemis dans la zone de détection
            for enemy in enemies:
                if (detection_x_start <= enemy.center_x <= detection_x_end and
                    detection_y_start <= enemy.center_y <= detection_y_end):
                    enemy.take_damage(20)  # Inflige 20 points de dégâts à l'ennemi

            # Planifie la réinitialisation de l'attaque si elle n'est pas déjà en attente
            if not self.attack_reset_scheduled:
                arcade.schedule(self.reset_attack_state, 0.2)
                self.attack_reset_scheduled = True  # Marque la réinitialisation comme programmée


    def reset_attack_state(self, delta_time):
        """ Réinitialise l'état d'attaque après un délai """
        self.is_attacking = False
        #self.attack_reset_scheduled = False  # Libère l'indicateur pour permettre une nouvelle programmation
        self.attack_active = False  # Marqueur pour savoir si l'attaque est en cours
        # Remet le sprite à son état normal
        self.texture = self.textures[self.current_direction]

    def shoot_projectile(self):
        
        """ Tirer un projectile dans la direction où le joueur fait face """

        # Déterminer la direction et charger la texture correspondante
        if self.texture == self.textures[TEXTURE_LEFT] or self.texture == self.textures_with_sword[TEXTURE_LEFT]:
            direction_x, direction_y = -1, 0
            texture = self.projectile_type.TEXTURES[0]
        elif self.texture == self.textures[TEXTURE_RIGHT] or self.texture == self.textures_with_sword[TEXTURE_RIGHT]:
            direction_x, direction_y = 1, 0
            texture = self.projectile_type.TEXTURES[1]
        elif self.texture == self.textures[TEXTURE_UP] or self.texture == self.textures_with_sword[TEXTURE_UP]:
            direction_x, direction_y = 0, 1
            texture= self.projectile_type.TEXTURES[2]
        else:
            direction_x, direction_y = 0, -1
            texture = self.projectile_type.TEXTURES[3]

        # Appliquer la direction au projectile
        projectile = self.projectile_type(texture, PROJECTILE_SCALING)
        projectile.center_x = self.center_x
        projectile.center_y = self.center_y
        projectile.change_x = direction_x * PROJECTILE_SPEED
        projectile.change_y = direction_y * PROJECTILE_SPEED

        return projectile

    def update(self, delta_time):
        
        """ Mettre à jour la position et la direction du joueur """
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Changer la direction selon le mouvement
        if self.change_x < 0 and self.change_y == 0:
            self.texture = self.textures[TEXTURE_LEFT]
            self.current_direction = TEXTURE_LEFT

        elif self.change_x > 0 and self.change_y == 0:
            self.texture = self.textures[TEXTURE_RIGHT]
            self.current_direction = TEXTURE_RIGHT

        elif self.change_y > 0 and self.change_x == 0:
            self.texture = self.textures[TEXTURE_UP]
            self.current_direction = TEXTURE_UP

        elif self.change_y < 0 and self.change_x == 0:
            self.texture = self.textures[TEXTURE_DOWN]
            self.current_direction = TEXTURE_DOWN

        if self.has_sword and self.is_attacking:
            if self.change_x < 0 and self.change_y == 0:
                self.texture = self.textures_with_sword[TEXTURE_LEFT]
            elif self.change_x > 0 and self.change_y == 0:
                self.texture = self.textures_with_sword[TEXTURE_RIGHT]
            elif self.change_y > 0 and self.change_x == 0:
                self.texture = self.textures_with_sword[TEXTURE_UP]
            elif self.change_y < 0 and self.change_x == 0:
                self.texture = self.textures_with_sword[TEXTURE_DOWN]
        else:
            super().update()

        if self.is_invincible:
            self.invincible_timer -= delta_time
            if self.invincible_timer <= 0 :
                self.is_invincible = False

        # Gérer le clignotement
        if self.hit_timer > 0:
            self.hit_timer -= delta_time
            if self.hit_timer <= 0:
                self.color = (255, 255, 255)  # Remettre la couleur normale