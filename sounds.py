import arcade

class GameSounds:
    def __init__(self):
        # Musiques de fond
        self.wizzrobe_theme = arcade.sound.load_sound("Themes/Wizzrobe_theme.mp3")
        self.tittle_screen = arcade.sound.load_sound("Themes/title-screen-theme.mp3")
        self.ikana_theme = arcade.sound.load_sound("Themes/ikana-theme.mp3")
        self.gerudo_town = arcade.sound.load_sound("Themes/gerudo-town-theme.mp3")
        self.gerudo_bazaar = arcade.sound.load_sound("Themes/gerudo-bazaar-theme.mp3")
        self.gerudo_house = arcade.sound.load_sound("Themes/gerudo-house-theme.mp3")
        self.hyrule_field = arcade.sound.load_sound("Themes/hyrule-field-theme.mp3")
        self.tower_of_death = arcade.sound.load_sound("Themes/tower-of-death-theme.mp3")

        # Effets sonores
        self.explosion_sound = arcade.sound.load_sound("Themes/explosion1.mp3")
        self.heart_sound = arcade.sound.load_sound("Themes/heart-sound.mp3")
        self.low_heart = arcade.sound.load_sound("Themes/low-health.mp3")
        self.game_over = arcade.sound.load_sound("Themes/game-over-theme.mp3")
        self.wizzrobe_blaster = arcade.sound.load_sound("Themes/wizzrobe_blaster.mp3")


        # Gestion musique en cours
        self.current_music = None
    
    def play_music(self, music):
        if self.current_music:
            arcade.sound.stop_sound(self.current_music)
        self.current_music = arcade.sound.play_sound(music, looping=True)
        
    def stop_music(self):
        if self.current_music:
            arcade.sound.stop_sound(self.current_music)
            self.current_music = None

    def play_sfx(self, sound):
        arcade.sound.play_sound(sound)