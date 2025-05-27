import arcade
from constants import *
from enemy import Chuchu, Archer, Enemy_Projectile, Moblin
from enemy_types import ENEMY_TYPES
from purple_wizzrobe import Wizzrobe, DirectionalShield
from constants import ENEMY_FILENAME

class EnemyManagement:
    def __init__(self, filename=ORIGINAL_ENEMY_FILENAME):
        # Définit le fichier qui gere l'apparition des ennemies
        self.filename = filename
        self.read_file()

    def read_file(self):
        with open(self.filename, 'r') as f:
            
            # Séparation des colonnes du csv des enemies
            # genre - type - x_pos - y_pos - map - alive
            self.enemies_info = f.read().split('\n')
            self.enemies_info = self.enemies_info[1:]
            self.enemy_list = []
            for enemy in self.enemies_info:
                if enemy != '':
                    info = enemy.split(',')
                    self.id = info[0]
                    self.genre = info[1]
                    self.type = info[2] 
                    self.x = info[3]
                    self.y = info[4]
                    self.map = info[5]
                    self.alive = info[6]
                    self.enemy_list.append([self.id, self.genre, self.type, self.x, self.y, self.map, self.alive])


    def spawn_enemy(self, archer_list, chuchu_list, wizzrobe_list, melee_list, map_index):

        for enemy in self.enemy_list:
            
            # Verifie que l'enemie correspond à la correcte map
            # Et qu'il soit toujours en vie
            if int(enemy[5]) == map_index and enemy[6] == "true":

                # Type Archer
                if enemy[1] == "Archer":
                    e = Archer(ENEMY_TYPES[enemy[2]])
                    e.id = enemy[0] # Pour gerer la mort
                    e.center_x = float(enemy[3])
                    e.center_y = float(enemy[4])
                    archer_list.append(e)  

                # Type Chuchu
                if enemy[1] == "Chuchu":
                    position_list = [
                        [float(enemy[3]) - 100, float(enemy[4]) - 100],
                        [float(enemy[3]) + 100, float(enemy[4]) - 100],
                        [float(enemy[3]) + 100, float(enemy[4]) + 100],
                        [float(enemy[3]) - 100, float(enemy[4]) + 100]
                        ]
                    e = Chuchu(position_list)
                    e.id = enemy[0] # Pour gerer la mort
                    e.center_x = position_list[0][0]
                    e.center_y = position_list[0][1]
                    chuchu_list.append(e)     
            
                # Type Wizzrobe
                if enemy[1] == "Wizzrobe":
                    e = Wizzrobe(enemy[2])
                    e.id = enemy[0] # Pour gerer la mort
                    e.center_x = float(enemy[3])
                    e.center_y = float(enemy[4])
                    wizzrobe_list.append(e)
                
                # Type Melee Enemy
                if enemy[1] == "Moblin":
                    e = Moblin(ENEMY_TYPES[enemy[2]])
                    e.id = enemy[0] # Pour gerer la mort
                    e.center_x = float(enemy[3])
                    e.center_y = float(enemy[4])
                    melee_list.append(e)

        
        return [archer_list, chuchu_list, wizzrobe_list, melee_list]
    
    def death(self, id):
        # valeur de la colonne alive devient false
        self.enemy_list[int(id)-1][6] = "false"

    def save_file(self):
        # Sauvegarde les modifications dans le fichier
        self.filename = ENEMY_FILENAME
        with open(self.filename, 'w') as f:
            f.writelines('id,genre,type,x_pos,y_pos,map,alive' + '\n')
            for el in self.enemy_list:
                e = el[0] + ',' + el[1] + ',' + el[2] + ',' + el[3] + ',' + el[4] + ',' + el[5] + ',' + el[6] + '\n'
                f.writelines(e)

    def reset_file(self):
        # Reinitialise le fichier de sauvegardes des enemies à l'etat initiale
        with open(ORIGINAL_ENEMY_FILENAME, 'r') as fr:
            self.enemies_info = fr.read().split('\n')
            self.enemies_info = self.enemies_info[1:]
            self.enemy_list = []
            for enemy in self.enemies_info:
                if enemy != '':
                    info = enemy.split(',')
                    self.id = info[0]
                    self.genre = info[1]
                    self.type = info[2] 
                    self.x = info[3]
                    self.y = info[4]
                    self.map = info[5]
                    self.alive = info[6]
                    self.enemy_list.append([self.id, self.genre, self.type, self.x, self.y, self.map, self.alive])

        with open(ENEMY_FILENAME, 'w') as fw:
            fw.writelines('id,genre,type,x_pos,y_pos,map,alive' + '\n')
            for el in self.enemy_list:
                e = el[0] + ',' + el[1] + ',' + el[2] + ',' + el[3] + ',' + el[4] + ',' + el[5] + ',' + el[6] + '\n'
                fw.writelines(e)


    def check_enemies_dunjon(self, index = 1):
        # Sert a verifier si tous les enemies d'une map sont mort

        for enemy in self.enemy_list:
            # Map au choix
            if enemy[5] == index:
                if enemy[6] == "false": # Pas alive
                    continue
                else:
                    return False # Au moins un enemie en vie
        
        return True # Tous les ennemis sont morts
                