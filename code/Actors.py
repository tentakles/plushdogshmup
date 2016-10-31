import pygame
import random

class Actor(object):
    def __init__(self,x,y,width,height,center,actors,sound):
        self.sound = sound
        self.x = x
        self.y = y
        self.halfWidth = width/2
        self.width = width
        self.height = height
        self.actors = actors
        self.center = center
        self.done = False
        self.rect = self.sprite.get_rect()
        self.explosion_speed= 0.5
        self.hit=False
        self.explosion_radius_val= 200
        self.explosion_radius=  self.explosion_radius_val
        self.explosion_color = pygame.Color("white")
        if len(actors)>0:
            self.player = actors[0]

    def draw_explosion(self,surface):
        if self.explosion_radius <= 0:
            self.done = True
            self.hit = False
            self.explosion_radius=  self.explosion_radius_val
            return
        pygame.draw.circle(surface, self.explosion_color, (int(self.x + (self.rect.width/2)), int(self.y + (self.rect.height/2))), int(self.explosion_radius))
        self.explosion_radius -= self.explosion_speed

    def load(self,filename):
        return pygame.image.load(filename).convert_alpha()

    def update(self):
        if self.done:
            self.actors.remove(self)

    def draw(self,surface):
        self.update()
        surface.blit(self.sprite, (self.x - self.center[0],self.y))

class Actor_Derpmissile(Actor):

    def draw(self,surface):
        if self.hit:
            self.draw_explosion(surface)
            super(Actor_Derpmissile, self).update()
            return
        if (self.x < self.center[0] + self.width) and (self.x > self.center[0] - self.width):
            self.update()
            surface.blit(self.sprite, (self.x - self.center[0],self.y))

    def update(self):
        super(Actor_Derpmissile, self).update()
        if self.hit:
            return
        self.x -= 0.2
        self.rect.left = self.x - self.center[0]
        if self.y < self.player.y:
            self.y += 0.04
            self.rect.top = self.y
        else:
            self.y -= 0.04
            self.rect.top = self.y

    def __init__(self,x,y,width,height,center,actors,sound):
        self.sprite =self.load('data/derpmissile.png')
        super(Actor_Derpmissile, self).__init__(x,y,width,height,center,actors,sound)

class Actor_Derpus(Actor):
    def __init__(self,x,y,width,height,center,actors,sound):
        self.sprite =self.load('data/derpus.png')
        super(Actor_Derpus, self).__init__(x,y,width,height,center,actors,sound)

class Player(Actor):
    def __init__(self,x,y,width,height,center,actors,sound):
        self.sprite =self.load('data/sharkboat.png')
        self.knife = self.load('data/knife.png')
        super(Player, self).__init__(x,y,width,height,center,actors,sound)
        self.explosion_color = pygame.Color("red")
        self.playerInc = 0.1
        self.knifeInc = 0.2
        self.knifes = []
        self.counter =0
        self.counterMax =600
        
        self.knivePositions = [22,10,14]

    def fire(self):
        if self.counter > self.counterMax:
            self.sound.play(self.sound.sound_shoot,False)
            x = 50  + self.x
            y = random.choice(self.knivePositions) + self.y
            rect = self.knife.get_rect()
            rect.left = x
            rect.top = y
            knife = {"x":x,"y":y,"rect":rect}
            self.knifes.append(knife)
            self.counter=0
    def update(self):
        self.counter+=1
        self.rect.top = self.y
        self.rect.left = self.x
        collisionPlayer = self.rect.collidelist(self.actors[1:]) 
        if collisionPlayer>= 0:
            self.sound.play(self.sound.sound_dog_hit,False)
            self.hit = True
            self.actors[collisionPlayer+1].done=True

    def draw(self,surface):
        self.update()

        if self.hit:
            self.draw_explosion(surface)
        else:
            surface.blit(self.sprite, (self.x,self.y))
        oldKnifes = []
        for i,k in enumerate(self.knifes):
            if k['x'] > (self.width + self.x):
                oldKnifes.append(k)
            else:
                surface.blit(self.knife, (k['x'],k['y']))
                k['x'] = k['x']+self.knifeInc
                k['rect'].left = k['x']
                collisionKnife = k['rect'].collidelist(self.actors[1:]) 
                if collisionKnife>= 0:
                    oldKnifes.append(k)
                    actor = self.actors[collisionKnife+1] 
                    if not actor.hit:
                        self.sound.play(self.sound.sound_missile_hit,False)
                        actor.hit = True
                        actor.x -= self.center[0]

        self.knifes = filter(lambda x: x not in oldKnifes, self.knifes)