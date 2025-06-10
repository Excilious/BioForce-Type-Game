import math
import glm
import pygame as pg
from texture_id import ID

# opengl
MAJOR_VERSION = 3
MINOR_VERSION = 3
DEPTH_SIZE = 15

# resolution
WIN_RES = glm.vec2(1280, 720)
# WIN_RES = glm.vec2(1600, 900)

# control keys
KEYS = {
    'FORWARD': pg.K_w,
    'BACK': pg.K_s,
    'UP': pg.K_q,
    'DOWN': pg.K_e,
    'STRAFE_L': pg.K_a,
    'STRAFE_R': pg.K_d,
    'INTERACT': pg.K_f,
    'WEAPON_1': pg.K_1,
    'WEAPON_2': pg.K_2,
    'WEAPON_3': pg.K_3,
    'WEAPON_4': pg.K_4,
    'WEAPON_5': pg.K_5,
    'WEAPON_6': pg.K_6,
}

# camera
ASPECT_RATIO = WIN_RES.x / WIN_RES.y
FOV_DEG = 50
V_FOV = glm.radians(FOV_DEG)  # vertical FOV
H_FOV = 2 * math.atan(math.tan(V_FOV * 0.5) * ASPECT_RATIO)  # horizontal FOV
NEAR = 0.01
FAR = 2000.0
PITCH_MAX = glm.radians(89)

# player
MOUSE_SENSITIVITY = 0.0015
PLAYER_SIZE = 0.15
PLAYER_SPEED = 0.0045
PLAYER_ROT_SPEED = 0.003
PLAYER_HEIGHT = 0.6
PLAYER_POS = glm.vec3(1.5, PLAYER_HEIGHT, 1.5)

PLAYER_INIT_HEALTH = 100
PLAYER_INIT_AMMO = 25
PLAYER_INIT_ROCKET = 1
PLAYER_INIT_SHELLS = 5

MAX_HEALTH_VALUE = 100
MAX_AMMO_VALUE = 999
MAX_SHELL_VALUE = 999
MAX_ROCKET_VALUE = 999
#
NUM_LEVELS = 2

# colors
BG_COLOR = glm.vec3(0.0, 0.0, 0.0)

# textures
TEX_SIZE = 256
TEXTURE_UNIT_0 = 0

# walls
WALL_SIZE = 1
H_WALL_SIZE = WALL_SIZE / 2

# timer
SYNC_PULSE = 10  # ms

# ray casting
MAX_RAY_DIST = 20

# animations
ANIM_DOOR_SPEED = 0.03

# sound
MAX_SOUND_CHANNELS = 10

# number of textures
NUM_TEXTURES = len(ID)

ID.FACE = 79
ID.FACEHURT = 97
ID.FACEPAIN = 98
ID.FACEALMOSTDEAD = 99
ID.FACEDEAD = 100

ID.FACEBACK = 101
ID.EMPTY = 102

ID.SHOTGUN_ICON = 125
ID.ROCKET_ICON = 129
ID.DB_SHOTGUN_ICON = 130
ID.AMMOICON = 103
ID.SHELLICON = 126
ID.INTERMISSIONSCREEN = 104
ID.INTERMISSIONLEVEL = 105
ID.INTERMISSIONCOMP = 106
ID.INTERMISSIONBACK = 107
ID.INTERMISSIONCOLLECT = 108
ID.INTERMISSIONTIME = 109

ID.SUPERORB = 132
ID.SUPERFACE = 112

ID.DBSHOTGUN_0 = 120
ID.DBSHOTGUN_1 = 121
ID.DBSHOTGUN_2 = 122
ID.DBSHOTGUN_3 = 123
ID.DBSHOTGUN_4 = 124

ID.INTERMISSIONINFO = 110
ID.TITLEMENU = 131
ID.INTERMISSION_MAP1 = 111

ID.ROCKETPACK = 127
ID.SHELLPACK = 128
ID.FACEGODMODE = 114

# item settings
ITEM_SETTINGS = {
    ID.AMMO: {
        'scale': 0.2,
        'value': 8
    },
    ID.SUPERORB: {
        'scale': 0.4,
        'value': 1
    },
    ID.SHELLPACK: {
        'scale': 0.2,
        'value': 14
    },
    ID.ROCKETPACK: {
        'scale': 0.2,
        'value': 4
    },
    ID.MED_KIT: {
        'scale': 0.3,
        'value': 20
    },
    ID.PISTOL_ICON: {
        'scale': 1.0
    },
    ID.RIFLE_ICON: {
        'scale': 1.0
    },
    ID.REDKEY: {
        'scale': 0.9
    },
    ID.BLUEKEY:
    {
        'scale': 0.9
    },
    ID.YELLOWKEY:
    {
        'scale': 0.9
    }
}

# hud object IDs
ID.HEALTH_DIGIT_0 = 0 + NUM_TEXTURES
ID.HEALTH_DIGIT_1 = 1 + NUM_TEXTURES
ID.HEALTH_DIGIT_2 = 2 + NUM_TEXTURES
ID.AMMO_DIGIT_0 = 3 + NUM_TEXTURES
ID.AMMO_DIGIT_1 = 4 + NUM_TEXTURES
ID.AMMO_DIGIT_2 = 5 + NUM_TEXTURES
ID.FPS_DIGIT_0 = 6 + NUM_TEXTURES
ID.FPS_DIGIT_1 = 7 + NUM_TEXTURES
ID.FPS_DIGIT_2 = 8 + NUM_TEXTURES
ID.FPS_DIGIT_3 = 9 + NUM_TEXTURES
ID.LEVEL_DIGIT_0 = ID.DIGIT_0

ID.HEALTHICON = 80

HUD_SETTINGS = {
    ID.REDKEY: {
        'scale': 0.47,
        'pos': glm.vec2(0.94, -0.80),
    },
    ID.YELLOWKEY: {
        'scale': 0.47,
        'pos': glm.vec2(0.87, -0.80),
    },
    ID.BLUEKEY: {
        'scale': 0.47,
        'pos': glm.vec2(0.80, -0.80),
    },
    ID.HEALTH_DIGIT_0: {
        'scale': 0.1,
        'pos': glm.vec2(-0.78, -0.94),
    },
    ID.HEALTH_DIGIT_1: {
        'scale': 0.1,
        'pos': glm.vec2(-0.73, -0.94),
    },
    ID.HEALTH_DIGIT_2: {
        'scale': 0.1,
        'pos': glm.vec2(-0.68, -0.94),
    },
    ID.AMMO_DIGIT_0: {
        'scale': 0.1,
        'pos': glm.vec2(0.85, -0.94),
    },
    ID.AMMO_DIGIT_1: {
        'scale': 0.1,
        'pos': glm.vec2(0.90, -0.94),
    },
    ID.AMMO_DIGIT_2: {
        'scale': 0.1,
        'pos': glm.vec2(0.95, -0.94),
    },
    ID.AMMOICON: {
        'scale': 0.15,
        'pos': glm.vec2(0.78, -0.82),
    },
    ID.HEALTHICON: {
        'scale': 0.19,
        'pos': glm.vec2(0.78, -0.98),
    },
    ID.FPS_DIGIT_0: {
        'scale': 0.11,
        'pos': glm.vec2(-0.75, 0.87),
    },
    ID.FPS_DIGIT_1: {
        'scale': 0.11,
        'pos': glm.vec2(-0.68, 0.87),
    },
    ID.FPS_DIGIT_2: {
        'scale': 0.11,
        'pos': glm.vec2(-0.61, 0.87),
    },
    ID.FPS_DIGIT_3: {
        'scale': 0.11,
        'pos': glm.vec2(-0.54, 0.87),
    },
    ID.FPS: {
        'scale': 0.35,
        'pos': glm.vec2(-0.89, 0.74),
    },
    ID.YELLOW_SCREEN: {
        'scale': 4.0,
        'pos': glm.vec2(0.0, -2.0),
    },
    ID.RED_SCREEN: {
        'scale': 4.0,
        'pos': glm.vec2(0.0, -2.0),
    },
    ID.INTERMISSIONSCREEN: {
        'scale': 4.0,
        'pos': glm.vec2(0.0, -2.5),
    },
    ID.FACE: {
        'scale': 0.25,
        'pos': glm.vec2(-0.89, -0.96),
    },
    ID.FACEBACK: {
        'scale': 0.27,
        'pos': glm.vec2(-0.89, -0.95),
    },
    ID.INTERMISSIONLEVEL: {
        'scale': 0.75,
        'pos': glm.vec2(-0.3, -0.15),
    },
    ID.INTERMISSIONCOLLECT: {
        'scale': 0.75,
        'pos': glm.vec2(-0.3, -0.35),
    },
      ID.INTERMISSIONTIME: {
        'scale': 0.75,
        'pos': glm.vec2(-0.24, -0.55),
    },
    ID.LEVEL_DIGIT_0: {
        'scale': 6.45,
        'pos': glm.vec2(0.0, 0.0),
    },
    ID.INTERMISSIONCOMP: {
        'scale': 1.25,
        'pos': glm.vec2(0.0, 0.0),
    },
    ID.INTERMISSIONINFO: {
        'scale': 0.75,
        'pos': glm.vec2(0.0, -1.15),
    },
    ID.INTERMISSIONBACK: {
        'scale': 3.0,
        'pos': glm.vec2(0.0, -1.55),
    },
    ID.TITLEMENU: {
        'scale': 0.85,
        'pos': glm.vec2(0.0, 0.1),
    },
    ID.INTERMISSION_MAP1: {
        'scale': 0.60,
        'pos': glm.vec2(0.0, 0.15),
    },
}
# weapon settings
WEAPON_SCALE = 1.9
WEAPON_NUM_FRAMES = 5
WEAPON_POS = glm.vec3(0.0, -1.0, 0.0)
WEAPON_ANIM_PERIODS = 6

WEAPON_SETTINGS = {
    ID.KNIFE_0: {
        'bullet':'none',
        'ammo_consumption': 0,
        'damage': 20,
        'delayatframe':3,
        'max_dist': 2,
        'miss_probability': 0.3
    },
    ID.PISTOL_0: {
        'bullet':'ammo',
        'ammo_consumption': 1,
        'damage': 30,
        'delayatframe':-1,
        'max_dist': 10,
        'miss_probability': 0.1
    },
    ID.RIFLE_0: {
        'bullet':'ammo',
        'ammo_consumption': 1,
        'damage': 50,
        'delayatframe':-1,
        'max_dist': 30,
        'miss_probability': 0.045
    },
    ID.ROCKET_0: {
        'bullet':'rocket',
        'ammo_consumption': 1,
        'damage': 1000,
        'delayatframe':-1,
        'max_dist': 1000,
        'miss_probability': 0.045
    },
    ID.SHOTGUN_0: {
        'bullet':'shells',
        'ammo_consumption': 1,
        'damage': 80,
        'delayatframe':-1,
        'max_dist': 1000,
        'miss_probability': 0.045
    },
    ID.DBSHOTGUN_0: {
        'bullet':'shells',
        'ammo_consumption': 2,
        'damage': 160,
        'delayatframe':-1,
        'max_dist': 1000,
        'miss_probability': 0.015
    },
}

# npc settings
NPC_SETTINGS = {
    #
    ID.SOLDIER_BROWN_0: {
        'scale': glm.vec3(1.00),
        'anim_periods': 20,
        'num_frames': {
            'walk': 4, 'attack': 1, 'hurt': 2, 'death': 5
        },
        "shootduration":14,
        'state_tex_id': {
            'walk': ID.SOLDIER_BROWN_0,
            'attack': ID.SOLDIER_BROWN_0 + 5,
            'hurt': ID.SOLDIER_BROWN_0 + 6,
            'death': ID.SOLDIER_BROWN_0 + 6,
        },
        'attack_dist': 4,
        'health': 100,
        'speed': 0.002,
        'size': 0.3,
        'damage': 5,
        'hit_probability': 0.01,
        'drop_item': ID.AMMO
    },
    #
    ID.SOLDIER_BLUE_0: {
        'scale': glm.vec3(0.85),
        'anim_periods': 40,
        'num_frames': {
            'walk': 3, 'attack': 3, 'hurt': 2, 'death': 5
        },
        "shootduration":2,
        'state_tex_id': {
            'walk': ID.SOLDIER_BLUE_0,
            'attack': ID.SOLDIER_BLUE_0 + 4,
            'hurt': ID.SOLDIER_BLUE_0 + 6,
            'death': ID.SOLDIER_BLUE_0 + 6,
        },
        'attack_dist': 7,
        'health': 150,
        'speed': 0.0045,
        'size': 0.6,
        'damage': 7,
        'hit_probability': 0.0015,
        'drop_item': ID.AMMO
    },
    #
    ID.RAT_0: {
        'scale': glm.vec3(1.0),
        'anim_periods': 12,
        'num_frames': {
            'walk': 4, 'attack': 3, 'hurt': 2, 'death': 5
        },
        "shootduration":14,
        'state_tex_id': {
            'walk': ID.RAT_0,
            'attack': ID.RAT_0 + 4,
            'hurt': ID.RAT_0 + 7,
            'death': ID.RAT_0 + 7,
        },
        'attack_dist': 0.6,
        'health': 30,
        'speed': 0.0045,
        'size': 0.2,
        'damage': 2,
        'hit_probability': 0.002,
        'drop_item': None
    },
}
