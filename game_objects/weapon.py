from game_objects.game_object import GameObject
from meshes.quad_mesh import QuadMesh
from settings import *


class Weapon:
    def __init__(self, eng):
        self.eng = eng
        self.app = eng.app

        # refer to the player
        self.player = self.eng.player
        self.weapon_id = self.player.weapon_id
        self.player.weapon_instance = self
        #
        self.pos = WEAPON_POS
        self.rot = 0
        self.scale = glm.vec3(WEAPON_SCALE / ASPECT_RATIO, WEAPON_SCALE, 0)
        self.m_model = GameObject.get_model_matrix(self)
        #
        self.frame = 0
        self.anim_counter = 0
        self.weapon_anim_trig = WEAPON_ANIM_PERIODS
        self.doframe = False
        self.frameint =0
        self.chainsawactive = False

    def update(self):

        if self.player.is_shot and self.app.anim_trigger:
            self.anim_counter += 1
            self.frameint += 1
            if self.anim_counter == self.weapon_anim_trig:
                self.anim_counter = 0
                if (self.weapon_id == ID.KNIFE_0):
                    if (self.frameint >= 200):
                        self.frame += 1
                        self.frameint =0
                        self.chainsawactive = False
                    if (self.frame != 3):
                        self.chainsawactive = True
                        self.frame += 1
                else:
                    self.frame += 1


                if self.frame == WEAPON_NUM_FRAMES:
                    self.frame = 0
                    self.player.is_shot = False

    def render(self):
        self.set_uniforms()
        self.mesh.render()
