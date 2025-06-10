from itertools import cycle
from camera import Camera
from settings import *
import random
from PIL import Image
import numpy as np
import moderngl as mgl
from level_map import LevelMap

Intermission = False

class PlayerAttribs:
    def __init__(self):
        self.health = PLAYER_INIT_HEALTH
        self.ammo = PLAYER_INIT_AMMO
        self.rocket = PLAYER_INIT_ROCKET
        self.shells = PLAYER_INIT_SHELLS
        self.weapons = {ID.KNIFE_0: 1, ID.PISTOL_0: 1, ID.RIFLE_0: 1,ID.ROCKET_0: 1,ID.SHOTGUN_0: 1,ID.DBSHOTGUN_0: 1}
        self.weapon_id = ID.PISTOL_0
        self.num_level = 0

    def update(self, player):
        self.health = player.health
        self.ammo = player.ammo
        self.shells = player.shells
        self.weapons = player.weapons
        self.rocket = player.rocket
        self.weapon_id = player.weapon_id


class Player(Camera):
    def __init__(self, eng, position=PLAYER_POS, yaw=0, pitch=0):
        self.app = eng.app
        self.eng = eng
        self.sound = eng.sound
        self.play = eng.sound.play
        super().__init__(position, yaw, pitch)

        # these maps will update when instantiated LevelMap
        self.door_map, self.wall_map, self.item_map = None, None, None

        # attribs
        self.health = self.eng.player_attribs.health
        self.ammo = self.eng.player_attribs.ammo
        self.shells = self.eng.player_attribs.shells
        self.rocket = self.eng.player_attribs.rocket
        #
        self.tile_pos: Tuple[int, int] = None

        self.PlayerSpeed = PLAYER_SPEED

        # weapon
        self.weapons = self.eng.player_attribs.weapons
        self.weapon_id = self.eng.player_attribs.weapon_id
        self.weapon_cycle = cycle(self.eng.player_attribs.weapons.keys())
        #
        self.inputsequance = ""
        self.is_shot = False
        self.initial = self.position.y
        self.doneinit = False
        self.oldhealth = 0
        #
        self.goldkey = 1
        self.silverkey = None
        self.bronzekey = None
        self.Intermission = False
        self.overcharge = False
        self.overchargepower = 0
        self.godmode = True
        self.debounce = False


    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            # door interaction
            if event.key == KEYS['INTERACT']:
                self.interact_with_door()

            # switch weapon by keys
            if event.key == KEYS['WEAPON_1']:
                self.switch_weapon(weapon_id=ID.KNIFE_0)
            elif event.key == KEYS['WEAPON_2']:
                self.switch_weapon(weapon_id=ID.PISTOL_0)
            elif event.key == KEYS['WEAPON_3']:
                self.switch_weapon(weapon_id=ID.RIFLE_0)
            elif event.key == KEYS['WEAPON_4']:
                self.switch_weapon(weapon_id=ID.ROCKET_0)
            elif event.key == KEYS['WEAPON_5']:
                self.switch_weapon(weapon_id=ID.SHOTGUN_0)
            elif event.key == KEYS['WEAPON_6']:
                self.switch_weapon(weapon_id=ID.DBSHOTGUN_0)
                

        # weapon by mouse wheel
        if event.type == pg.MOUSEWHEEL:
            weapon_id = next(self.weapon_cycle)
            if self.weapons[weapon_id]:
                self.switch_weapon(weapon_id=weapon_id)

        # shooting
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.do_shot()

    def update(self):
        if (self.overcharge):
            self.overchargepower += 1

        if (self.overchargepower >= 7000):
            self.play(self.sound.powerdown)
            self.overchargepower = 0
            self.overcharge = False
            SYNC_PULSE = 10
            self.eng.scene.hud.face.tex_id = ID.FACE
            self.PlayerSpeed /= 2
            self.health = self.oldhealth
            self.oldhealth = 0

        self.mouse_control()
        self.keyboard_control()
        super().update()
        #
        self.check_health()
        self.update_tile_position()
        self.pick_up_item()

    def check_health(self):
        if (self.Intermission): 
            self.eng.scene.hud.face.tex_id = ID.EMPTY 
            return
        if (self.overcharge):
            self.eng.scene.hud.face.tex_id = ID.SUPERFACE
        elif (self.godmode):
            self.eng.scene.hud.face.tex_id = ID.FACEGODMODE
            self.health = 999
        else:
            if (self.health <= 100 and self.health >= 75):
                self.eng.scene.hud.face.tex_id = ID.FACE
            elif (self.health <= 74 and self.health >= 50):
                self.eng.scene.hud.face.tex_id = ID.FACEHURT
            elif (self.health <= 49 and self.health >= 25):
                self.eng.scene.hud.face.tex_id = ID.FACEALMOSTDEAD
            elif (self.health <= 24 and self.health >= 0):
                self.eng.scene.hud.face.tex_id = ID.FACEDEAD

        if self.health <= 0:
            self.play(self.sound.player_death)
            #
            pg.time.wait(2000)
            self.eng.player_attribs = PlayerAttribs()
            self.eng.new_game(False)

    def check_hit_on_npc(self):
        if WEAPON_SETTINGS[self.weapon_id]['miss_probability'] > random.random():
            return None

        if npc_pos := self.eng.ray_casting.run(
                start_pos=self.position,
                direction=self.forward,
                max_dist=WEAPON_SETTINGS[self.weapon_id]['max_dist'],
                npc_to_player_flag=False
        ):
            npc = self.eng.level_map.npc_map[npc_pos]
            npc.get_damage()

    def switch_weapon(self, weapon_id):
        if (self.debounce): return
        self.debounce = True
        if self.weapons[weapon_id]:
            if (weapon_id == ID.KNIFE_0):
                self.eng.scene.hud.health.tex_id = ID.EMPTY
            else:
                self.eng.scene.hud.health.tex_id = ID.HEALTHICON
            self.weapon_instance.weapon_id = self.weapon_id = weapon_id
        self.debounce = False

    def do_shot(self):
        global Intermission
        if (Intermission):
            self.play(self.sound.player_attack[ID.PISTOL_0])
            pg.time.wait(600)
            self.eng.scene.hud.do_intermission_clear(False)
            self.eng.new_game(False)
            Intermission = False
            return 
            
        if self.weapon_id == ID.KNIFE_0:
            self.is_shot = True
            self.check_hit_on_npc()
            #
            self.play(self.sound.player_attack[ID.KNIFE_0])

        elif WEAPON_SETTINGS[self.weapon_id]['bullet'] == 'ammo':
            consumption = WEAPON_SETTINGS[self.weapon_id]['ammo_consumption']
            if not self.is_shot and self.ammo >= consumption:
                self.is_shot = True
                self.check_hit_on_npc()
                #
                self.ammo -= consumption
                self.ammo = max(0, self.ammo)
                #
                self.play(self.sound.player_attack[self.weapon_id])
        elif WEAPON_SETTINGS[self.weapon_id]['bullet'] == 'shells':
            consumption = WEAPON_SETTINGS[self.weapon_id]['ammo_consumption']
            if not self.is_shot and self.shells >= consumption:
                self.is_shot = True
                self.check_hit_on_npc()
                #
                self.shells -= consumption
                self.shells = max(0, self.shells)
                #
                self.play(self.sound.player_attack[self.weapon_id])
        elif WEAPON_SETTINGS[self.weapon_id]['bullet'] == 'rocket':
            consumption = WEAPON_SETTINGS[self.weapon_id]['ammo_consumption']
            if not self.is_shot and self.rocket >= consumption:
                self.is_shot = True
                self.check_hit_on_npc()
                #
                self.rocket -= consumption
                self.rocket = max(0, self.rocket)
                #
                self.play(self.sound.player_attack[self.weapon_id])


    def update_tile_position(self):
        self.tile_pos = int(self.position.x), int(self.position.z)

    def pick_up_item(self):
        if self.tile_pos not in self.item_map:
            return None

        item = self.item_map[self.tile_pos]
        #
        if item.tex_id == ID.MED_KIT:
            self.health += ITEM_SETTINGS[ID.MED_KIT]['value']
            self.health = min(self.health, MAX_HEALTH_VALUE)
        #
        elif item.tex_id == ID.SHELLPACK:
            self.shells += ITEM_SETTINGS[ID.SHELLPACK]['value']
            self.shells = min(self.shells,MAX_SHELL_VALUE)
        elif item.tex_id == ID.ROCKETPACK:
            self.rocket += ITEM_SETTINGS[ID.ROCKETPACK]['value']
            self.rocket = min(self.rocket,MAX_ROCKET_VALUE)
        elif item.tex_id == ID.AMMO:
            self.ammo += ITEM_SETTINGS[ID.AMMO]['value']
            self.ammo = min(self.ammo, MAX_AMMO_VALUE)
        #
        elif item.tex_id == ID.PISTOL_ICON:
            if not self.weapons[ID.PISTOL_0]:
                self.weapons[ID.PISTOL_0] = 1
                self.switch_weapon(weapon_id=ID.PISTOL_0)
        #
        elif item.tex_id == ID.RIFLE_ICON:
            if not self.weapons[ID.RIFLE_0]:
                self.weapons[ID.RIFLE_0] = 1
                self.switch_weapon(weapon_id=ID.RIFLE_0)

        elif item.tex_id == ID.SHOTGUN_ICON:
            if not self.weapons[ID.SHOTGUN_0]:
                self.weapons[ID.SHOTGUN_0] = 1
                self.switch_weapon(weapon_id=ID.SHOTGUN_0)
        
        elif item.tex_id == ID.ROCKET_ICON:
            if not self.weapons[ID.ROCKET_0]:
                self.weapons[ID.ROCKET_0] = 1
                self.switch_weapon(weapon_id=ID.ROCKET_0)

        elif item.tex_id == ID.DB_SHOTGUN_ICON:
            if not self.weapons[ID.DBSHOTGUN_0]:
                self.weapons[ID.DBSHOTGUN_0] = 1
                self.switch_weapon(weapon_id=ID.DBSHOTGUN_0)
        #
        elif item.tex_id == ID.YELLOWKEY:
            self.bronzekey = 1
        elif item.tex_id == ID.BLUEKEY:
            self.silverkey = 1
        elif item.tex_id == ID.REDKEY:
            self.goldkey = 1
        elif item.tex_id == ID.SUPERORB:
            self.overcharge = True
            SYNC_PULSE = 6
            self.oldhealth = self.health
            self.PlayerSpeed *= 2
            self.health *= 2
        #
        self.play(self.sound.pick_up[item.tex_id])
        #
        del self.item_map[self.tile_pos]

    def interact_with_door(self):
        global Intermission
        pos = self.position + self.forward
        int_pos = int(pos.x), int(pos.z)

        if int_pos not in self.door_map:
            return None

        door = self.door_map[int_pos]
        #
        if self.goldkey and door.tex_id == ID.REDKEY_DOOR:
            #
            self.play(self.sound.open_door)
            # door.is_closed = not door.is_closed
            # next level
            #
            self.eng.player_attribs.update(player=self)
            self.eng.player_attribs.num_level += 1
            self.eng.player_attribs.num_level %= NUM_LEVELS

            self.eng.new_game(True)
            self.eng.scene.hud.do_intermission_clear(True)
            Intermission = True
            # self.eng.new_game()
        elif self.silverkey and door.tex_id == ID.BLUEKEY_DOOR:
            door.is_moving = True
            self.play(self.sound.open_door)
        elif self.bronzekey and door.tex_id == ID.YELLOWKEY_DOOR:
            door.is_moving = True
            self.play(self.sound.open_door)
        elif (door.tex_id != ID.REDKEY_DOOR and door.tex_id != ID.BLUEKEY_DOOR and door.tex_id != ID.YELLOWKEY_DOOR):
            door.is_moving = True
            self.play(self.sound.open_door)

    def mouse_control(self):
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        if mouse_dx:
            self.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy:
            self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)

    def keyboard_control(self):
        key_state = pg.key.get_pressed()
        vel = self.PlayerSpeed * self.app.delta_time
        next_step = glm.vec2()
        #
        if key_state[KEYS['FORWARD']]:
            next_step += self.move_forward(vel)
        if key_state[KEYS['BACK']]:
            next_step += self.move_back(vel)
        if key_state[KEYS['STRAFE_R']]:
            next_step += self.move_right(vel)
        if key_state[KEYS['STRAFE_L']]:
            next_step += self.move_left(vel)
        #
        self.move(next_step=next_step)

    def move(self, next_step):
        if not self.is_collide(dx=next_step[0]):
            self.position.x += next_step[0]

        if not self.is_collide(dz=next_step[1]):
            self.position.z += next_step[1]
        if (next_step[0] or next_step[1]):
            self.position.y = self.initial + glm.sin(self.eng.app.time * 12) / 15

    def is_collide(self, dx=0, dz=0):
        int_pos = (
            int(self.position.x + dx + (
                PLAYER_SIZE if dx > 0 else -PLAYER_SIZE if dx < 0 else 0)
                ),
            int(self.position.z + dz + (
                PLAYER_SIZE if dz > 0 else -PLAYER_SIZE if dz < 0 else 0)
                )
        )
        # check doors
        if int_pos in self.door_map:
            return self.door_map[int_pos].is_closed
        # check walls
        return int_pos in self.wall_map
