import arcade

SCREEN_TITLE = "The Legend of Link : A New Zelda Adventure"

# Saves
SAVE_FILENAME = "saves.csv"

# Dimensions de l'écran
SCREEN_WIDTH = 1120
SCREEN_HEIGHT = 784

# Index of textures, first element faces left, second faces right
TEXTURE_LEFT = TEXTURE_LEFT_ATTACK = 0
TEXTURE_RIGHT = TEXTURE_RIGHT_ATTACK = 1
TEXTURE_UP = TEXTURE_UP_ATTACK = 2
TEXTURE_DOWN = TEXTURE_DOWN_ATTACK = 3

# Scaling
SPRITE_SCALING = 0.5
ENEMY_SCALING = 0.5
PROJECTILE_SCALING = 0.3
TILE_SCALING = 0.5
GRID_PIXEL_SIZE = (28 * TILE_SCALING)

# Projectile
PROJECTILE_SPEED = 5

# Cooldown et limites des projectiles
PROJECTILE_LIMIT = 100
PROJECTILE_REGEN = 20
PROJECTILE_COOLDOWN = 5.0

# Dégâts
SWORD_DAMAGE = 20
PROJECTILE_DAMAGE = 20

# Physique 
GRAVITY = 0

# Player
MOVEMENT_SPEED = 2

# Enemies
ENEMY_PROJECTILE_SPEED = 10
WIZZROBE_PROJECTILE_SPEED = 10
ORIGINAL_ENEMY_FILENAME = "enemy_logbook.csv"
ENEMY_FILENAME = "enemy_logbook_save.csv"
ENEMY_SPEED = 1.5

# Map files
IKANA_FILENAME = "map/ikana.tmx"
TOWER_OF_DEATH_FILENAME = "map/tower_of_death-entrance.tmx"
GERUDO_FILENAME = "map/gerudo.tmx"
GERUDO_HOUSE_FILENAME = "map/gerudo_house.tmx"
GERUDO_BAZAAR_FILENAME = "map/gerudo_bazaar.tmx"
SOUTH_WEST_HYRULE_FIELD_FILENAME = "map/south-west-hyrule-field.tmx"
TOWER_OF_DEATH_LEVEL_FILENAME = "map/tower_of_death.tmx"

MAP_FILENAMES = [IKANA_FILENAME,
                 TOWER_OF_DEATH_FILENAME,
                 GERUDO_FILENAME,
                 GERUDO_HOUSE_FILENAME,
                 GERUDO_BAZAAR_FILENAME,
                 SOUTH_WEST_HYRULE_FIELD_FILENAME,
                 TOWER_OF_DEATH_LEVEL_FILENAME,
                 ]

# Map layer options 
IKANA_LAYER_OPTIONS = {
                            "Ground": {
                                "use_spatial_hash": True,
                            },
                        }

TOWER_OF_DEATH_LAYER_OPTIONS = {
                            "Ground": {
                                "use_spatial_hash": True,
                            },
                        }
GERUDO_LAYER_OPTIONS = {
                            "Ground": {
                                "use_spatial_hash": True,
                            },
                        }
GERUDO_HOUSE_LAYER_OPTIONS = {
                            "Ground": {
                                "use_spatial_hash": True,
                            },

                        }
GERUDO_BAZAAR_LAYER_OPTIONS = {
                            "Ground": {
                                "use_spatial_hash": True,
                            },
                        },

SOUTH_WEST_HYRULE_FIELD_LAYER_OPTIONS = {
                            "Ground": {
                                "use_spatial_hash": True,
                            },
                        },

TOWER_OF_DEATH_LEVEL_LAYER_OPTION = {
                            "Ground": {
                                "use_spatial_hash": True,
                            },
                        },

MAP_LAYER_OPTIONS = [IKANA_LAYER_OPTIONS, #0
                     TOWER_OF_DEATH_LAYER_OPTIONS, #1
                     GERUDO_LAYER_OPTIONS, #2
                     GERUDO_HOUSE_LAYER_OPTIONS, #3
                     GERUDO_BAZAAR_LAYER_OPTIONS, #4
                     SOUTH_WEST_HYRULE_FIELD_LAYER_OPTIONS, #5
                     TOWER_OF_DEATH_LEVEL_LAYER_OPTION, #6
                     ]

# Map layers collisions name
ROCKS_LAYER = "Rocks"
COLLISION_LAYER = "Collision"


MAP_COLLISIONS = [ROCKS_LAYER, COLLISION_LAYER]

# Waypoints
WAYPOINTS = {"0" : (0, 1652, 2478),
             "1" : (1,),
             "2" : (2, 2408, 2226),
             "3" : (3,),
             "4" : (4, 0, 0)}