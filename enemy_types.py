ENEMY_TYPES = {
    "blue_chuchu": {
        "name": "Blue ChuChu",
        "hp": 20,
        "detection": 300,
        "optimal_distance": 200,
        "min_distance": 150,
        "shoot_range": 250,
        "patrol_distance": 100,  # Ajout de la distance de patrouille
        "sprites": {
            "left": r"SpritesTempo\blue_chuchu_left.png",
            "right": r"SpritesTempo\blue_chuchu_right.png",
            "up": r"SpritesTempo\blue_chuchu_up.png",
            "down": r"SpritesTempo\blue_chuchu_down.png"
        },
        "scale": 0.5,
        "speed": 2,
        "shoot_interval": 2.0
    },

    "blue_bokoblin": {
        "name": "Blue Bokoblin",
        "hp": 100,
        "detection":300,
        "optimal_distance": 200,
        "min_distance": 150,
        "shoot_range": 250,
        "patrol_distance": 100,
        "sprites": {
            "left": r"SpritesTempo/blue_bokoblin_left.png",
            "right": r"SpritesTempo/blue_bokoblin_right.png",
            "up": r"SpritesTempo/blue_bokoblin_up.png",
            "down": r"SpritesTempo/blue_bokoblin_down.png",
        },
        "scale": 0.5,
        "speed": 2,
        "shoot_interval": 2.0
    },

    "purple_wizzrobe": {
        "name": "Purple Wizzrobe",
        "hp": 400,
        "detection": 500,
        "optimal_distance": 300,
        "min_distance": 150,
        "shoot_range": 400,
        "patrol_distance": 100,
        "sprites": {
            "left": r"SpritesTempo\purple_wizzrobe_left.png",
            "right": r"SpritesTempo\purple_wizzrobe_right.png",
            "up": r"SpritesTempo\purple_wizzrobe_up.png",
            "down": r"SpritesTempo\purple_wizzrobe_down.png",
        },
        "scale": 0.5,
        "speed": 1,
        "shoot_interval": 2.0
    },

    "red_moblin": {
        "name": "Red Moblin",
        "hp": 200,
        "detection": 250,
        "optimal_distance": 40,  # Distance très courte car c'est un ennemi de mêlée
        "min_distance": 0,       # Pas de distance minimum car il veut être au contact
        "shoot_range": 0,        # Pas de tir à distance
        "patrol_distance": 100,
        "sprites": {
            "left": r"SpritesTempo/red_moblin_left.png",
            "right": r"SpritesTempo/red_moblin_right.png",
            "up": r"SpritesTempo/red_moblin_up.png",
            "down": r"SpritesTempo/red_moblin_down.png",
        },
        "scale": 0.45,
        "speed": 3,             # Plus rapide que les autres ennemis
        "shoot_interval": 0     # Pas utilisé pour cet ennemi
    }, 
}