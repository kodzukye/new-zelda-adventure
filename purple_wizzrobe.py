from enemy_types import ENEMY_TYPES
from constants import *
from sounds import GameSounds
import arcade
import math


# Classe pour les boucliers
class DirectionalShield(arcade.Sprite):
    def __init__(self, mini_boss):
        super().__init__()
        self.mini_boss = mini_boss
        self.duration = 60
        self.hp = 30
        self.shield_sprites = {
            'left': r"SpritesTempo\purple_wizzrobes_shield_left.png",
            'right': r"SpritesTempo\purple_wizzrobes_shield_right.png",
            'up': r"SpritesTempo\purple_wizzrobes_shield_up_down.png",
            'down': r"SpritesTempo\purple_wizzrobes_shield_up_down.png"
        }
        self.current_direction = 'down'
        self.texture = arcade.load_texture(self.shield_sprites['down'])
        self.scale = 0.5
        
    def update(self, delta_time, player):
        # Calculer l'angle vers le joueur
        dx = player.center_x - self.mini_boss.center_x
        dy = player.center_y - self.mini_boss.center_y
        
        # Déterminer la direction dominante et positionner le bouclier
        if abs(dx) > abs(dy):
            if dx < 0:
                new_direction = 'left'
                self.center_x = self.mini_boss.center_x - 40
                self.center_y = self.mini_boss.center_y
            else:
                new_direction = 'right'
                self.center_x = self.mini_boss.center_x + 40
                self.center_y = self.mini_boss.center_y
        else:
            if dy > 0:
                new_direction = 'up'
                self.center_x = self.mini_boss.center_x
                self.center_y = self.mini_boss.center_y + 40
            else:
                new_direction = 'down'
                self.center_x = self.mini_boss.center_x
                self.center_y = self.mini_boss.center_y - 40
        
        # Mettre à jour la texture si la direction a changé
        if new_direction != self.current_direction:
            self.current_direction = new_direction
            self.texture = arcade.load_texture(self.shield_sprites[new_direction])
        
        # Mettre à jour la durée et vérifier si le bouclier doit disparaître
        self.duration -= delta_time
        if self.duration <= 0 or self.hp <= 0:
            self.remove_from_sprite_lists()
            self.mini_boss.has_active_shield = False
            self.mini_boss.shield_cooldown = 2.0


class Wizzrobes_Projectile(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.scale = 0.3  # Vous pouvez ajuster cette valeur si nécessaire
        self.textures = []

        # Chargement des textures pour chaque direction
        # Note: Vous devrez ajuster les chemins des fichiers selon votre structure de projet
        texture = arcade.load_texture(r"SpritesTempo\purple_wizzrobes_fire_left.png")
        self.textures.append(texture)
        texture = arcade.load_texture(r"SpritesTempo\purple_wizzrobes_fire_right.png")
        self.textures.append(texture)
        texture = arcade.load_texture(r"SpritesTempo\purple_wizzrobes_fire_up.png")
        self.textures.append(texture)
        texture = arcade.load_texture(r"SpritesTempo\purple_wizzrobes_fire_down.png")
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


class LaserBeam(arcade.Sprite):
    """Un laser continu plutôt que des segments"""
    def __init__(self):
        super().__init__()
        self.textures = []
        # Charger les textures pour les deux orientations
        self.textures.append(arcade.load_texture(r"SpritesTempo\purple_wizzrobe_lazer_left_right.png"))
        self.textures.append(arcade.load_texture(r"SpritesTempo\purple_wizzrobe_lazer_up_down.png"))
        self.texture = self.textures[0]
        self.width = 32  # Largeur de base
        self.height = 32  # Hauteur de base
        self.alpha = 255  # Pour l'effet de fondu
        self.hit_box = self.texture.hit_box_points

class BrimstoneLaser:
    def __init__(self, start_x, start_y, target_x, target_y):
        self.beam = LaserBeam()
        self.start_x = start_x
        self.start_y = start_y
        self.target_x = target_x
        self.target_y = target_y
        self.duration = 2.5
        self.charge_time = 1.2
        self.is_charging = True
        self.damage = 30
        self.fade_duration = 0.2
        self.current_fade = 0
        
        # Utiliser une seule texture de base
        self.beam.texture = self.beam.textures[0]
        
        # Paramètres de rotation
        self.rotation_speed = 25.0  # Degrés par seconde
        self.current_angle = 0
        self.target_angle = 0
        
        # Initialisation des valeurs
        self.update_beam_position(target_x, target_y, force_angle=True)
        
        # Effet de charge
        self.charge_particles = arcade.SpriteList()
        self.charge_scale = 0.1

    def get_target_angle(self, dx, dy):
        """Calcule l'angle cible vers le joueur"""
        return math.degrees(math.atan2(dy, dx))

    def update_angle(self, target_angle, delta_time):
        """Met à jour l'angle du laser avec une vitesse limitée"""
        # Calculer la différence d'angle
        angle_diff = (target_angle - self.current_angle + 180) % 360 - 180
        
        # Calculer le maximum de rotation possible pour ce frame
        max_rotation = self.rotation_speed * delta_time
        
        # Appliquer la rotation limitée
        if abs(angle_diff) <= max_rotation:
            self.current_angle = target_angle
        else:
            if angle_diff > 0:
                self.current_angle += max_rotation
            else:
                self.current_angle -= max_rotation
        
        # Normaliser l'angle entre -180 et 180 degrés
        self.current_angle = ((self.current_angle + 180) % 360) - 180

    def update_beam_position(self, new_target_x, new_target_y, force_angle=False):
        """Met à jour la position et l'orientation du laser depuis sa base"""
        self.target_x = new_target_x
        self.target_y = new_target_y
        
        # Calculer la différence de position
        self.dx = self.target_x - self.start_x
        self.dy = self.target_y - self.start_y
        self.distance = math.sqrt(self.dx ** 2 + self.dy ** 2)
        
        # Calculer l'angle cible
        self.target_angle = self.get_target_angle(self.dx, self.dy)
        
        if force_angle:
            self.current_angle = self.target_angle
        
        # Calculer l'angle en radians pour les calculs de position
        angle_rad = math.radians(self.current_angle)
        
        # Configurer le laser
        self.beam.width = self.distance
        self.beam.height = 75
        
        # Positionner la base du laser au point de départ (boss)
        # et étendre le laser dans la direction de l'angle actuel
        self.beam.center_x = self.start_x + (self.distance/2) * math.cos(angle_rad)
        self.beam.center_y = self.start_y + (self.distance/2) * math.sin(angle_rad)
        self.beam.angle = self.current_angle

        self.beam.hit_box = [
            [-self.beam.width/2, -self.beam.height/2],
            [self.beam.width/2, -self.beam.height/2],
            [self.beam.width/2, self.beam.height/2],
            [-self.beam.width/2, self.beam.height/2]
        ]

    def update_charge_effect(self, delta_time):
        if self.is_charging:
            self.charge_scale = min(4, self.charge_scale + delta_time * 0.8)
            
            charge_sprite = arcade.Sprite(
                r"SpritesTempo\purple_wizzrobe_down.png",
                scale=self.charge_scale
            )
            charge_sprite.center_x = self.start_x
            charge_sprite.center_y = self.start_y
            charge_sprite.alpha = 150
            self.charge_particles.append(charge_sprite)
            
            for particle in self.charge_particles:
                particle.alpha -= 2
                if particle.alpha <= 0:
                    particle.remove_from_sprite_lists()

    def update(self, delta_time, player_x, player_y):
        if self.is_charging:
            self.update_charge_effect(delta_time)
            self.charge_time -= delta_time
            if self.charge_time <= 0:
                self.is_charging = False
                self.beam.alpha = 255
        else:
            # Calculer le nouvel angle cible
            dx = player_x - self.start_x
            dy = player_y - self.start_y
            target_angle = self.get_target_angle(dx, dy)
            
            # Mettre à jour l'angle avec la vitesse de rotation limitée
            self.update_angle(target_angle, delta_time)
            
            # Mettre à jour la position du laser
            self.update_beam_position(player_x, player_y)
            
            self.duration -= delta_time
            if self.duration <= 0:
                self.current_fade += delta_time
                fade_ratio = self.current_fade / self.fade_duration
                self.beam.alpha = max(0, int(255 * (1 - fade_ratio)))
                
                if self.current_fade >= self.fade_duration:
                    return True
        return False

    def draw(self):
        if self.is_charging:
            self.charge_particles.draw()
        else:
            self.beam.draw()




# Classe du MiniBoss
class Wizzrobe(arcade.Sprite):
    def __init__(self, enemy_type):

        self.enemy_data = ENEMY_TYPES["purple_wizzrobe"]
        super().__init__(self.enemy_data["sprites"]["down"], self.enemy_data["scale"])
        
        # Initialisation des attributs de base
        self.hp = self.enemy_data["hp"]
        self.max_hp = self.enemy_data["hp"]
        self.detection = self.enemy_data["detection"]
        self.optimal_distance = self.enemy_data["optimal_distance"]
        self.min_distance = self.enemy_data["min_distance"]
        self.shoot_range = self.enemy_data["shoot_range"]
        self.PATROL_DISTANCE = self.enemy_data["patrol_distance"]
        self.speed = self.enemy_data["speed"]
        self.base_shoot_interval = self.enemy_data["shoot_interval"]
        self.shoot_interval = self.base_shoot_interval
    

        # Variables de gestion du temps
        self.time_since_last_shot = 0
        self.hit_timer = 0


        self.shield_cooldown = 0
        self.has_active_shield = False
        self.shield = None

        self.active_laser = None
        self.laser_cooldown = 5.0
        self.laser_timer = 0

        # Ajouter un état pour l'attaque laser
        self.is_firing_laser = False

        # État et direction
        self.state = "patrouille"
        self.direction = 0
        self.patrol_distance = 0

        self.shoot_timer = 0

        # Forme étoile
        self.star_texture = arcade.load_texture(r"SpritesTempo/purple_wizzrobes_star_form.png")


        # Variables pour le pattern de transformation
        self.attacks_until_transform = 5  # Se transforme tous les X attaques
        self.attack_counter = 0
        self.hits_taken = 0
        self.hits_for_transform = 3  # Se transforme après avoir pris X coups
        
        # Variables de contrôle de la transformation
        self.star_form_duration = 2.0  # Durée en forme étoile
        self.transform_cooldown = 15.0  # Temps minimum entre les transformations
        self.transform_timer = 0
        self.current_state = "normal"
        self.transform_cooldown_timer = 0
        self.is_transforming = False

        
        # Chargement des textures
        self.textures = []
        for direction in ['left', 'right', 'up', 'down']:
            texture = arcade.load_texture(self.enemy_data['sprites'][direction])
            self.textures.append(texture)

        
        # Variables pour la forme étoile
        self.is_star_form = False  # booléen pour l'état étoile
        self.normal_textures = self.textures.copy()  # Sauvegarde des textures normales

        # gestion de la musique
        self.sounds = GameSounds()
        self.musique_en_cours = False

        

        # Chargement de la texture étoile
        try:
            self.star_texture = arcade.load_texture(r"SpritesTempo/purple_wizzrobes_star_form.png")
        except Exception as e:
            print(f"Error loading star texture: {e}")
        
        self.current_texture_index = TEXTURE_DOWN
        self.texture = self.textures[self.current_texture_index]

        self.previous_texture = None
        self.previous_state = None
        

    def update_texture_from_movement(self, dx, dy):
        if not self.is_star_form:
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

    def take_damage(self, damage):
        """ Réduit la santé de l'ennemi lorsqu'il prend des dégâts """
        self.hp -= damage
        if self.hp <= 0:
            if self.musique_en_cours:
                self.sounds.stop_music()
                self.musique_en_cours = False
            self.kill()  # Supprime l'ennemi s'il n'a plus de vie


    def patrol(self):
        """Gère le comportement de patrouille du mini-boss."""
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
        """Gère le comportement de poursuite du mini-boss."""
        dx = player.center_x - self.center_x
        dy = player.center_y - self.center_y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            dx /= distance
            dy /= distance

        
        if distance > self.optimal_distance:  # Distance pour avancer
            self.center_x += dx * self.speed
            self.center_y += dy * self.speed
            self.update_texture_from_movement(dx, dy)
        else:  # Rester dans la position actuelle
            self.update_texture_from_movement(dx, dy)
    
    def star_form(self, delta_time) :
        """Gère la transformation en étoile avec un pattern spécifique"""
        # Mettre à jour les timers
        if self.transform_cooldown_timer > 0:
            self.transform_cooldown_timer -= delta_time
            
        # Si nous sommes en cooldown, ne rien faire
        if self.transform_cooldown_timer > 0:
            return
            
        # Gérer les différents états
        if self.current_state == "normal":
            if (self.attack_counter >= self.attacks_until_transform or 
                self.hits_taken >= self.hits_for_transform):
                
                self.previous_texture = self.texture # sauvegarde de la texture avant la transformation
                self.is_transforming = True
                self.current_state = "transforming"
                self.transform_timer = 0


                # Retirer le bouclier s'il est actif
                if self.has_active_shield and self.shield:
                    self.shield.remove_from_sprite_lists()
                    self.has_active_shield = False
                    self.shield = None
                # Réinitialiser les compteurs
                self.attack_counter = 0
                self.hits_taken = 0
                
        elif self.current_state == "transforming":
            self.transform_timer += delta_time
            if self.transform_timer >= 0.5:  # Durée de la transformation
                self.is_star_form = True  # Activer la forme étoile
                self.texture = self.star_texture # affichage du sprite étoile
                self.current_state = "star_form"
                self.transform_timer = 0 # Réinitialiser le timer
                self.is_transforming = False 
                
        elif self.current_state == "star_form":
            self.transform_timer += delta_time
            if self.transform_timer >= self.star_form_duration:
                self.is_star_form = False  # Désactiver la forme étoile
                self.texture = self.previous_texture # Récupération de la texture avant transformation
                self.current_state = "normal"
                self.transform_cooldown_timer = self.transform_cooldown
                self.transform_timer = 0



    def get_current_shoot_interval(self):
        """Calcule l'intervalle de tir en fonction du pourcentage de HP restant"""
        hp_percentage = (self.hp / self.max_hp) * 100
        
        # Accélération progressive des tirs:
        # - À 100% HP: intervalle normal (base_shoot_interval)
        # - À 75% HP: 60% de l'intervalle normal
        # - À 50% HP: 50% de l'intervalle normal
        # - À 25% HP: 40% de l'intervalle normal
        # - À 10% HP: 30% de l'intervalle normal
        if hp_percentage <= 10:
            return self.base_shoot_interval * 0.3
        elif hp_percentage <= 25:
            return self.base_shoot_interval * 0.4
        elif hp_percentage <= 50:
            return self.base_shoot_interval * 0.5
        elif hp_percentage <= 75:
            return self.base_shoot_interval * 0.6
        else:
            return self.base_shoot_interval

    def shoot_at_player(self, player, projectile_list, delta_time):
        """Tirer sur le joueur s'il est dans la zone de tir"""

        if self.current_state != "normal":  # Ne peut pas attaquer en forme étoile
            return
        dx = player.center_x - self.center_x
        dy = player.center_y - self.center_y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            dx = dx / distance
            dy = dy / distance

        projectile = Wizzrobes_Projectile()
        projectile.center_x = self.center_x
        projectile.center_y = self.center_y

        projectile.change_x = dx * WIZZROBE_PROJECTILE_SPEED
        projectile.change_y = dy * WIZZROBE_PROJECTILE_SPEED

        projectile.set_direction_texture(dx, dy)

        projectile_list.append(projectile)

        self.attack_counter += 1

    def summon_shield(self, shield_list):
        """Créer un bouclier pour le mini-boss."""
        if not self.has_active_shield and self.shield_cooldown <= 0:
            self.shield = DirectionalShield(self)
            shield_list.append(self.shield)
            self.has_active_shield = True
            return True
        return False


    def shoot_brimstone_laser(self, player, delta_time):
            if self.hp <= self.enemy_data["hp"] / 2 and not self.active_laser and self.laser_timer <= 0:
                self.sounds.play_sfx(self.sounds.wizzrobe_blaster)
            # Créer un nouveau laser
                self.active_laser = BrimstoneLaser(
                    self.center_x, 
                    self.center_y,
                    player.center_x,
                    player.center_y
                )
                
                self.laser_timer = self.laser_cooldown
        
            # Mettre à jour le laser existant avec la position actuelle du joueur
            if self.active_laser:
                if self.active_laser.update(delta_time, player.center_x, player.center_y):
                    self.active_laser = None
    
    
    def is_invulnerable(self):
        """Vérifie si le Wizzrobe est actuellement invulnérable"""
        return (self.is_star_form or                  # Invulnérable en forme étoile
                self.current_state == "transforming" or # Invulnérable pendant la transformation
                self.has_active_shield)  
    
    def on_hit(self):
        if self.is_invulnerable():
            return  # Ignore les dégâts en forme étoile
        if self.current_state == "normal":
            self.hits_taken += 1
            # Définir la couleur en rouge (rouge = 255, vert = 0, bleu = 0)
            self.color = (255, 0, 0)
            self.hit_timer = 0.2  # Le sprite restera rouge pendant 0.2 secondes
    
    def on_death(self, shield_list):
        for shield in shield_list:
            shield.remove_from_sprite_lists()

        # Arrêter le laser
        if self.active_laser:
            self.active_laser = None
            self.laser_timer = 0
            self.is_firing_laser = False

        # Réinitialiser les timers d'attaque
        self.shoot_timer = 0
        self.time_since_last_shot = 0

    def update(self, player, delta_time, projectile_list, shield_list):
        """Mettre à jour le comportement du mini-boss."""
        arcade.Sprite.update(self)
        # Mettre à jour l'intervalle de tir en fonction des HP
        self.shoot_interval = self.get_current_shoot_interval()

        distance_to_player = arcade.get_distance_between_sprites(self, player)
        dx = player.center_x - self.center_x
        dy = player.center_y - self.center_y
        distance = math.sqrt(dx**2 + dy**2)

        # Ajouter au début de la méthode update
        if self.hp <= 0:
            self.on_death(shield_list)
            return  # Sortir immédiatement si le boss est mort

        # Gestion des timers
        if self.shield_cooldown > 0:
            self.shield_cooldown -= delta_time
        if self.laser_timer > 0:
            self.laser_timer -= delta_time
        if self.transform_cooldown > 0:
            self.transform_cooldown -= delta_time
        
        self.shoot_timer += delta_time

        

        # ------------- Vérification du Laser AVANT tout mouvement -------------
        # Si le laser est actif, le boss reste immobile
        if self.active_laser:
            self.is_firing_laser = True
            # Orienter le boss vers le joueur pendant le tir
            self.update_texture_from_movement(dx, dy)
            # Mise à jour du laser
            if self.active_laser.update(delta_time, player.center_x, player.center_y):
                self.active_laser = None
                self.is_firing_laser = False
            return  # Sortir IMMÉDIATEMENT si le laser est actif

        # Si pas de laser actif, on continue avec le comportement normal
        self.is_firing_laser = False


        

        # ------------- Comportement Normal -------------
        # Gestion du changement d'état
        if distance_to_player <= self.detection:
            self.state = "poursuite"
        elif distance_to_player > self.detection + 50:
            self.state = "patrouille"

        # Mise à jour du comportement selon l'état
        if not self.is_star_form:
            if self.state == "patrouille":
                self.patrol()
            elif self.state == "poursuite":
                self.pursuit(player)


        # Gérer la transformation en étoile
        self.star_form(delta_time)
        
        # Si en forme étoile, continuer à suivre le joueur mais ne pas attaquer
        if self.current_state in ["transforming", "star_form"]:
            dx = player.center_x - self.center_x
            dy = player.center_y - self.center_y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > 0:
                dx = dx / distance
                dy = dy / distance
            
                star_form_optimal_distance = self.optimal_distance * 0.75  # Distance plus courte que normale mais pas collé
                speed = self.speed * 1.5  # Un peu plus rapide en étoile
                
                # Si trop loin ou trop près, ajuster la position
                if distance > star_form_optimal_distance + 20:
                    # Se rapprocher
                    self.center_x += dx * speed
                    self.center_y += dy * speed
                elif distance < star_form_optimal_distance - 20:
                    # S'éloigner
                    self.center_x -= dx * speed
                    self.center_y -= dy * speed
                
                # Ajouter un léger mouvement circulaire
                angle = math.atan2(dy, dx)
                orbit_speed = speed * 0.5
                self.center_x += math.cos(angle + math.pi/2) * orbit_speed * delta_time
                self.center_y += math.sin(angle + math.pi/2) * orbit_speed * delta_time


        # ------------- Gestion des Boucliers -------------
        if self.current_state == "normal":
            if distance_to_player <= self.min_distance and not self.has_active_shield and self.shield_cooldown <= 0:
                self.summon_shield(shield_list)

        for shield in shield_list:
            if isinstance(shield, DirectionalShield):
                if shield.duration <= 0:
                    shield.remove_from_sprite_lists()
                    self.has_active_shield = False
                if distance_to_player >= self.min_distance and self.has_active_shield:
                    shield.remove_from_sprite_lists()
                    self.has_active_shield = False

        # ------------- Gestion des Attaques -------------
        if self.hp <= self.enemy_data["hp"] / 2 and self.is_star_form == True:
            # Sous 50% HP, utilise le laser sous forme étoile
            self.shoot_brimstone_laser(player, delta_time)
            
            # Attaque normale si pas de laser
            if not self.active_laser and distance <= self.shoot_range and self.shoot_timer >= self.shoot_interval:
                self.shoot_at_player(player, projectile_list, delta_time)
                self.shoot_timer = 0
        else:
            # Au-dessus de 50% HP, uniquement l'attaque normale
            if distance <= self.shoot_range and self.shoot_timer >= self.shoot_interval:
                self.shoot_at_player(player, projectile_list, delta_time)
                self.shoot_timer = 0

        
        # ------------- Gestion des Dégâts -------------
        if self.hit_timer > 0:
            self.hit_timer -= delta_time
            if self.hit_timer <= 0:
                self.color = (255, 255, 255)

        if self.hp <= 0:
            self.on_death(shield_list)

        
        # ------Gestion de la musique ------

        if self.state == "poursuite" and not self.musique_en_cours:
            self.sounds.play_music(self.sounds.wizzrobe_theme)
            self.musique_en_cours = True
        elif self.state != "poursuite" and self.musique_en_cours:
            # Arrêter la musique quand on ne poursuit plus
            self.sounds.stop_music()
            self.musique_en_cours = False