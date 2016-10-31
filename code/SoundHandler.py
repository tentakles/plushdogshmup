import pygame

class SoundHandler:
	def __init__(self):

		self.sound_shoot =  pygame.mixer.Sound('data/sound/270344__littlerobotsoundfactory__shoot-00.wav')
		self.sound_dog_hit =  pygame.mixer.Sound('data/sound/270308__littlerobotsoundfactory__explosion-00.wav')
		self.sound_missile_hit =  pygame.mixer.Sound('data/sound/270311__littlerobotsoundfactory__explosion-03.wav')
		self.mute = False
		self.sound_win =  pygame.mixer.Sound('data/sound/270330__littlerobotsoundfactory__jingle-achievement-01.wav')
		self.sound_fail =  pygame.mixer.Sound('data/sound/270329__littlerobotsoundfactory__jingle-lose-00.wav')

	def play(self,sound,stop):
		if stop is True:
			pygame.mixer.stop()
		if self.mute is False:
			sound.play()
