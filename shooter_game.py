#Создай собственный Шутер!

from pygame import *
from random import randint

window = display.set_mode((800,600), RESIZABLE)
display.set_caption("мега супер шутер, который лучше квейка")
global speed
speed = 10
global lost
lost=0
global hits
hits=0
font.init()
font1=font.SysFont('Arial',24)
font2=font.SysFont('Arial',24)
font3=font.SysFont('Arial',72)
font4=font.SysFont('Arial',72)
#задай фон сцены
background = transform.scale(image.load("a.png"),(800,600))

mixer.init()
mixer.music.load('terrariya-noch_(mp3CC.biz).mp3')
mixer.music.play()
clock = time.Clock()
FPS = 60
game = True

class GameSprite(sprite.Sprite):
    def __init__(self,player_image, player_x, player_y, player_speed,width,height):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(width,height))
        self.speed=player_speed
        self.rect=self.image.get_rect()
        self.rect.x=player_x
        self.rect.y=player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))



class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

monsters = sprite.Group()
en = Enemy('ufo.png', randint(100,700), 1, randint(1,5),128,64)
monsters.add(en)

def new_enemy():
    en = Enemy('ufo.png', randint(100,700), 1, randint(1,5),128,64)
    monsters.add(en)

def new_meteors():
    met = Meteor('1.png', randint(100,700), 1, randint(1,5),128,64)
    meteors.add(met)

class Bullet(GameSprite):
    def fire(self):
        self.rect.y-=self.speed     

class Meteor(GameSprite):
    def update(self):
        self.rect.y += self.speed

meteors = sprite.Group()

player = GameSprite('rocket.png',350,500,10,100,100)
en = Enemy('ufo.png', randint(100,700), 1, randint(1,5),128,64)
bullet=Bullet('bullet.png',player.rect.x,player.rect.y,20,10,10)
met = Meteor('1.png', randint(100,700), 1, randint(1,5),128,64)
bullet.rect.x=-10
bullets=sprite.Group()
bullets.add(bullet)
#x1= 0
#y1= 600
meteors.add(met)

while game:
    clock.tick(FPS)
    window.blit(background,(0,0))
    text_lose=font1.render("Пропущенно:"+ str(lost), 1,(255,255,255))
    text_hits=font2.render("Счёт:"+ str(hits),1 ,(255,255,255))
    window.blit(text_hits,(1,25))
    window.blit(text_lose,(1,1))
    keys_pressed = key.get_pressed()
    monsters.update()
    monsters.draw(window)
    meteors.update()
    meteors.draw(window)
    bullets.update()
    bullets.draw(window)
    player.reset()
    en.reset()
    met.reset()
    bullet.reset()
    bullet.fire()

    for en in monsters:
        if sprite.collide_rect(bullet,en):
            bullet.remove(bullets)
            en.remove(monsters)
            if len(monsters) <= 7:
                new_enemy()
            hits+=1      
    for en in monsters:
        if en.rect.y>500:
            en.rect.x=randint(0,700)
            en.rect.y=0
            lost+=1
            if len(monsters) <= 2:
                new_enemy()
    for met in meteors:
        if met.rect.y>500:
            met.rect.x=randint(0,700)
            met.rect.y=0
        if len(meteors) <= 1:
                new_meteors()
    if met.rect.x == player.rect.x and met.rect.y == player.rect.y:
        global helth
        helth -= 1
    if keys_pressed[K_LEFT]:
        player.rect.x -= speed
    if keys_pressed[K_RIGHT]:
        player.rect.x += speed
    if keys_pressed[K_SPACE]:
        if bullet.rect.y>=0:
            bullet.rect.x=-10
        bullet.fire()
        bullet=Bullet('bullet.png',player.rect.x,player.rect.y,20,10,10)
        bullet.rect.x=player.rect.x+45
    if keys_pressed[K_l]:
        New_Enemy()
    for e in event.get():
        if e.type == QUIT:
            game = False
    if int(lost) == 15:
        text_lose=font3.render("Ты проиграв/n тебя скушали иноплонетяне",1,(255,255,255))
        time.delay(10)
        game = False
    if int(hits) == 50:
        text_lose=font4.render("Ты выйграл/n иноплонетяне ушли",1,(255,255,255))
        time.delay(10)
        game = False
    display.update()