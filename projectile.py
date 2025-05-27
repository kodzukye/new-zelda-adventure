import arcade, time

class Projectile(arcade.Sprite):
    """ Class to represent a projectile fired by the player """
    
    # Storing the textures as a class variable
    TEXTURES = [
        "SpritesTempo/light_left.png",
        "SpritesTempo/light_right.png",
        "SpritesTempo/light_up.png",
        "SpritesTempo/light_down.png"
    ]


    def __init__(self, texture_file, scale, damage = 0, cost = 0, cooldown = .1):
        # Initialize the parent class without damage, as it's not part of Sprite's constructor
        super().__init__(texture_file, scale)

        self.damage = damage
        self.cost = cost
        self.cooldown = cooldown

    def update(self, map_left=0, map_bottom=0):
        """ Move the projectile """
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Remove the projectile if it goes off-screen
        if self.right < 0 or self.top < 0:
            self.right < 0 or self.left > map_left or self.top < 0 or self.bottom > map_bottom
            self.remove_from_sprite_lists()


class LightProjectile(Projectile):
    """ Class to represent a light projectile """

    name = 'light'
    
    TEXTURES = [
        "SpritesTempo/light_left.png",
        "SpritesTempo/light_right.png",
        "SpritesTempo/light_up.png",
        "SpritesTempo/light_down.png"
    ]
    
    cost = 10
    cooldown = .5

    def __init__(self, texture_file, scale, damage = 10):
        super().__init__(texture_file, scale, damage)
        self.name = 'light'

    def update(self):
        super().update()

class PoisonProjectile(Projectile):
    """ Class to represent a fireball projectile """
    
    name = 'poison'

    TEXTURES = [
        "SpritesTempo/cyan_light_left.png",
        "SpritesTempo/cyan_light_right.png",
        "SpritesTempo/cyan_light_up.png",
        "SpritesTempo/cyan_light_down.png"
    ]
    
    cost = 20
    cooldown = .75

    def __init__(self, texture_file, scale, damage = 5):
        super().__init__(texture_file, scale, damage)

        self.name = 'poison'

        self.dot_duration = 20  # Durée totale de l'effet
        self.dot_interval = 2  # Intervalle entre les dégâts en secondes
        self.last_dot_time = None  # Dernière fois où les dégâts ont été appliqués

    def apply_damage_over_time(self, enemy):
        """ Applique les dégâts toutes les 5 secondes pendant 20 secondes """
        current_time = time.time()
        if self.last_dot_time is None:
            self.last_dot_time = current_time

        elapsed_time = current_time - self.last_dot_time

        # Applique des dégâts toutes les `dot_interval` secondes
        if elapsed_time >= self.dot_interval and self.dot_duration > 0:
            enemy.take_damage(self.damage)
            print(f"Applied {self.damage} damage to enemy, remaining duration: {self.dot_duration}")  # Debugging print
            self.last_dot_time = current_time
            self.dot_duration -= self.dot_interval

    def update(self):
        super().update()

class ExplosionProjectile(Projectile):

    name = 'explosion'
    
    TEXTURES = [
        "SpritesTempo/red_light_left.png",
        "SpritesTempo/red_light_right.png",
        "SpritesTempo/red_light_up.png",
        "SpritesTempo/red_light_down.png"
    ]
    
    cost = 33
    cooldown = 2

    def __init__(self, texture_file, scale, damage=20, ):
        super().__init__(texture_file, scale, damage)

        self.name = 'explosion'
        self.explosion_radius = 50  # Rayon de l'explosion
        self.explosion_damage = 30  # Dégâts de l'explosion

    def trigger_explosion(self, enemy_list):
        """ Crée une explosion et applique des dégâts aux ennemis à proximité """
        explosion = Explosion(self.center_x, self.center_y, self.explosion_radius, self.explosion_damage)
        explosion.apply_explosion_damage(enemy_list)
        return explosion

    def update(self):
        super().update()


class Explosion(arcade.Sprite):
    def __init__(self, center_x, center_y, damage_radius, damage_amount):
        super().__init__("SpritesTempo/large_explosion.png", scale=.75)
        self.center_x = center_x
        self.center_y = center_y
        self.damage_radius = damage_radius
        self.damage_amount = damage_amount
        self.lifespan = 0.5  # Durée d'affichage de l'explosion en secondes
        self.start_time = time.time()

    def apply_explosion_damage(self, enemy_list):
        """ Applique des dégâts aux ennemis dans la zone d'explosion """
        for enemy in enemy_list:
            # Calcule la distance entre l'explosion et l'ennemi
            distance = arcade.get_distance_between_sprites(self, enemy)
            if distance <= self.damage_radius:
                enemy.take_damage(self.damage_amount)

    def update(self):
        """ Vérifie si l'explosion doit disparaître """
        elapsed_time = time.time() - self.start_time
        if elapsed_time > self.lifespan:
            self.kill()  # Supprime l'explosion après la durée spécifiée
