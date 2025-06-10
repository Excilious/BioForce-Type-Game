from player import Player, PlayerAttribs
from scene import Scene
from shader_program import ShaderProgram
from settings import *
from path_finding import PathFinder
from ray_casting import RayCasting
from level_map import LevelMap
from textures import Textures
from sound import Sound
import pygame as pg


class Engine:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.num_level = 0

        self.textures = Textures(self)
        self.sound = Sound()

        self.player_attribs = PlayerAttribs()
        self.player: Player = None
        self.shader_program: ShaderProgram = None
        self.scene: Scene = None

        self.level_map: LevelMap = None
        self.ray_casting: RayCasting = None
        self.path_finder: PathFinder = None
        #self.show_menu()
        self.new_game(False)

    def show_menu(self):
        self.player = Player(self)
        self.shader_program = ShaderProgram(self)
        self.level_map = LevelMap(
                self, tmx_file=f'intermission.tmx'
            )
        self.ray_casting = RayCasting(self)
        self.path_finder = PathFinder(self)
        self.scene = Scene(self)
        self.close_intermission()
        self.player.Intermission = True
        self.scene.hud.title.tex_id = ID.TITLEMENU
        self.scene.hud.face.tex_id = ID.EMPTY
        self.scene.hud.health.tex_id = ID.EMPTY
        self.scene.hud.Intermission.tex_id = ID.INTERMISSIONSCREEN
        self.scene.hud.IntermissionBack.tex_id = ID.INTERMISSIONBACK

    def close_intermission(self):
        self.scene.hud.IntermissionBack.tex_id = ID.EMPTY
        self.scene.hud.Intermission.tex_id = ID.EMPTY
        self.scene.hud.Intermissiontitle.tex_id = ID.EMPTY
        self.scene.hud.Intermissionitem.tex_id = ID.EMPTY
        self.scene.hud.Intermissiontime.tex_id = ID.EMPTY
        self.scene.hud.IntermissionComp.tex_id = ID.EMPTY
        self.scene.hud.Intermissioninfo.tex_id = ID.EMPTY
        self.scene.hud.Intermissionmaps.tex_id = ID.EMPTY

    def new_game(self,doint):
        self.player = Player(self)
        self.shader_program = ShaderProgram(self)
        if (doint == True):
            self.level_map = LevelMap(
                self, tmx_file=f'intermission.tmx'
            )
        else:
            self.level_map = LevelMap(
                self, tmx_file=f'level_{self.player_attribs.num_level}.tmx'
            )
        self.ray_casting = RayCasting(self)
        self.path_finder = PathFinder(self)
        self.scene = Scene(self)
        self.scene.hud.title.tex_id = ID.EMPTY
        self.close_intermission()
        if (doint):
            pg.mixer.music.load(self.sound.path+"intermission.mp3")
        else:
            pg.mixer.music.load(self.sound.path+'theme'+str(self.player_attribs.num_level)+".mp3")
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1)

    def update_npc_map(self):
        new_npc_map = {}
        for npc in self.level_map.npc_list:
            if npc.is_alive:
                new_npc_map[npc.tile_pos] = npc
            else:
                self.level_map.npc_list.remove(npc)
        #
        self.level_map.npc_map = new_npc_map

    def handle_events(self, event):
        self.player.handle_events(event=event)

    def update(self):
        self.update_npc_map()
        self.player.update()
        self.shader_program.update()
        self.scene.update()

    def render(self):
        self.scene.render()
