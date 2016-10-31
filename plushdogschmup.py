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
    def __init__(self, width,height):

		self.screen = pygame.display.set_mode((width, height))
		self.icon =  pygame.image.load('data/icon.gif')
		pygame.display.set_icon(self.icon)
		self.sound = SoundHandler()
		filename = "data/level_01.tmx"

		# load data from pytmx
		tmx_data = load_pygame(filename)
		self.scrollspeed = 0.025
		# create new data source
		map_data = pyscroll.data.TiledMapData(tmx_data)
		# create new renderer
		self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
		self.center = [width/2,0]

		self.actors = []
		self.player = Player(0,height/2,width,height,self.center,self.actors,self.sound)
		self.actors.append(self.player)

		#numDerpMissiles = 10

		self.levelLength = self.map_layer.map_rect[2]

		base = 1000
		for i in range(0,80):
			x= i*25 + base
			print x
			self.actors.append(Actor_Derpmissile(x,random.randint(0,450),width,height,self.center,self.actors,self.sound))

		self.lastCenter = self.levelLength - (width/2)

		# true when running
		self.running = False

    def draw(self,):
        #print str(self.map_layer.view_rect.centerx)
        #print str(self.map_layer.map_rect[2])

        self.map_layer.draw(self.screen, self.screen.get_rect())
        for actor in self.actors:
            actor.draw(self.screen)

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
        if pressed[K_UP]:
            self.player.y -= self.player.playerInc
        elif pressed[K_DOWN]:
             self.player.y += self.player.playerInc
        if pressed[K_LEFT]:
            self.player.x -= self.player.playerInc
        elif pressed[K_RIGHT]:
            self.player.x += self.player.playerInc
        if pressed[K_SPACE]:
            self.player.fire()

    def update(self, td):
        self.last_update_time = td

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
