from constants import *
from projectile import *

class SaveManagement:
    def __init__(self, filename) -> None:
        self.filename = filename
        self.read_file()

    def read_file(self):
        with open(self.filename, 'r') as f:
            
            # Séparation des colonnes du csv des enemies
            # number - map - player_x - player_y - last_player_x - last_player_y - pv,sword - projectile - enemy_file
            self.saves_info = f.read().split('\n')
            self.saves_info = self.saves_info[1:]
            self.saves = []
            for info in self.saves_info:
                if info == '': continue
                info = info.split(',')
                self.number = int(info[0])
                self.map = int(info[1])
                self.player_x = float(info[2])
                self.player_y = float(info[3])
                self.last_player_x = float(info[4])
                self.last_player_y = float(info[5])
                self.pv = int(info[6])

                if info[7] == "False":
                    self.sword = False
                else:
                    self.sword = True

                if info[8] == 'light':
                    self.projectile = LightProjectile
                elif info[8] == "poison":
                    self.projectile = PoisonProjectile
                else:
                    self.projectile = ExplosionProjectile
                
                if info[9] == 'original' or info[9] == ORIGINAL_ENEMY_FILENAME:
                    self.enemy_file = ORIGINAL_ENEMY_FILENAME
                else:
                    self.enemy_file = ENEMY_FILENAME

                self.saves.append(
                    [
                        self.number, self.map, self.player_x, self.player_y,
                        self.last_player_x, self.last_player_y, self.pv,
                        self.sword, self.projectile, self.enemy_file
                    ]
                )

    def reset_file(self):
        with open(self.filename, 'w') as f:
            f.write("number,map,player_x,player_y,last_player_x,last_player_y,pv,sword,projectile,enemy_file\n0,2,2408,2226,0,0,300,False,light,original")
        
        self.read_file()

    def save_file(self, map, player_x, player_y, last_player_x, last_player_y, pv, sword, projectile, enemy_file):
        self.map = map
        self.player_x = player_x
        self.player_y = player_y
        self.last_player_x = last_player_x
        self.last_player_y = last_player_y
        self.pv = pv
        self.sword = sword
        self.projectile = projectile
        self.enemy_file = ENEMY_FILENAME

        self.saves.append(
                    [
                        self.number, self.map, self.player_x, self.player_y,
                        self.last_player_x, self.last_player_y, self.pv,
                        self.sword, self.projectile, self.enemy_file
                    ]
                )
        with open(self.filename, 'a') as f:
            f.write(f"\n{int(len(self.saves) - 1)},{self.map},{self.player_x},{self.player_y},{self.last_player_x},{self.last_player_y},{self.pv},{self.sword},{self.projectile},{self.enemy_file}")

    def load_file(self, index = -1):
        self.map = self.saves[index][1]
        self.player_x = self.saves[index][2]
        self.player_y = self.saves[index][3]
        self.last_player_x = self.saves[index][4]
        self.last_player_y = self.saves[index][5]
        self.pv = self.saves[index][6]
        self.sword = self.saves[index][7]
        self.projectile = self.saves[index][8]
        self.enemy_file = self.saves[index][9]
        return self.saves[index]