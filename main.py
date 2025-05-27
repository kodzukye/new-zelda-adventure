import arcade
from constants import *
from pause_menu import *
from death_menu import *
from enemy import Enemy_Projectile
from enemy_types import ENEMY_TYPES
from purple_wizzrobe import Wizzrobe, DirectionalShield
from enemy_management import EnemyManagement
from save_management import SaveManagement
from player import Player
from ui import UI
from sword import Sword
from constants import *
from projectile import *
from camera import Camera
from map_management import Map
from loading_screen import LoadingView
from sounds import GameSounds




#----------------------------------- MyGame ------------------------------------------------#

class MyGame(arcade.View):
    """
    Main application class.
    """

    def __init__(self):

        self.keys_pressed = []
        self.movement_keys = [arcade.key.UP, arcade.key.Z,  # Haut
                              arcade.key.DOWN, arcade.key.S,  # Bas
                              arcade.key.LEFT, arcade.key.Q,  # Gauche
                              arcade.key.RIGHT, arcade.key.D]  # Droite

        # Call the parent class initializer
        super().__init__()

        self.fullscreen = True  # Le jeu démarre en plein écran
        self.window.set_fullscreen(self.fullscreen)  # Appliquer l'état de plein écran

        self.window.set_mouse_visible(False)

        self.is_running = False

        # Variables that will hold sprite lists
        self.player_list = None
        self.projectile_list = None
        self.enemy_easter_egg = None
        self.archer_enemy = None
        self.moblins = None
        self.wizzrobes = None
        self.wizzrobes_shield_list = None
        self.enemy_projectile_list = None
        self.explosion_list = None
        self.moblins_attack_list = None

        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

        # Set up the player info
        self.player_sprite = None
        self.ui = None  # UI pour gérer les affichages

        # Set up the mini boss info
        self.mini_boss = None

        # Our Scene Object
        self.scene = None

        # Our physics engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera = None

        self.explosion_list = None

        # gestion de la musique
        self.sounds = GameSounds()
        self.low_health_sound_playing = False
        self.low_health_sound_ref = None

    def setup(self, 
              setup_values = None,
              player_x = 1847, 
              player_y = 2672,
              map_index = 0, 
              player_pv = 300, 
              player_has_sword=False,
              last_player_x = 0, 
              last_player_y = 0,
              default_player_texture = TEXTURE_DOWN,
              player_projectile_type = LightProjectile,
              enemy_file=ENEMY_FILENAME
              ):
        """ Set up the game and initialize the variables. """

        # *** Sauvegarde des arguments pour réutilisation ultérieure ***
        if setup_values == None:
            self.setup_values = {

                "player_x": player_x,
                "player_y": player_y,
                "map_index": map_index,
                "player_pv": player_pv,
                "player_has_sword": player_has_sword,
                "last_player_x": last_player_x,
                "last_player_y": last_player_y,
                "default_player_texture": default_player_texture,
                "player_projectile_type": player_projectile_type,
                "enemy_file": enemy_file
        }
        else :
            self.setup_values = setup_values

        self.saves = SaveManagement(SAVE_FILENAME)

        self.last_player_x = self.setup_values["last_player_x"]
        self.last_player_y = self.setup_values["last_player_y"]

        # Set up the Camera
        self.camera = Camera(self.window.width, self.window.height)

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.projectile_list = arcade.SpriteList()
        self.enemy_easter_egg = arcade.SpriteList()
        self.archer_enemy = arcade.SpriteList()
        self.moblins = arcade.SpriteList()
        self.wizzrobes = arcade.SpriteList()
        self.wizzrobes_shield_list = arcade.SpriteList()
        self.wizzrobes_projectile_list = arcade.SpriteList()
        self.enemy_projectile_list = arcade.SpriteList()  # Initialisation de la liste des projectiles
        self.explosion_list = arcade.SpriteList()
        self.moblins_attack_list = arcade.SpriteList()
        
        # Set up the maps
        self.map = Map(MAP_FILENAMES, MAP_LAYER_OPTIONS, MAP_COLLISIONS)
        self.map.load_map(self.setup_values["map_index"])

        # Set up the player
        self.player_sprite = Player(game=self, default_texture=self.setup_values["default_player_texture"])
        self.player_sprite.pv = self.setup_values["player_pv"]
        self.player_sprite.update_hearts()
        self.player_sprite.projectile_type = self.setup_values['player_projectile_type']
        self.player_sprite.has_sword = self.setup_values['player_has_sword']
        self.player_sprite.center_x = self.setup_values["player_x"] #SCREEN_WIDTH + 100
        self.player_sprite.center_y = self.setup_values["player_y"] #SCREEN_HEIGHT + 100
        self.player_list.append(self.player_sprite)

        # Ajoute le joueur à la map
        self.map.scene.add_sprite("Player", self.player_sprite)

        # Set up the UI
        self.ui = UI(self.player_sprite)


        if self.map.current_map == 0:
            if not self.player_sprite.has_sword:
                self.sword_sprite = Sword()
                self.sword_sprite.center_x = 2271
                self.sword_sprite.center_y = 1072
                self.player_list.append(self.sword_sprite) 

        # Add enemies
        self.enemies = EnemyManagement(enemy_file)
        self.enemies_list = self.enemies.spawn_enemy(self.archer_enemy, self.enemy_easter_egg,
                                                        self.wizzrobes, self.moblins, 
                                                        self.map.current_map)
        
        self.archer_enemy = self.enemies_list[0]
        self.enemy_easter_egg = self.enemies_list[1]
        self.wizzrobes = self.enemies_list[2]
        self.moblins = self.enemies_list[3]


        for melee_enemy in self.moblins:
            melee_enemy.set_attack_list(self.moblins_attack_list)
            
        # Liste pour la physique du jeu
        self.physics_engine = []

        # Create the 'physics engine'
        for layer in self.map.collisions:
            self.pe = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.map.scene[layer]
        )
            self.physics_engine.append(self.pe)
        

    def restart_with_loading(self):
        """Relance le jeu avec l'écran de chargement."""
        self.sounds.stop_music()
        self.stop_all_sounds()
        loading_view = LoadingView(self.setup_values)  # *** Initialisation avec des arguments dynamiques ***
        self.window.show_view(loading_view)

    def stop_all_sounds(self):
        """Arrête tous les sons en cours"""
        # Arrêter le son de faible santé
        if self.low_health_sound_playing:
            arcade.sound.stop_sound(self.low_health_sound_ref)
            self.low_health_sound_playing = False
            
        # Arrêter la musique du boss si elle est en cours
        for wizzrobe in self.wizzrobes:
            if wizzrobe.musique_en_cours:
                wizzrobe.sounds.stop_music()
                wizzrobe.musique_en_cours = False

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        # Draw our Scene
        self.map.scene.draw()

        # Draw all the sprites.
        self.player_list.draw()
        self.enemy_easter_egg.draw()
        self.archer_enemy.draw()
        self.wizzrobes.draw()
        self.moblins.draw()

        self.projectile_list.draw()
        self.enemy_projectile_list.draw()  # Dessiner les projectiles
        self.wizzrobes_projectile_list.draw()
        self.wizzrobes_shield_list.draw()
        self.explosion_list.draw()
        self.moblins_attack_list.draw()

        # Dessiner le laser du boss s'il est actif
        for wizzrobe in self.wizzrobes:
            if wizzrobe and wizzrobe.active_laser:
                wizzrobe.active_laser.draw()

        # Activate our Camera
        self.camera.use()


        # Dessiner les éléments de l'interface utilisateur
        self.ui.draw(self.camera.get_position(), game=self)
        
    
    def on_update(self, delta_time):
        """ Movement and game logic """

        # Move the player with the physics engine

        # Gestion musique de zones

        # Ikana
        if self.map.current_map == 0 and (not self.sounds.current_music): 
            self.sounds.play_music(self.sounds.ikana_theme)

        # Tower of death
        if self.map.current_map == 1 and (not self.sounds.current_music): 
            self.sounds.play_music(self.sounds.tower_of_death)

        # Gerudo Town
        if self.map.current_map == 2 and (not self.sounds.current_music): 
            self.sounds.play_music(self.sounds.gerudo_town)

        # Gerudo House
        if self.map.current_map == 3 and (not self.sounds.current_music): 
            self.sounds.play_music(self.sounds.gerudo_house)

        # Gerudo Bazaar
        if self.map.current_map == 4 and (not self.sounds.current_music): 
            self.sounds.play_music(self.sounds.gerudo_bazaar)

        # Gerudo Town
        if self.map.current_map == 5 and (not self.sounds.current_music): 
            self.sounds.play_music(self.sounds.hyrule_field)

        #self.physics_engine_walls.update()
        for pe in self.physics_engine:
            pe.update()


        # Move the player
        self.player_sprite.update(delta_time)
        # Met à jour les autres sprites de la liste normalement
        for sprite in self.player_list:
            if sprite != self.player_sprite:
                sprite.update()

        self.enemy_easter_egg.update()
        self.projectile_list.update()
        self.enemy_projectile_list.update()
        self.moblins_attack_list.update()
        self.ui.update(delta_time)

        # Mise à jour des explosions
        self.explosion_list.update()

        # Mise à jour du mini-boss (gestion des projectiles et des gardes)
        for wizzrobe in self.wizzrobes:
            wizzrobe.update(self.player_sprite, delta_time, self.wizzrobes_projectile_list, self.wizzrobes_shield_list)

        # Mise à jour des projectiles du mini-boss
        self.wizzrobes_projectile_list.update()

        # Mise à jour des boucliers
        for shield in self.wizzrobes_shield_list:
            if isinstance(shield, DirectionalShield):
                shield.update(delta_time, self.player_sprite)

        # Centre la caméra sur le joueur
        self.camera.center_on(self.player_sprite, self.map.end_right, self.map.end_top)

        # Vérifier si le joueur touche l'épée
        if (self.map.current_map == 0) and (not self.player_sprite.has_sword) and (arcade.check_for_collision(self.player_sprite, self.sword_sprite)):
            self.player_sprite.acquire_sword()
            self.sword_sprite.kill()  # Supprimer l'épée après l'avoir ramassée

        # Vérifier les collisions des projectiles
        
        
        
        for enemy in self.archer_enemy:
            enemy.update(self.player_sprite, delta_time, self.enemy_projectile_list, None)
            
            
        for enemy in self.moblins:
            enemy.update(self.player_sprite, delta_time, None, None)


        for enemy in self.wizzrobes:
            enemy.update(self.player_sprite, delta_time, self.enemy_projectile_list, self.wizzrobes_shield_list)
        


        hits_on_player = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_projectile_list)
        for projectile in hits_on_player:
            self.player_sprite.take_damage(25)  # 25 points de dégâts par projectile
            self.player_sprite.on_hit()
            projectile.remove_from_sprite_lists()

        hits_from_wizzrobe = arcade.check_for_collision_with_list(self.player_sprite, self.wizzrobes_projectile_list)
        for projectile in hits_from_wizzrobe:
            self.player_sprite.take_damage(100)
            self.player_sprite.on_hit()
            projectile.remove_from_sprite_lists()

        for enemy_list in [self.enemy_easter_egg, self.archer_enemy, self.moblins]:
            hits_from_enemy = arcade.check_for_collision_with_list(self.player_sprite, enemy_list)
            for enemy in hits_from_enemy:
                self.player_sprite.take_damage(25)
                self.player_sprite.on_hit()

        hits_from_melee = arcade.check_for_collision_with_list(self.player_sprite, self.moblins_attack_list)
        for attack in hits_from_melee :
            self.player_sprite.take_damage(50)
            self.player_sprite.on_hit()
            

        for wizzrobe in self.wizzrobes:
            if wizzrobe.active_laser and not wizzrobe.active_laser.is_charging:
                if arcade.check_for_collision(self.player_sprite, wizzrobe.active_laser.beam):
                    self.player_sprite.take_damage(350)
                    self.player_sprite.on_hit()


        # ----- dégats à l'ennemi -----
        
        # Vérifier les collisions entre les projectiles du joueur et les boucliers
        for projectile in self.projectile_list: 
            for enemy in self.enemy_easter_egg:

                if arcade.check_for_collision(projectile, enemy):
                    if enemy.health - projectile.damage <= 0:
                        self.enemies.death(enemy.id)
                        self.enemies.save_file()
                    enemy.take_damage(projectile.damage)  # Inflige les dégâts à l'ennemi
                    self.enemies.death(enemy.id)
                    enemy.kill()
                    if isinstance(projectile, PoisonProjectile):
                        arcade.schedule(lambda dt: projectile.apply_damage_over_time(enemy), projectile.dot_interval)
                        enemy.kill()

                    # Déclencher une explosion si le projectile est de type ExplosionProjectile
                    elif isinstance(projectile, ExplosionProjectile):
                        explosion = projectile.trigger_explosion(self.enemy_easter_egg)
                        self.explosion_list.append(explosion)
                        self.sounds.play_sfx(self.sounds.explosion_sound)
                        enemy.kill()

                    projectile.kill()  # Supprimer le projectile après la collision

        # Vérifier les collisions entre les projectiles du joueur et les boucliers
        for projectile in self.projectile_list:
            for enemy in self.archer_enemy:

                if arcade.check_for_collision(projectile, enemy):
                    if enemy.hp - projectile.damage <= 0:
                        self.enemies.death(enemy.id)
                        self.enemies.save_file()
                    enemy.take_damage(projectile.damage)  # Inflige les dégâts à l'ennemi
                    enemy.on_hit()
                    if isinstance(projectile, PoisonProjectile):
                        arcade.schedule(lambda dt: projectile.apply_damage_over_time(enemy), projectile.dot_interval)

                    # Déclencher une explosion si le projectile est de type ExplosionProjectile
                    elif isinstance(projectile, ExplosionProjectile):
                        explosion = projectile.trigger_explosion(self.archer_enemy)
                        self.explosion_list.append(explosion)
                        self.sounds.play_sfx(self.sounds.explosion_sound)

                    projectile.kill()  # Supprimer le projectile après la collision

                

        # Vérifier les collisions entre les projectiles du joueur et les boucliers
        for projectile in self.projectile_list:
            for enemy in self.wizzrobes:

                if arcade.check_for_collision(projectile, enemy):
                    if not enemy.is_invulnerable():  # Vérifier l'invulnérabilité avant tout

                        if enemy.hp - projectile.damage <= 0:
                            enemy.sounds.stop_music()
                            self.enemies.death(enemy.id)
                            self.enemies.save_file()

                        enemy.take_damage(projectile.damage)  # Inflige les dégâts à l'ennemi
                        enemy.on_hit()  # Appeler la méthode pour clignoter

                        # Pour le poison, on ne l'applique que si l'ennemi n'est pas invulnérable
                        if isinstance(projectile, PoisonProjectile):
                            arcade.schedule(lambda dt: projectile.apply_damage_over_time(enemy), 
                                         projectile.dot_interval)

                        # Pour l'explosion, on ne la déclenche que si l'ennemi n'est pas invulnérable
                        elif isinstance(projectile, ExplosionProjectile):
                            explosion = projectile.trigger_explosion(self.wizzrobes)
                            self.explosion_list.append(explosion)
                            self.sounds.play_sfx(self.sounds.explosion_sound)

                    # On supprime toujours le projectile, qu'il y ait eu des dégâts ou non
                    projectile.kill()


        for projectile in self.projectile_list:
            for enemy in self.moblins:

                if arcade.check_for_collision(projectile, enemy):
                    if enemy.hp - projectile.damage <= 0:
                        self.enemies.death(enemy.id)
                        self.enemies.save_file()
                    enemy.take_damage(projectile.damage)  # Inflige les dégâts à l'ennemi
                    enemy.on_hit()
                    if isinstance(projectile, PoisonProjectile):
                        arcade.schedule(lambda dt: projectile.apply_damage_over_time(enemy), projectile.dot_interval)

                    # Déclencher une explosion si le projectile est de type ExplosionProjectile
                    elif isinstance(projectile, ExplosionProjectile):
                        explosion = projectile.trigger_explosion(self.archer_enemy)
                        self.explosion_list.append(explosion)
                        self.sounds.play_sfx(self.sounds.explosion_sound)

                    projectile.kill()  # Supprimer le projectile après la collision
                



        for projectile in self.projectile_list:
            for enemy in self.moblins:

                if arcade.check_for_collision(projectile, enemy):
                    if enemy.hp - projectile.damage <= 0:
                        self.enemies.death(enemy.id)
                        self.enemies.save_file()
                    enemy.take_damage(projectile.damage)  # Inflige les dégâts à l'ennemi
                    enemy.on_hit()
                    if isinstance(projectile, PoisonProjectile):
                        arcade.schedule(lambda dt: projectile.apply_damage_over_time(enemy), projectile.dot_interval)

                    # Déclencher une explosion si le projectile est de type ExplosionProjectile
                    elif isinstance(projectile, ExplosionProjectile):
                        explosion = projectile.trigger_explosion(self.archer_enemy)
                        self.explosion_list.append(explosion)
                        self.sounds.play_sfx(self.sounds.explosion_sound)

                    projectile.kill()  # Supprimer le projectile après la collision

                    if enemy.hp <= 0:
                        self.enemies.death(enemy.id)



        # Gestion de la mort du joueur (player's death)
        if self.player_sprite.pv == 0:
            self.stop_all_sounds()
            self.player_sprite.pv = 0
            # Sauvegarde la progression du joueur
            self.saves.save_file(self.map.current_map,
                                self.player_sprite.center_x,
                                self.player_sprite.center_y,
                                self.last_player_x,
                                self.last_player_y,
                                300,
                                self.player_sprite.has_sword,
                                self.player_sprite.projectile_type.name,
                                ENEMY_FILENAME)
            death_menu = DeathMenu(self)
            self.sounds.play_sfx(self.sounds.game_over)
            self.window.show_view(death_menu)
            return

        # gestion de la boucle du son low hp
        if self.player_sprite.pv <= 200:
            if not self.low_health_sound_playing:
                self.low_health_sound_ref = arcade.sound.play_sound(self.sounds.low_heart, looping=True)
                self.low_health_sound_playing = True
        elif self.player_sprite.pv > 200:
            if self.low_health_sound_playing:
                arcade.sound.stop_sound(self.low_health_sound_ref)
                self.low_health_sound_playing = False


        # CHANGEMENT DE MAPS

        # ikana vers tower of death
        if self.map.current_map == 0 and arcade.check_for_collision_with_list(
            self.player_sprite, self.map.scene["TOD_EntranceCollision"]
        ):
            self.enemies.save_file()

            self.saves.save_file(self.map.current_map,
                             self.player_sprite.center_x,
                             self.player_sprite.center_y,
                             self.last_player_x,
                             self.last_player_y,
                             self.player_sprite.pv,
                             self.player_sprite.has_sword,
                             self.player_sprite.projectile_type.name,
                             ENEMY_FILENAME)

            self.setup_values = {
            "player_x": 1565,
            "player_y": 60,
            "map_index": 1,
            "player_pv": self.player_sprite.pv,
            "player_has_sword": self.player_sprite.has_sword,
            "last_player_x": self.last_player_x,
            "last_player_y": self.last_player_y,
            "default_player_texture": TEXTURE_UP,
            "player_projectile_type": self.player_sprite.projectile_type,
            "enemy_file": ENEMY_FILENAME
    }
            self.restart_with_loading()

        # Tower of death vers ikana
        if self.map.current_map == 1 and arcade.check_for_collision_with_list(
            self.player_sprite, self.map.scene["TOD_ExitCollision"]
        ):
            self.enemies.save_file()

            self.saves.save_file(self.map.current_map,
                             self.player_sprite.center_x,
                             self.player_sprite.center_y,
                             self.last_player_x,
                             self.last_player_y,
                             self.player_sprite.pv,
                             self.player_sprite.has_sword,
                             self.player_sprite.projectile_type.name,
                             ENEMY_FILENAME)

            self.setup_values = {
            "player_x": 1899,
            "player_y": 3738,
            "map_index": 0,
            "player_pv": self.player_sprite.pv,
            "player_has_sword": self.player_sprite.has_sword,
            "last_player_x": self.last_player_x,
            "last_player_y": self.last_player_y,
            "default_player_texture": TEXTURE_DOWN,
            "player_projectile_type": self.player_sprite.projectile_type,
            "enemy_file": ENEMY_FILENAME
    }
            
            self.restart_with_loading()

        # Ikana vers Gerudo
        if self.map.current_map == 0 and arcade.check_for_collision_with_list(
            self.player_sprite, self.map.scene["GerudoEntranceCollision"]
        ):
            self.enemies.save_file()

            self.saves.save_file(self.map.current_map,
                             self.player_sprite.center_x,
                             self.player_sprite.center_y,
                             self.last_player_x,
                             self.last_player_y,
                             self.player_sprite.pv,
                             self.player_sprite.has_sword,
                             self.player_sprite.projectile_type.name,
                             ENEMY_FILENAME)

            self.setup_values = {
            "player_x": 80,
            "player_y": 1536,
            "map_index": 2,
            "player_pv": self.player_sprite.pv,
            "player_has_sword": self.player_sprite.has_sword,
            "last_player_x": self.last_player_x,
            "last_player_y": self.last_player_y,
            "default_player_texture": TEXTURE_RIGHT,
            "player_projectile_type": self.player_sprite.projectile_type,
            "enemy_file": ENEMY_FILENAME
    }
            self.restart_with_loading() 
        
        # Gerudo vers Ikana
        if self.map.current_map == 2 and arcade.check_for_collision_with_list(
            self.player_sprite, self.map.scene["IkanaEntranceCollision"]
        ):
            self.enemies.save_file()

            self.saves.save_file(self.map.current_map,
                             self.player_sprite.center_x,
                             self.player_sprite.center_y,
                             self.last_player_x,
                             self.last_player_y,
                             self.player_sprite.pv,
                             self.player_sprite.has_sword,
                             self.player_sprite.projectile_type.name,
                             ENEMY_FILENAME)

            self.setup_values = {
            "player_x": 3235,
            "player_y": 1536,
            "map_index": 0,
            "player_pv": self.player_sprite.pv,
            "player_has_sword": self.player_sprite.has_sword,
            "last_player_x": self.last_player_x,
            "last_player_y": self.last_player_y,
            "default_player_texture": TEXTURE_LEFT,
            "player_projectile_type": self.player_sprite.projectile_type,
            "enemy_file": ENEMY_FILENAME
    }
            self.restart_with_loading()

        # Gerudo town vers gerudo house
        if self.map.current_map == 2 and arcade.check_for_collision_with_list(
            self.player_sprite, self.map.scene["GerudoHouseCollision"]
        ):  
            self.enemies.save_file()

            self.saves.save_file(self.map.current_map,
                             self.player_sprite.center_x,
                             self.player_sprite.center_y,
                             self.last_player_x,
                             self.last_player_y,
                             self.player_sprite.pv,
                             self.player_sprite.has_sword,
                             self.player_sprite.projectile_type.name,
                             ENEMY_FILENAME)

            self.setup_values = {
            "player_x": 136,
            "player_y": 88,
            "map_index": 3,
            "player_pv": self.player_sprite.pv,
            "player_has_sword": self.player_sprite.has_sword,
            "last_player_x": self.player_sprite.center_x,
            "last_player_y": self.player_sprite.center_y - (28 * 2),
            "default_player_texture": TEXTURE_UP,
            "player_projectile_type": self.player_sprite.projectile_type,
            "enemy_file": ENEMY_FILENAME
    }
            self.restart_with_loading()

        # Gerudo house vers gerudo town
        if self.map.current_map == 3 and arcade.check_for_collision_with_list(
            self.player_sprite, self.map.scene["HouseExitCollision"]
        ):  
            self.enemies.save_file()

            self.saves.save_file(self.map.current_map,
                             self.player_sprite.center_x,
                             self.player_sprite.center_y,
                             self.last_player_x,
                             self.last_player_y,
                             self.player_sprite.pv,
                             self.player_sprite.has_sword,
                             self.player_sprite.projectile_type.name,
                             ENEMY_FILENAME)

            self.setup_values = {
            "player_x": self.last_player_x,
            "player_y": self.last_player_y,
            "map_index": 2,
            "player_pv": self.player_sprite.pv,
            "player_has_sword": self.player_sprite.has_sword,
            "last_player_x": 0,
            "last_player_y": 0,
            "default_player_texture": TEXTURE_DOWN,
            "player_projectile_type": self.player_sprite.projectile_type,
            "enemy_file": ENEMY_FILENAME
    }
            self.restart_with_loading()   

        # Gerudo town vers gerudo bazaar
        if self.map.current_map == 2 and arcade.check_for_collision_with_list(
            self.player_sprite, self.map.scene["GerudoBazaarCollision"]
        ):  
            self.enemies.save_file()

            self.saves.save_file(self.map.current_map,
                             self.player_sprite.center_x,
                             self.player_sprite.center_y,
                             self.last_player_x,
                             self.last_player_y,
                             self.player_sprite.pv,
                             self.player_sprite.has_sword,
                             self.player_sprite.projectile_type.name,
                             ENEMY_FILENAME)

            self.setup_values = {
            "player_x": 75,
            "player_y": self.player_sprite.center_y,
            "map_index": 4,
            "player_pv": self.player_sprite.pv,
            "player_has_sword": self.player_sprite.has_sword,
            "last_player_x": 0,
            "last_player_y": 0,
            "default_player_texture": TEXTURE_RIGHT,
            "player_projectile_type": self.player_sprite.projectile_type,
            "enemy_file": ENEMY_FILENAME
    }
            self.restart_with_loading()  

        # gerudo bazaar vers Gerudo town
        if self.map.current_map == 4 and arcade.check_for_collision_with_list(
            self.player_sprite, self.map.scene["GerudoTownEntranceCollision"]
        ):  
            self.enemies.save_file()

            self.saves.save_file(self.map.current_map,
                             self.player_sprite.center_x,
                             self.player_sprite.center_y,
                             self.last_player_x,
                             self.last_player_y,
                             self.player_sprite.pv,
                             self.player_sprite.has_sword,
                             self.player_sprite.projectile_type.name,
                             ENEMY_FILENAME)

            self.setup_values = {
            "player_x": 3525,
            "player_y": self.player_sprite.center_y,
            "map_index": 2,
            "player_pv": self.player_sprite.pv,
            "player_has_sword": self.player_sprite.has_sword,
            "last_player_x": 0,
            "last_player_y": 0,
            "default_player_texture": TEXTURE_LEFT,
            "player_projectile_type": self.player_sprite.projectile_type,
            "enemy_file": ENEMY_FILENAME
    }
            self.restart_with_loading()


        # gerudo town vers south west hyrule field 
        if self.map.current_map == 2 and arcade.check_for_collision_with_list(
            self.player_sprite, self.map.scene["south-west-hyrule-entrance-collision"]
        ):  
            self.enemies.save_file()

            self.saves.save_file(self.map.current_map,
                             self.player_sprite.center_x,
                             self.player_sprite.center_y,
                             self.last_player_x,
                             self.last_player_y,
                             self.player_sprite.pv,
                             self.player_sprite.has_sword,
                             self.player_sprite.projectile_type.name,
                             ENEMY_FILENAME)

            self.setup_values = {
            "player_x": self.player_sprite.center_x,
            "player_y": 75,
            "map_index": 5,
            "player_pv": self.player_sprite.pv,
            "player_has_sword": self.player_sprite.has_sword,
            "last_player_x": 0,
            "last_player_y": 0,
            "default_player_texture": TEXTURE_UP,
            "player_projectile_type": self.player_sprite.projectile_type,
            "enemy_file": ENEMY_FILENAME
    }
            self.restart_with_loading()

        # south west hyrule field vers gerudo town
        if self.map.current_map == 5 and arcade.check_for_collision_with_list(
            self.player_sprite, self.map.scene["GerudoEntranceCollision"]
        ):  
            self.enemies.save_file()

            self.saves.save_file(self.map.current_map,
                             self.player_sprite.center_x,
                             self.player_sprite.center_y,
                             self.last_player_x,
                             self.last_player_y,
                             self.player_sprite.pv,
                             self.player_sprite.has_sword,
                             self.player_sprite.projectile_type.name,
                             ENEMY_FILENAME)

            self.setup_values = {
            "player_x": self.player_sprite.center_x,
            "player_y": 3505,
            "map_index": 2,
            "player_pv": self.player_sprite.pv,
            "player_has_sword": self.player_sprite.has_sword,
            "last_player_x": 0,
            "last_player_y": 0,
            "default_player_texture": TEXTURE_DOWN,
            "player_projectile_type": self.player_sprite.projectile_type,
            "enemy_file": ENEMY_FILENAME
    }
            self.restart_with_loading()


        # tod labirhynthe to boss room
        if self.map.current_map == 1 and arcade.check_for_collision_with_list(
            self.player_sprite, self.map.scene["TOP_BossCollision"]
        ):  
            self.enemies.save_file()

            self.saves.save_file(self.map.current_map,
                             self.player_sprite.center_x,
                             self.player_sprite.center_y,
                             self.last_player_x,
                             self.last_player_y,
                             self.player_sprite.pv,
                             self.player_sprite.has_sword,
                             self.player_sprite.projectile_type.name,
                             ENEMY_FILENAME)

            self.setup_values = {
            "player_x": 352,
            "player_y": 55,
            "map_index": 6,
            "player_pv": self.player_sprite.pv,
            "player_has_sword": self.player_sprite.has_sword,
            "last_player_x": 0,
            "last_player_y": 0,
            "default_player_texture": TEXTURE_UP,
            "player_projectile_type": self.player_sprite.projectile_type,
            "enemy_file": ENEMY_FILENAME
    }
            self.restart_with_loading()

        
        # boss room to tod labirhynthe
        if self.map.current_map == 6 and arcade.check_for_collision_with_list(
            self.player_sprite, self.map.scene["ExitDunjonCollision"]
        ):  
            self.enemies.save_file()

            self.saves.save_file(self.map.current_map,
                             self.player_sprite.center_x,
                             self.player_sprite.center_y,
                             self.last_player_x,
                             self.last_player_y,
                             self.player_sprite.pv,
                             self.player_sprite.has_sword,
                             self.player_sprite.projectile_type.name,
                             ENEMY_FILENAME)

            self.setup_values = {
            "player_x": 1510,
            "player_y": 2186,
            "map_index": 1,
            "player_pv": self.player_sprite.pv,
            "player_has_sword": self.player_sprite.has_sword,
            "last_player_x": 0,
            "last_player_y": 0,
            "default_player_texture": TEXTURE_DOWN,
            "player_projectile_type": self.player_sprite.projectile_type,
            "enemy_file": ENEMY_FILENAME
    }
            self.restart_with_loading()

        
        # boss room to ikana
        if self.map.current_map == 6 and arcade.check_for_collision_with_list(
            self.player_sprite, self.map.scene["NextLevelCollision"]
        ):  
            self.enemies.save_file()

            self.saves.save_file(self.map.current_map,
                             self.player_sprite.center_x,
                             self.player_sprite.center_y,
                             self.last_player_x,
                             self.last_player_y,
                             self.player_sprite.pv,
                             self.player_sprite.has_sword,
                             self.player_sprite.projectile_type.name,
                             ENEMY_FILENAME)

            self.setup_values = {
            "player_x": 1899,
            "player_y": 3738,
            "map_index": 0,
            "player_pv": self.player_sprite.pv,
            "player_has_sword": self.player_sprite.has_sword,
            "last_player_x": 0,
            "last_player_y": 0,
            "default_player_texture": TEXTURE_DOWN,
            "player_projectile_type": self.player_sprite.projectile_type,
            "enemy_file": ENEMY_FILENAME
    }
            self.restart_with_loading()


        # print(self.player_sprite.center_x, self.player_sprite.center_y)


    def update_player_movement(self):
        """ Mettre à jour les mouvements du joueur en fonction de la dernière touche pressée. """
        # Réinitialiser les mouvements
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        # Parcourir les touches en ordre inversé (priorité à la dernière ajoutée)
        for key in reversed(self.keys_pressed):
            if key == arcade.key.UP or key == arcade.key.Z:
                self.player_sprite.change_y = MOVEMENT_SPEED
                break  # Priorité donnée, on arrête 
            elif key == arcade.key.DOWN or key == arcade.key.S:
                self.player_sprite.change_y = -MOVEMENT_SPEED
                break
            elif key == arcade.key.LEFT or key == arcade.key.Q:
                self.player_sprite.change_x = -MOVEMENT_SPEED
                break
            elif key == arcade.key.RIGHT or key == arcade.key.D:
                self.player_sprite.change_x = MOVEMENT_SPEED
                break


    def on_key_press(self, key, modifiers):
        "Called whenever a key is pressed."

        # To enter or exit fullscreen
        if key == arcade.key.ESCAPE:
            self.toggle_fullscreen()

        # To enter or exit fullscreen
        if key == arcade.key.F4:
            self.on_close()

        elif key == arcade.key.P:

            self.saves.save_file(self.map.current_map,
                             self.player_sprite.center_x,
                             self.player_sprite.center_y,
                             self.last_player_x,
                             self.last_player_y,
                             self.player_sprite.pv,
                             self.player_sprite.has_sword,
                             self.player_sprite.projectile_type.name,
                             ENEMY_FILENAME)

            for wizzrobe in self.wizzrobes:
                if wizzrobe.musique_en_cours:
                    wizzrobe.sounds.stop_music()
                    wizzrobe.musique_en_cours = False
            pause_menu = PauseMenu(self)
            self.window.show_view(pause_menu)

        # If the player presses a key, update the speed
        if key in self.movement_keys and key not in self.keys_pressed:
            self.keys_pressed.append(key)  # Ajouter seulement les touches de mouvement
            self.update_player_movement()

        # Shoot a projectile when space is pressed if there are enough points
        elif key == arcade.key.SPACE and self.ui.current_projectile_points >= self.player_sprite.projectile_type.cost:
            projectile = self.player_sprite.shoot_projectile()
            self.projectile_list.append(projectile)
            self.ui.current_projectile_points -= self.player_sprite.projectile_type.cost  # Consommer des points

        elif key == arcade.key.KEY_1 :
            self.player_sprite.projectile_type = LightProjectile
            self.player_sprite.projectile_type.name = 'light'
        elif key == arcade.key.KEY_2 :
            self.player_sprite.projectile_type = PoisonProjectile
            self.player_sprite.projectile_type.name = 'poison'
        elif key == arcade.key.KEY_3 :
            self.player_sprite.projectile_type = ExplosionProjectile  
            self.player_sprite.projectile_type.name = 'explosion'          

        elif key == arcade.key.KEY_4:
            self.player_sprite.heal(100)  # Soigne de 100 PV
            self.sounds.play_sfx(self.sounds.heart_sound)

        elif key == arcade.key.V:
            self.player_sprite.take_damage(25)  # Réduit de 25 PV


        # Attaquer un ennemi
            # Attaquer tous les ennemis
        elif key == arcade.key.E:
            # Passer la liste des ennemis à la méthode d'attaque
            all_enemies = [
            self.enemy_easter_egg,
            self.archer_enemy, 
            self.wizzrobes,
            self.moblins
        ]
            for enemy in all_enemies:
                self.player_sprite.attack(enemy)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        # If a player releases a key, zero out the speed.
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)  # Retirer seulement les touches de mouvement

        # Vérifier s'il reste des touches de mouvement enfoncées
        if self.keys_pressed:
            self.update_player_movement()
        else:
            # Aucune touche de mouvement enfoncée, arrêter le mouvement
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0

    
    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            all_enemies = [
            self.enemy_easter_egg,
            self.archer_enemy, 
            self.wizzrobes,
            self.moblins
        ]
            for enemy in all_enemies:
                self.player_sprite.attack(enemy)
            

        elif button == arcade.MOUSE_BUTTON_RIGHT and self.ui.current_projectile_points >= self.player_sprite.projectile_type.cost:
            projectile = self.player_sprite.shoot_projectile()
            self.projectile_list.append(projectile)
            self.ui.current_projectile_points -= self.player_sprite.projectile_type.cost  # Consommer des points

    def toggle_fullscreen(self):
        """Basculer entre plein écran et mode fenêtre."""
        self.fullscreen = not self.fullscreen  # Inverser l'état actuel du plein écran
        self.window.set_fullscreen(self.fullscreen)  # Appliquer le changement
    
    def on_close(self):

        # Sauvegarde la mort des ennemies
        self.enemies.save_file()

        # Sauvegarde la progression du joueur
        self.saves.save_file(self.map.current_map,
                             self.player_sprite.center_x,
                             self.player_sprite.center_y,
                             self.last_player_x,
                             self.last_player_y,
                             self.player_sprite.pv,
                             self.player_sprite.has_sword,
                             self.player_sprite.projectile_type.name,
                             ENEMY_FILENAME)
        return self.window.close()

    def on_show_view(self):
        self.is_running = True
        # print("Le jeu est maintenant lancé !")

def main():
    """ Main function """
    window = MyGame()
    window.saves = SaveManagement(SAVE_FILENAME)
    window.saves.load_file()

    # Reset before loading the main file again
    # Pour que ce soit plus simple pour vous Rhonny et Kendrick lol :))
    """window.saves.reset_file()
    window.saves.load_file()"""

    window.setup(
        map_index = window.saves.map, 
        player_x = window.saves.player_x, 
        player_y = window.saves.player_y, 
        enemy_file = window.saves.enemy_file,
        player_pv = window.saves.pv, 
        player_has_sword = window.saves.sword,
        last_player_x = window.saves.last_player_x, 
        last_player_y = window.saves.last_player_y,
        player_projectile_type = window.saves.projectile,
              )
    arcade.run()


if __name__ == "__main__":
    main()