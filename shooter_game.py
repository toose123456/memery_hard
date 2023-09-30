#Создай собственный Шутер!

from pygame import *
from random import randint
class GameSprite(sprite.Sprite):
    def __init__(self, player_image,player_x, player_y, player_speed,size_x,size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.direction = 'left'
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx, self.rect.top, -10, 10, 30)
        bullets.add(bullet)
        pass
lost = 0
score = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(80, 620)
            lost = lost + 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y = self.rect.y + self.speed
        if self.rect.y <= 0:
            self.kill()


win_width = 700
win_height = 500
window = display.set_mode(
    (win_width, win_height)
)
display.set_caption('Shooter Game')
background = transform.scale(
    image.load('galaxy.jpg'),
    (win_width, win_height)
)
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
kick = mixer.Sound('fire.ogg')
run = True
finish = False
FPS = 60
player = Player('rocket.png',randint(80, 620),400, 10, 65, 65)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(80, 620), 0, randint(1, 3),90,65)
    monsters.add(monster)
clock = time.Clock()
font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))



bullets = sprite.Group()

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN   :
            if e.key == K_SPACE:
                player.fire()
                kick.play()
    if finish != True:
        window.blit(background,(0, 0))
        player.update()
        player.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        collides = sprite.groupcollide(monsters,bullets, True, True)
        for c in collides:
            score = score +1
            monster = Enemy('ufo.png', randint(80, 620), 0, randint(1, 3),90,65)
            monsters.add(monster)
        if sprite.spritecollide(player, monsters, False) or lost>3:
            finish=True
            window.blit(lose,(200, 200))
        if score>10:
            finish=True
            window.blit(win, (200, 200))

        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose,(5,10))

        text_win = font1.render('Счет:' + str(score), 1, (255,255, 255))
        window.blit(text_win,(5,40))

    display.update()
    clock.tick(FPS)