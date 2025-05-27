# camera.py
import arcade

class Camera:
    def __init__(self, screen_width, screen_height):
        self.camera = arcade.Camera(screen_width, screen_height)
        self.viewport_width = screen_width
        self.viewport_height = screen_height

    def center_on(self, target, end_map_right=0, end_map_top=0):
        # Centre la caméra sur la cible (par exemple, le joueur)
        screen_center_x = target.center_x - (self.viewport_width / 2)
        screen_center_y = target.center_y - (self.viewport_height / 2)

        # Don't let camera travel past map
        #left
        if screen_center_x < 0:
            screen_center_x = 0
        #bottom
        if screen_center_y < 0:
            screen_center_y = 0
        #right
        if screen_center_x >= end_map_right - self.viewport_width:
            screen_center_x = end_map_right - self.viewport_width
        #top
        if screen_center_y >= end_map_top - self.viewport_height:
            screen_center_y = end_map_top - self.viewport_height
        
        # si map plus petite que la fenetre
        if end_map_right <= self.viewport_width and screen_center_x >= end_map_right - self.viewport_width:
            screen_center_x = (end_map_right - self.viewport_width) / 2
        if end_map_top <= self.viewport_height and screen_center_y >= end_map_top - self.viewport_height:
            screen_center_y = (end_map_top - self.viewport_height) / 2



        self.camera.move_to((screen_center_x, screen_center_y))

    def use(self):
        # Active la caméra pour dessiner la vue centrée
        self.camera.use()

    def get_position(self):
        # Retourne la position actuelle de la caméra
        return self.camera.position