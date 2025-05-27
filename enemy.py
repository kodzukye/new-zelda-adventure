from enemy_types import ENEMY_TYPES
from constants import *
import arcade
import math


class Enemy_Projectile(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.scale = 0.3  # Vous pouvez ajuster cette valeur si nécessaire
        self.textures = []

        # Chargement des textures pour chaque direction
        # Note: Vous devrez ajuster les chemins des fichiers selon votre structure de projet
        texture = arcade.load_texture(r"SpritesTempo\arrow_left.png")
        self.textures.append(texture)
        texture = arcade.load_texture(r"SpritesTempo\arrow_right.png")
        self.textures.append(texture)
        texture = arcade.load_texture(r"SpritesTempo\arrow_up.png")
        self.textures.append(texture)
        texture = arcade.load_texture(r"SpritesTempo\arrow_down.png")
        self.textures.append(texture)

        # Texture par défaut
        self.texture = self.textures[TEXTURE_DOWN]

    def set_direction_texture(self, dx, dy):
        if abs(dx) > abs(dy):  # Mouvement horizontal dominant
            if dx < 0:
                self.texture = self.textures[TEXTURE_LEFT]
            else:
                self.texture = self.textures[TEXTURE_RIGHT]
        else:  # Mouvement vertical dominant
            if dy > 0:
                self.texture = self.textures[TEXTURE_UP]
            else:
                self.texture = self.textures[TEXTURE_DOWN]

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Remove the projectile if it goes off-screen
        '''if self.right < 0 or self.left > arcade.get_window().width or \
           self.top < 0 or self.bottom > arcade.get_window().height:
            self.remove_from_sprite_lists()'''


class SpearAttack(arcade.Sprite):
    def __init__(self, enemy_x, enemy_y, direction, range=40):
        super().__init__()
        
        # Charger les textures pour chaque direction d'attaque
        self.textures = []
        texture = arcade.load_texture(r"SpritesTempo/moblin_spear_left.png")
        self.textures.append(texture)
        texture = arcade.load_texture(r"SpritesTempo/moblin_spear_right.png")
        self.textures.append(texture)
        texture = arcade.load_texture(r"SpritesTempo/moblin_spear_up.png")
        self.textures.append(texture)
        texture = arcade.load_texture(r"SpritesTempo/moblin_spear_down.png")
        self.textures.append(texture)

        self.scale = 0.5
        self.lifetime = 0.4  # Durée de vie de l'attaque en secondes
        self.damage = 15
        
        # Positionner le sprite d'attaque en fonction de la direction
        if direction == "left":
            self.center_x = enemy_x - range
            self.center_y = enemy_y
            self.texture = self.textures[TEXTURE_LEFT]
        elif direction == "right":
            self.center_x = enemy_x + range
            self.center_y = enemy_y
            self.texture = self.textures[TEXTURE_RIGHT]
        elif direction == "up":
            self.center_x = enemy_x
            self.center_y = enemy_y + range
            self.texture = self.textures[TEXTURE_UP]
        else:  # down
            self.center_x = enemy_x
            self.center_y = enemy_y - range
            self.texture = self.textures[TEXTURE_DOWN]

    def update(self):
        self.lifetime -= 1/60  # Assume 60 FPS
        if self.lifetime <= 0:
            self.remove_from_sprite_lists()


class Archer(arcade.Sprite):
    def __init__(self, enemy_type, alive = True):
        super().__init__()
        
        self.name = enemy_type['name']
        self.hp = enemy_type['hp']
        self.alive = alive
        self.DETECTION = enemy_type['detection']
        self.OPTIMAL_DISTANCE = enemy_type['optimal_distance']
        self.MIN_DISTANCE = enemy_type['min_distance']
        self.SHOOT_RANGE = enemy_type['shoot_range']
        self.PATROL_DISTANCE = enemy_type['patrol_distance']
        
        self.textures = []
        self.scale = enemy_type['scale']

        # Ajouter une variable pour gérer le clignotement
        self.hit_timer = 0  # Durée du clignotement

        # Charger les textures
        for direction in ['left', 'right', 'up', 'down']:
            texture = arcade.load_texture(enemy_type['sprites'][direction])
            self.textures.append(texture)

        self.texture = self.textures[TEXTURE_DOWN]
        
        self.speed = enemy_type['speed']
        self.direction = 0
        self.patrol_distance = 0
        self.state = "patrouille"

        self.shoot_timer = 0
        self.SHOOT_INTERVAL = enemy_type['shoot_interval']

    def take_damage(self, damage):
        """ Réduit la santé de l'ennemi lorsqu'il prend des dégâts """
        self.hp -= damage
        if self.hp <= 0:
            self.kill()  # Supprime l'ennemi s'il n'a plus de vie

    def shoot_at_player(self, player, enemy_projectile_list):
        dx = player.center_x - self.center_x
        dy = player.center_y - self.center_y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            dx = dx / distance
            dy = dy / distance

        projectile = Enemy_Projectile()
        projectile.center_x = self.center_x
        projectile.center_y = self.center_y

        projectile.change_x = dx * ENEMY_PROJECTILE_SPEED
        projectile.change_y = dy * ENEMY_PROJECTILE_SPEED

        projectile.set_direction_texture(dx, dy)

        enemy_projectile_list.append(projectile)

    def update_texture_from_movement(self, dx, dy):
        if abs(dx) > abs(dy):
            if dx < 0:
                self.texture = self.textures[TEXTURE_LEFT]
            else:
                self.texture = self.textures[TEXTURE_RIGHT]
        else:
            if dy > 0:
                self.texture = self.textures[TEXTURE_UP]
            else:
                self.texture = self.textures[TEXTURE_DOWN]

    def patrol(self):
        if self.direction == 0:  # Droite
            self.center_x += self.speed
            self.texture = self.textures[TEXTURE_RIGHT]
        elif self.direction == 1:  # Haut
            self.center_y += self.speed
            self.texture = self.textures[TEXTURE_UP]
        elif self.direction == 2:  # Gauche
            self.center_x -= self.speed
            self.texture = self.textures[TEXTURE_LEFT]
        elif self.direction == 3:  # Bas
            self.center_y -= self.speed
            self.texture = self.textures[TEXTURE_DOWN]

        self.patrol_distance += self.speed

        if self.patrol_distance >= self.PATROL_DISTANCE:
            self.patrol_distance = 0
            self.direction = (self.direction + 1) % 4

    def pursuit(self, player):
        dx = player.center_x - self.center_x
        dy = player.center_y - self.center_y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            dx = dx / distance
            dy = dy / distance
            
        if distance < self.MIN_DISTANCE:
            self.center_x -= dx * self.speed
            self.center_y -= dy * self.speed
            self.update_texture_from_movement(-dx, -dy)
        elif distance > self.OPTIMAL_DISTANCE:
            self.center_x += dx * self.speed
            self.center_y += dy * self.speed
            self.update_texture_from_movement(dx, dy)
        else:
            self.update_texture_from_movement(dx, dy)

            



    def on_hit(self):
        # Définir la couleur en rouge (rouge = 255, vert = 0, bleu = 0)
        self.color = (255, 0, 0)
        self.hit_timer = 0.2  # Le sprite restera rouge pendant 0.2 secondes

    def update(self, player, delta_time, enemy_projectile_list, shield_list):
        dx = player.center_x - self.center_x
        dy = player.center_y - self.center_y
        distance = math.sqrt(dx**2 + dy**2)

        self.shoot_timer += delta_time
        
        if distance <= self.SHOOT_RANGE and self.shoot_timer >= self.SHOOT_INTERVAL:
            self.shoot_at_player(player, enemy_projectile_list)
            self.shoot_timer = 0
        
        if self.state == "patrouille":
            if distance <= self.DETECTION:
                self.state = "poursuite"
            else:
                self.patrol()
        elif self.state == "poursuite":
            if distance > self.DETECTION + 50:
                self.state = "patrouille"
            else:
                self.pursuit(player)
        
        # Réduire le timer du clignotement
        if self.hit_timer > 0:
            self.hit_timer -= delta_time
            if self.hit_timer <= 0:
                self.color = (255, 255, 255)  # Remettre la couleur normale



class Moblin(Archer):
    def __init__(self, enemy_type):
        super().__init__(enemy_type)
        self.attack_range = 100  # Distance à laquelle l'ennemi peut attaquer
        self.attack_cooldown = 1.0  # Temps entre chaque attaque en secondes
        self.attack_timer = 0
        self.attack_sprite = None
        self.current_direction = "down"
        self.attack_list = None  # Sera initialisé dans le jeu

    def set_attack_list(self, attack_list):
        self.attack_list = attack_list

    def take_damage(self, damage):
        """ Réduit la santé de l'ennemi lorsqu'il prend des dégâts """
        self.hp -= damage
        if self.hp <= 0:
            self.kill()  # Supprime l'ennemi s'il n'a plus de vie

    def update_direction(self, dx, dy):
        if abs(dx) > abs(dy):
            self.current_direction = "left" if dx < 0 else "right"
        else:
            self.current_direction = "up" if dy > 0 else "down"

    def update(self, player, delta_time, enemy_projectile_list, shield_list):
        dx = player.center_x - self.center_x
        dy = player.center_y - self.center_y
        distance = math.sqrt(dx**2 + dy**2)

        # Mise à jour du timer d'attaque
        if self.attack_timer > 0:
            self.attack_timer -= delta_time

        # Mise à jour de la direction face au joueur
        if distance > 0:
            self.update_direction(dx, dy)

        # Logique d'état
        if self.state == "patrouille":
            if distance <= self.DETECTION:
                self.state = "poursuite"
            else:
                self.patrol()
        elif self.state == "poursuite":
            if distance > self.DETECTION + 50:
                self.state = "patrouille"
            else:
                # Toujours poursuivre le joueur
                self.pursuit(player)
                # Et attaquer si assez proche
                if distance <= self.attack_range:
                    self.try_attack()

        # Mise à jour de la couleur après avoir été touché
        if self.hit_timer > 0:
            self.hit_timer -= delta_time
            if self.hit_timer <= 0:
                self.color = (255, 255, 255)

    def pursuit(self, player):
        dx = player.center_x - self.center_x
        dy = player.center_y - self.center_y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            dx = dx / distance
            dy = dy / distance
            
            # Se déplacer seulement si on est trop loin pour attaquer
            if distance > self.attack_range:
                self.center_x += dx * self.speed
                self.center_y += dy * self.speed
                self.update_texture_from_movement(dx, dy)
            elif distance <= self.attack_range:
                # Si on est à portée d'attaque, on s'arrête et on attaque
                self.try_attack()
            self.update_direction(dx, dy)

    def try_attack(self):
        if self.attack_timer <= 0 and self.attack_list is not None:
            # Créer le sprite d'attaque
            attack = SpearAttack(
                self.center_x,
                self.center_y,
                self.current_direction
            )
            self.attack_list.append(attack)
            self.attack_timer = self.attack_cooldown



class Chuchu(arcade.Sprite):
    """
    This class represents the Enemy on our screen.
    """

    def __init__(self, position_list):
        super().__init__()

        self.name = "chuchu"
        self.textures = []
        self.scale = ENEMY_SCALING
        self.health = 100

        # Load enemy textures (left, right, up, down)
        texture = arcade.load_texture(r"SpritesTempo/blue_chuchu_left.png")
        self.textures.append(texture)
        texture = arcade.load_texture(r"SpritesTempo/blue_chuchu_right.png")
        self.textures.append(texture)
        texture = arcade.load_texture(r"SpritesTempo/blue_chuchu_up.png")
        self.textures.append(texture)
        texture = arcade.load_texture(r"SpritesTempo/blue_chuchu_down.png")
        self.textures.append(texture)

        # Default texture
        self.texture = self.textures[TEXTURE_DOWN]

        self.position_list = position_list
        self.cur_position = 0
        self.speed = ENEMY_SPEED

    def take_damage(self, damage):
        """ Réduit la santé de l'ennemi lorsqu'il prend des dégâts """
        self.health -= damage
        if self.health <= 0:
            self.kill()  # Supprime l'ennemi s'il n'a plus de vie

    def update(self):
        """ Have the enemy follow a path and update its texture """
        start_x = self.center_x
        start_y = self.center_y

        dest_x = self.position_list[self.cur_position][0]
        dest_y = self.position_list[self.cur_position][1]

        # X and Y diff between the two
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y

        # Calculate angle to get there
        angle = math.atan2(y_diff, x_diff)

        # How far are we?
        distance = math.sqrt(x_diff ** 2 + y_diff ** 2)

        # How fast should we go? If we are close to our destination, lower our speed
        speed = min(self.speed, distance)

        # Calculate vector to travel
        change_x = math.cos(angle) * speed
        change_y = math.sin(angle) * speed

        # Update our location
        self.center_x += change_x
        self.center_y += change_y

        # Update texture based on direction
        if abs(change_x) > abs(change_y):
            if change_x < 0:
                self.texture = self.textures[TEXTURE_LEFT]
            else:
                self.texture = self.textures[TEXTURE_RIGHT]
        else:
            if change_y > 0:
                self.texture = self.textures[TEXTURE_UP]
            else:
                self.texture = self.textures[TEXTURE_DOWN]

        # If we are there, head to the next point.
        if distance <= self.speed:
            self.cur_position += 1
            if self.cur_position >= len(self.position_list):
                self.cur_position = 0