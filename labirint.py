from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (55, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def hide(self):
        self.rect.x = -100
        self.rect.y = -100

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

class Enemy(GameSprite):
    direction = 'left'
    def update(self):
        if self.rect.x <= 600:
            self.direction = 'right'
        if self.rect.x >= win_width - 85:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color1, color2, color3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color1, color2, color3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

def reset_game():
    global player, monster, finish
    player.rect.x = 5
    player.rect.y = win_height - 80
    monster.rect.x = win_width - 80
    monster.rect.y = 350
    finish = False
    mixer.music.play(-1)

win_width = 800
win_height = 600
window = display.set_mode((win_width, win_height))
display.set_caption('Лабиринт')
image_background = image.load('star.webp')
background = transform.scale(image_background, (win_width, win_height))

player = Player('heros.png', 5, win_height - 80, 4)
monster = Enemy('enemy.png', win_width - 80, 350, 2)
final = GameSprite('portal.png', win_width - 120, win_height - 80, 0)

w1 = Wall(150, 70, 150, 100, 10, 500, 10)
w2 = Wall(150, 70, 150, 100, 550, 500, 10)
w3 = Wall(150, 70, 150, 100, 10, 10, 460)
w4 = Wall(150, 70, 150, 200, 100, 10, 460)
w5 = Wall(150, 70, 150, 300, 10, 10, 460)
w6 = Wall(150, 70, 150, 400, 100, 10, 460)
w7 = Wall(150, 70, 150, 500, 10, 10, 460)
w8 = Wall(150, 70, 150, 600, 100, 10, 460)

game = True
finish = False
clock = time.Clock()
fps = 60
font.init()
font = font.SysFont('Arial', 70)
win_text = font.render('YOU WIN!', True, (0, 255, 0))
lose_text = font.render('YOU LOSE!', True, (255, 0, 0))

mixer.init()
mixer.music.load('space.mp3')
mixer.music.play(-1)

winer = mixer.Sound('winer.mp3')
loser = mixer.Sound('lose.mp3')

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_r and finish:
                reset_game()

    if not finish:
        player.update()
        monster.update()

        window.blit(background, (0, 0))
        player.reset()
        monster.reset()
        final.reset()
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()
        w6.draw_wall()
        w7.draw_wall()
        w8.draw_wall()

        if sprite.collide_rect(player, monster) or sprite.collide_rect(player, w1) or sprite.collide_rect(player, w2) or sprite.collide_rect(player, w3) or sprite.collide_rect(player, w4) or sprite.collide_rect(player, w5) or sprite.collide_rect(player, w6) or sprite.collide_rect(player, w7) or sprite.collide_rect(player, w8):
            finish = True
            mixer.music.stop()
            loser.play()
            window.blit(lose_text, (280, 300))
        
        if sprite.collide_rect(player, final):
            finish = True
            mixer.music.stop()
            winer.play()
            player.hide()
            window.blit(win_text, (280, 300))
    else:
        if not mixer.get_busy():
            pass

    display.update()
    clock.tick(fps)
