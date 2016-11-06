import pygame

class SoundHandler:
	def __init__(self):
		self.mute = False
		self.sound_shoot =  pygame.mixer.Sound('data/sound/270344__littlerobotsoundfactory__shoot-00.ogg')
		self.sound_hit_1 =  pygame.mixer.Sound('data/sound/270308__littlerobotsoundfactory__explosion-00.ogg')
		self.sound_hit_2 =  pygame.mixer.Sound('data/sound/270311__littlerobotsoundfactory__explosion-03.ogg')
		self.sound_win =  pygame.mixer.Sound('data/sound/270330__littlerobotsoundfactory__jingle-achievement-01.ogg')
		self.sound_fail =  pygame.mixer.Sound('data/sound/270328__littlerobotsoundfactory__hero-death-00.ogg')
		self.sound_gameover =  pygame.mixer.Sound('data/sound/270329__littlerobotsoundfactory__jingle-lose-00.ogg')

	def play(self,sound,stop):
		if stop is True:
			pygame.mixer.stop()
		if self.mute is False:
			sound.play()
