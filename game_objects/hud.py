from meshes.quad_mesh import QuadMesh
from game_objects.game_object import GameObject
from settings import *


class HUDObject:
    def __init__(self, hud, tex_id):
        self.tex_id = tex_id
        self.pos = glm.vec3(HUD_SETTINGS[tex_id]['pos'], 0)
        self.rot = 0
        #
        hud.objects.append(self)
        #
        scale = HUD_SETTINGS[tex_id]['scale']
        self.scale = glm.vec3(scale / ASPECT_RATIO, scale, 0)
        #
        self.m_model = GameObject.get_model_matrix(self)


class HUD:
    def __init__(self, eng):
        self.eng = eng
        self.app = eng.app
        #
        self.objects = []
        self.maps = [ID.INTERMISSION_MAP1]
        #
        self.IntermissionComp = HUDObject(self,ID.INTERMISSIONLEVEL)
        self.Intermissiontitle = HUDObject(self,ID.INTERMISSIONCOMP)
        self.Intermissionmaps = HUDObject(self,self.maps[0])
        self.Intermissionitem = HUDObject(self,ID.INTERMISSIONCOLLECT)
        self.Intermissiontime = HUDObject(self,ID.INTERMISSIONTIME)

        self.Intermissioninfo = HUDObject(self,ID.INTERMISSIONINFO)
        self.health = HUDObject(self, ID.HEALTHICON)
        #self.ammo = HUDObject(self, ID.AMMOICON)
        self.face = HUDObject(self,ID.FACE)
        #self.back = HUDObject(self,ID.FACEBACK)

        self.title = HUDObject(self,ID.TITLEMENU)
        self.IntermissionBack = HUDObject(self, ID.INTERMISSIONBACK)
        self.Intermission = HUDObject(self,ID.INTERMISSIONSCREEN)

        self.redkeycard = HUDObject(self,ID.REDKEY)
        self.bluekeycard = HUDObject(self,ID.BLUEKEY)
        self.yellowkeycard = HUDObject(self,ID.YELLOWKEY)
        #
        self.ammo_digit_0 = HUDObject(self, ID.AMMO_DIGIT_0)
        self.ammo_digit_1 = HUDObject(self, ID.AMMO_DIGIT_1)
        self.ammo_digit_2 = HUDObject(self, ID.AMMO_DIGIT_2)
        #
        self.health_digit_0 = HUDObject(self, ID.HEALTH_DIGIT_0)
        self.health_digit_1 = HUDObject(self, ID.HEALTH_DIGIT_1)
        self.health_digit_2 = HUDObject(self, ID.HEALTH_DIGIT_2)
        self.digits = [0, 0, 0]

    def do_intermission_clear(self,IsIntermisson):
        self.health.tex_id = (IsIntermisson == True and ID.EMPTY) or ID.HEALTHICON
        #self.ammo.tex_id = (IsIntermisson == True and ID.EMPTY) or ID.AMMOICON
        self.face.tex_id = (IsIntermisson == True and ID.EMPTY) or ID.FACE
        #self.back.tex_id = (IsIntermisson == True and ID.EMPTY) or ID.FACEBACK

        self.ammo_digit_0.tex_id = (IsIntermisson == True and ID.EMPTY) or ID.AMMO_DIGIT_0
        self.ammo_digit_1.tex_id = (IsIntermisson == True and ID.EMPTY) or ID.AMMO_DIGIT_1
        self.ammo_digit_2.tex_id = (IsIntermisson == True and ID.EMPTY) or ID.AMMO_DIGIT_2
        self.health_digit_0.tex_id = (IsIntermisson == True and ID.EMPTY) or ID.HEALTH_DIGIT_0
        self.health_digit_1.tex_id = (IsIntermisson == True and ID.EMPTY) or ID.HEALTH_DIGIT_1
        self.health_digit_2.tex_id = (IsIntermisson == True and ID.EMPTY) or ID.HEALTH_DIGIT_2
        self.IntermissionBack.tex_id = (IsIntermisson == True and ID.INTERMISSIONBACK) or ID.EMPTY
        self.Intermission.tex_id = (IsIntermisson == True and ID.INTERMISSIONSCREEN) or ID.EMPTY 
        self.Intermissiontitle.tex_id = (IsIntermisson == True and ID.INTERMISSIONCOMP) or ID.EMPTY 
        self.Intermissionitem.tex_id = (IsIntermisson == True and ID.INTERMISSIONCOLLECT) or ID.EMPTY 
        self.Intermissiontime.tex_id = (IsIntermisson == True and ID.INTERMISSIONTIME) or ID.EMPTY 
        self.IntermissionComp.tex_id = (IsIntermisson == True and ID.INTERMISSIONLEVEL) or ID.EMPTY
        self.Intermissioninfo.tex_id = (IsIntermisson == True and ID.INTERMISSIONINFO) or ID.EMPTY
        self.Intermissionmaps.tex_id = (IsIntermisson == True and self.maps[self.eng.player_attribs.num_level-1]) or ID.EMPTY


    def update_digits(self, value):
        value = min(value, 999)
        self.digits[2] = value % 10
        #
        value //= 10
        self.digits[1] = value % 10
        #
        value //= 10
        self.digits[0] = value % 10

    def update(self):
        if (self.eng.player.Intermission): return
        if (self.eng.player.weapon_id != ID.KNIFE_0):
            if (WEAPON_SETTINGS[self.eng.player.weapon_id]['bullet'] == 'ammo'):
                self.update_digits(self.eng.player.ammo)
                self.health.tex_id = ID.AMMOICON
            elif (WEAPON_SETTINGS[self.eng.player.weapon_id]['bullet'] == 'shells'):
                self.update_digits(self.eng.player.shells)
                self.health.tex_id = ID.SHELLICON
            elif (WEAPON_SETTINGS[self.eng.player.weapon_id]['bullet'] == 'rocket'):
                self.update_digits(self.eng.player.rocket)
                self.health.tex_id = ID.HEALTHICON
            self.ammo_digit_0.tex_id = self.digits[0] + ID.DIGIT_0
            self.ammo_digit_1.tex_id = self.digits[1] + ID.DIGIT_0
            self.ammo_digit_2.tex_id = self.digits[2] + ID.DIGIT_0
        else:
            self.ammo_digit_0.tex_id = ID.EMPTY
            self.ammo_digit_1.tex_id = ID.EMPTY
            self.ammo_digit_2.tex_id = ID.EMPTY

        # health
        self.update_digits(self.eng.player.health)
        self.health_digit_0.tex_id = self.digits[0] + ID.DIGIT_0
        self.health_digit_1.tex_id = self.digits[1] + ID.DIGIT_0
        self.health_digit_2.tex_id = self.digits[2] + ID.DIGIT_0

        if (self.eng.player.goldkey == None):
            self.redkeycard.tex_id = ID.EMPTY
        elif (self.eng.player.goldkey == 1):
            self.redkeycard.tex_id = ID.REDKEY

        if (self.eng.player.silverkey == None):
            self.bluekeycard.tex_id = ID.EMPTY
        elif (self.eng.player.silverkey == 1):
            self.bluekeycard.tex_id = ID.BLUEKEY

        if (self.eng.player.bronzekey == None):
            self.yellowkeycard.tex_id = ID.EMPTY
        elif (self.eng.player.bronzekey == 1):
            self.yellowkeycard.tex_id = ID.YELLOWKEY
