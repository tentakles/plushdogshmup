import pygame
import random

class Actor(object):
    def __init__(self,x,y,width,height,center,actors,sound,sprites):
        self.sprites = sprites
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
        self.dead=False
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

    def update(self):
        if self.done or self.x - self.center[0] < -self.rect.width:
            self.actors.remove(self)

    def draw(self,surface):
        if self.dead:
            self.draw_explosion(surface)
            self.update()
            surface.blit(self.sprite, (self.x - self.center[0],self.y))
            return

        if self.hit:      
            if self.lifes ==0:
                self.x -= self.center[0]
                self.dead=True
                self.sound.play(self.sound.sound_dog_hit,False)
            else:
                self.lifes -= 1
                self.hit = False
                self.sound.play(self.sound.sound_missile_hit,False)

        self.update()
        surface.blit(self.sprite, (self.x - self.center[0],self.y))

class Actor_Derpmissile(Actor):

    def __init__(self,x,y,width,height,center,actors,sound,sprites):
        self.sprite =sprites[2]
        super(Actor_Derpmissile, self).__init__(x,y,width,height,center,actors,sound,sprites)
        self.lifes=1
        self.ySpeed = 0.07
        self.xSpeed = 0.2

    def update(self):
        super(Actor_Derpmissile, self).update()
        if self.hit:
            return
        self.x -= self.xSpeed
        self.rect.left = self.x - self.center[0]
        if self.y < self.player.y:
            self.y += self.ySpeed
            self.rect.top = self.y
        else:
            self.y -= self.ySpeed
            self.rect.top = self.y

class Actor_Derpuss(Actor):
    def __init__(self,x,y,width,height,center,actors,sound,sprites):
        self.sprite = sprites[3]
        self.yPosList = [0,3,6,8,10,11,12,12,11,10,8,6,3,0,-3,-6,-8,-10,-11,-12,-12,-11,-10,-8,-6,-3]
        self.yPosLen = len(self.yPosList)
        self.yPos = random.randint(0,self.yPosLen-1)
        self.baseY = y
        self.aniCountMax = 400
        self.aniCount = 0
        super(Actor_Derpuss, self).__init__(x,y,width,height,center,actors,sound,sprites)
        self.lifes=2

    def update(self):
        super(Actor_Derpuss, self).update()
        if self.hit:
            return
        self.rect.left = self.x - self.center[0]
        self.rect.top = self.y
        self.aniCount += 1

        if self.aniCount % 50 ==0:
            self.y = self.baseY + self.yPosList[self.yPos] *2
            self.yPos+=1
            if self.yPos == self.yPosLen:
                self.yPos=0

        if self.aniCount == self.aniCountMax:
            self.aniCount =0
            if self.sprite is self.sprites[3]:
                self.sprite = self.sprites[4]
            else:
                self.sprite = self.sprites[3]

class Player(Actor):
    def __init__(self,x,y,width,height,center,actors,sound,sprites):
        self.sprite =sprites[0]
        self.knife = sprites[1]
        super(Player, self).__init__(x,y,width,height,center,actors,sound,sprites)
        self.explosion_color = pygame.Color("red")
        self.playerInc = 0.1
        self.knifeInc = 0.2
        self.knifes = []
        self.counter =0
        self.counterMax =600    
        self.knivePositions = [22,10,14]
        self.lifes =2

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
                        actor.hit = True
<<<<<<< HEAD
                        actor.x -= self.center[0]

        self.knifes = list(filter(lambda x: x not in oldKnifes, self.knifes))
=======
 
        self.knifes = filter(lambda x: x not in oldKnifes, self.knifes)
>>>>>>> origin/master
