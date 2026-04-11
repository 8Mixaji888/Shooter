#Создай собственный Шутер!

from pygame import *
from random import randint

display.init()
mixer.init()
font.init()

clock = time.Clock()
mwWidth = 700
mwHigth = 500
account = 0
missed = 0

end_game = False
finish = False

mw = display.set_mode((mwWidth, mwHigth))
display.set_caption('Shooter')

background = transform.scale(image.load('galaxy.jpg'), (mwWidth,mwHigth))
mixer.music.load('space.ogg')
mixer.music.set_volume(0.1)
strike_effect = mixer.Sound('fire.ogg')
strike_effect.set_volume(0.1)
mixer.music.play()

class GameSprite(sprite.Sprite):
    def __init__(self, ppicture, xcor, ycor, speed=0, width=65, height=96):
        super().__init__()
        self.ppicture = transform.scale(image.load(ppicture), (width, height))
        self.rect = self.ppicture.get_rect()
        self.rect.x = xcor
        self.rect.y = ycor
        self.speed = speed
    
    def reset(self):
        mw.blit(self.ppicture, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def go(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < mwWidth-65:
            self.rect.x += self.speed

    def fire(self):
        bullet_group.add(Bullet('bullet.png', self.rect.centerx, self.rect.top, 5, 16, 20))

class Enemy(GameSprite):
    def go(self):
        global missed
        if self.rect.y < 705:
            self.rect.y += self.speed
        if self.rect.y >= 505:
            missed += 1
            self.rect.y = 0
            self.rect.x = randint(0,mwWidth-65)
            print(missed)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0 :
            self.kill()

player_ship = Player('rocket.png', 318, 404, 7)
allien_group = sprite.Group()
bullet_group = sprite.Group()
for i in range(5):
    allien_group.add(Enemy('ufo.png', randint(0,mwWidth-65), -35, randint(1,2), 75,45))
        

while not end_game:
    for e in event.get():
        if e.type == QUIT:
            end_game = True
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player_ship.fire()
                strike_effect.play()

    if not finish:
        mw.blit(background, (0,0))
        player_ship.go()
        player_ship.reset()
        for bullet in bullet_group:
            bullet.reset()
            bullet.update()
        for enemy in allien_group:
            enemy.reset()
            enemy.go()
        count = font.SysFont(None, 36).render('Счет:'+ str(account), 1, (255,255,255))
        lost = font.SysFont(None, 36).render('Пропущено:'+ str(missed), 1, (255,255,255))
        mw.blit(count, (10,20))
        mw.blit(lost, (10,56))

        collide_list = sprite.groupcollide(allien_group, bullet_group, True,True)
        for c in collide_list:
            account += 1
            allien_group.add(Enemy('ufo.png', randint(0,mwWidth-65), -35, randint(1,2), 75,45))

        if account >= 100:
            finish= True
            win_text = font.SysFont(None, 70).render("You're win", 1, (255,255,255))
            mw.blit(win_text, (mwWidth//2-130, mwHigth//2-50))

        if sprite.spritecollide(player_ship, allien_group, True) or missed >= 1:
            finish = True
            fail_text = font.SysFont(None, 70).render("You're LOSEEER", 1, (255,255,255))
            mw.blit(fail_text, (mwWidth//2-190, mwHigth//2-40))

    clock.tick(60)
    display.update()