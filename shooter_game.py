from time import time as get_time
from pygame import *
from random import randint

font.init()
screen_size = (700,500)
sprite_size = 60
window = display.set_mode(screen_size)
bg = transform.scale( image.load("galaxy.jpg"), screen_size)


class GameSprite(sprite.Sprite):
    def __init__(self, x,y, image_name, speed, scale=1):
        super().__init__()
        self.image = transform.scale(image.load(image_name), (sprite_size//scale, sprite_size//scale))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= screen_size[1]:
            self.rect.y = 0
            self.rect.x = randint(0, screen_size[0] - sprite_size)
            missed_counter.count += 1
            missed_counter.render()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= screen_size[1]:
            self.rect.y = 0
            self.rect.x = randint(0, screen_size[0] - sprite_size)
        
class Bullet(GameSprite):
    def __init__(self, x,y, image_name, speed, scale=1, direction = 0):
        super().__init__(x,y, image_name, speed, scale)
        self.direction = direction
    def update(self):
        self.rect.y -= self.speed
        if self.direction ==1:
            self.rect.x -= self.speed
        if self.direction ==2:
            self.rect.x += self.speed

class Player (GameSprite):
    def __init__(self, x,y, image_name, speed, scale=1, lives = 5, image_live = 'heart.png'):
        super().__init__( x,y, image_name, speed, scale)
        self.last_shoot_time = 0
        self.lives = lives
        self.image_live = transform.scale(image.load(image_live), (sprite_size//scale//2, sprite_size//scale//2))
    def draw_lives(self):
        for i in range(self.lives):
            window.blit(self.image_live,(screen_size[0] - self.image_live.get_rect().width - 5 - i*self.image_live.get_rect().width, 10))


    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if key_pressed[K_d] and self.rect.x < screen_size[0] - sprite_size:
            self.rect.x += self.speed
        if key_pressed[K_SPACE] and get_time() - self.last_shoot_time > .1 and bullets_counter.count >0:
            self.shoot()
            self.last_shoot_time = get_time()
        self.draw()
        self.draw_lives()

    def shoot(self):
        bullets_counter.count -= 1

        bullets_counter.render()
        
        new_bullet1 = Bullet(x = self.rect.x, y = self.rect.y, image_name = "bullet.png", speed = 7, scale = 4, direction=1 )
        new_bullet2 = Bullet(x = self.rect.centerx - sprite_size//8 , y = self.rect.y, image_name = "bullet.png", speed = 7, scale = 4, direction=0 )
        new_bullet3 = Bullet(x = self.rect.x + self.rect.width - sprite_size//4, y = self.rect.y, image_name = "bullet.png", speed = 7, scale = 4 , direction=2)

        bullets.add(new_bullet1)
        bullets.add(new_bullet2)
        bullets.add(new_bullet3)

        #s = mixer.Sound("fire.ogg")
        #s.play()
    
player = Player(x = screen_size[0]//2-sprite_size//2,
                y = screen_size[1] - sprite_size - 5,
                image_name = 'rocket.png',
                speed = 5)
#mixer.init()
#mixer.music.load("space.ogg")
#mixer.music.play() 


class Counter:
    def __init__(self, x, y, text):
        self.text = text
        self.pos = (x,y)
        self.count = 0
        self.render()
    def render(self):
        f = font.SysFont("Verdana", 30)
        self.image = f.render(self.text + str(self.count), True, (255,255,255))
    def draw(self):
        window.blit(self.image, self.pos)

def show_text(text, x, y, text_color = (255, 255, 255), text_size = 40, font_name = 'Verdana'):
        f = font.SysFont(font_name, text_size)
        image = f.render(text, True, text_color)
        window.blit(image,(x, y))


bullets = sprite.Group()

enemies = sprite.Group()
for i in range(5):
    enemy = Enemy(randint(0, screen_size[0]- sprite_size), 0, 'ufo.png', randint(1,2))
    enemies.add(enemy)
asteroids = sprite.Group()
for i in range(2):
    asteroid = Asteroid(randint(0, screen_size[0]- sprite_size), 0, 'asteroid.png', randint(1,2))
    asteroids.add(asteroid)

missed_counter = Counter(10, 10, 'пропущенные:')
bullets_counter =  Counter(10, 70, 'кол-во пуль:')
bullets_counter.count = 100

bullets_counter.render()
killed_counter = Counter(10, 40, "уничтоженые:")

    



clock = time.Clock()
game = True
finish = False
while game:
    clock.tick(60)
    if finish != True:
        window.blit(bg, (0,0))
        player.update()
        enemies.update()
        enemies.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)

        bullets_counter.draw()
        missed_counter.draw()
        killed_counter.draw()
        display.update()
        enemies_lists = sprite.groupcollide(enemies, bullets, False, True)
        for e in enemies_lists:
            e.rect.y = 0
            e.rect.x = randint(0, screen_size[0] - sprite_size)
            killed_counter.count += 1
            killed_counter.render()
            
        if killed_counter.count >= 15:
            show_text("победа", screen_size[0]//2 - 100, screen_size[1]//2- 100)
            display.update()
            finish = True

        if sprite.spritecollide(player, enemies, False) or missed_counter.count >= 6 or  sprite.spritecollide(player, asteroids, False) :
            show_text("поражение", screen_size[0]//2 - 100, screen_size[1]//2- 100)
            display.update()
            finish = True

        # ПРОВЕРКА НА ПОРАЖЕНИЕ
        if missed_counter.count >= 3:
            player.lives -= 1
            missed_counter.count = 0
            missed_counter.render()
        

        for m in sprite.spritecollide(player, enemies, False) + sprite.spritecollide(player, asteroids, False):
            player.lives -= 1
            player.rect.x = screen_size[0] // 2
            m.rect.y = 0
            m.rect.x = randint(0, 640)

        
        if player.lives <= 0:
            show_text('Lose...', 300, 200, (255, 0, 0))
            display.update()
            finish = True
        
        

    for e in event.get():
        if e.type == QUIT:
            game = False