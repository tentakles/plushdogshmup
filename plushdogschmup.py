from pytmx.util_pygame import load_pygame
from code.Actors import *
from code.SoundHandler import *

import pygame
import pyscroll
import pyscroll.data
import collections
import logging

from pygame.locals import *

import pyscroll.orthographic

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

class Shooter:

    def gameover_screen(self):
        self.sound.play(self.sound.sound_gameover,True)
        gameover_screen = self.load('data/gameover_screen.png')
        while True:	
            self.screen.blit(gameover_screen, (0,0))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                        #self.selectLevelScreen()
                        #self.gameLoop()
                    if event.key == pygame.K_RETURN:
                        return True
                        #self.gameLoop()
                        #pygame.display.set_caption("plush dog's sokoban ")
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            clock = pygame.time.Clock()
            fps = 30.
            clock.tick(fps*2)

    def load(self,filename):
        return pygame.image.load(filename).convert_alpha()

    def __init__(self, width,height):
        self.BLACK = ( 0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.normalFont = pygame.font.Font('freesansbold.ttf', 16)
        self.screen = pygame.display.set_mode((width, height))
        self.icon =  pygame.image.load('data/icon.gif')
        pygame.display.set_icon(self.icon)
        self.sound = SoundHandler()

        self.width=width
        self.height=height

        self.oneup_offset_x =10
        self.oneup_offset_y =10
        self.oneup_margin =40

        self.sprites={}

        self.sprites["sharkboat"] = self.load('data/sharkboat.png')
        self.sprites["sharkboat_hit"] = self.load('data/sharkboat_hit.png')
        self.sprites["knife"] = self.load('data/knife.png')
        self.sprites["derpmissile"] = self.load('data/derpmissile.png')
        self.sprites["derpuss_1"] = self.load('data/derpuss_1.png')
        self.sprites["derpuss_2"] = self.load('data/derpuss_2.png')
        self.sprites["1up"] = self.load('data/1up.png')

        self.levels = ["data/level_01.tmx"]

        self.init_level(0)

		# true when running
        self.running = False

    def init_level(self,level):
        # load data from pytmx
        
        tmx_data = load_pygame(self.levels[level])
        self.level = level

        #todo : init scrollspeed from level array
        self.scrollspeed = 0.025

        # create new data source
        map_data = pyscroll.data.TiledMapData(tmx_data)
        # create new renderer
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        self.center = [self.width/2,0]

        self.actorSpawns = next(map_data.visible_object_layers)

        self.actors = []
        self.player = Player(0,self.height/2,self.width,self.height,self.center,self.actors,self.sound,self.sprites)
        self.actors.append(self.player)

        self.levelLength = self.map_layer.map_rect[2]
        self.lastCenter = self.levelLength - (self.width/2)

    def draw(self):
        self.map_layer.draw(self.screen, self.screen.get_rect())
        for actor in self.actors:
            actor.draw(self.screen)

        for i in range(0,self.player.lifes):
            x = self.oneup_offset_x + i* self.oneup_margin
            self.screen.blit(  self.sprites["1up"], (x ,self.oneup_offset_y))

        return
        textRender = self.normalFont.render('Num actors: ' + str(len(self.actors)),True, self.WHITE, self.BLACK)
        textRect =  textRender.get_rect()
        self.screen.blit(textRender, textRect)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                break
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                    break
					
        pressed = pygame.key.get_pressed()
        if pressed[K_UP] and self.player.y>0:
            self.player.y -= self.player.playerInc
        elif pressed[K_DOWN] and self.player.y+self.player.rect.height<self.height:
             self.player.y += self.player.playerInc
        if pressed[K_LEFT] and self.player.x>0:
            self.player.x -= self.player.playerInc
        elif pressed[K_RIGHT] and self.player.x+self.player.rect.width<self.width:
            self.player.x += self.player.playerInc
        if pressed[K_SPACE]:
            self.player.fire()

    def update(self, td):
        self.last_update_time = td

        if self.player.lifes < 0:
            restart = self.gameover_screen()

            if restart:
                self.init_level(self.level )  
                #todo fixme
                #only init lelvel
            else:
                self.return_to_menu=True
        usedActorSpawns = []
        for actorSpawn in self.actorSpawns:
            if actorSpawn.x < self.center[0] + self.width/2:
                x  =  actorSpawn.x+self.width/2 - self.center[0]
                if actorSpawn.type=='missile':
                    self.actors.append(Actor_Derpmissile(x ,actorSpawn.y,self.width,self.height,self.scrollspeed,self.actors,self.sound,self.sprites))
                if actorSpawn.type=='derpuss':
                    self.actors.append(Actor_Derpuss(x,actorSpawn.y,self.width,self.height,self.scrollspeed,self.actors,self.sound,self.sprites))              
                usedActorSpawns.append(actorSpawn)

        self.actorSpawns = list(filter(lambda x: x not in usedActorSpawns, self.actorSpawns))

        if self.map_layer.view_rect.centerx < self.lastCenter:
            self.center[0] += self.scrollspeed
            self.map_layer.center(self.center)

    def run(self):
        clock = pygame.time.Clock()
        self.running = True
        fps = 30.
        fps_log = collections.deque(maxlen=20)
   
        try:
            while self.running:
                # somewhat smoother way to get fps and limit the framerate
                clock.tick(fps*2)

                try:
                    fps_log.append(clock.get_fps())
                    fps = sum(fps_log)/len(fps_log)
                    dt = 1/fps
                except ZeroDivisionError:
                    continue

                self.handle_input()
                self.update(dt)
                self.draw()
                pygame.display.flip()

        except KeyboardInterrupt:
            self.running = False

if __name__ == "__main__":
    import sys
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('plushdog shooter')

    try:
        shooter = Shooter(640, 480)
        shooter.run()
    except:
        pygame.quit()
        raise
