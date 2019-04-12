# Imports
import pygame
import random

# Initialize game engine
pygame.init()
pygame.mixer.init()

# Window
WIDTH = 1600
HEIGHT = 900
SIZE = (WIDTH, HEIGHT)
TITLE = "Galaxy Runner"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)

# Timer
clock = pygame.time.Clock()
refresh_rate = 60

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)
GREY = (128, 128, 128)
DARKGREY = (169, 169, 169)

# Fonts
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font(None, 32)
FONT_LG = pygame.font.Font(None, 64)
FONT_XL = pygame.font.Font("assets/fonts/spacerangerboldital.ttf", 96)
FONT_XL2 = pygame.font.Font("assets/fonts/spacerangerboldital.ttf", 90)

# Images
player_img = pygame.image.load('assets/images/player.png').convert_alpha()
laser_img = pygame.image.load('assets/images/Lasers/laserBlue16.png').convert_alpha()
enemy_img = pygame.image.load('assets/images/Enemies/enemyRed5.png').convert_alpha()
bomb_img = pygame.image.load('assets/images/Meteors/meteorGrey_med2.png').convert_alpha()
shield_img = pygame.image.load('assets/images/Effects/shield3.png').convert_alpha()
button_img = pygame.image.load('assets/images/UI/buttonBlue.png').convert_alpha()
star_img = pygame.image.load('assets/images/Effects/star2.png').convert_alpha()
genemy_img = pygame.image.load('assets/images/Enemies/enemyGreen1.png').convert_alpha()
benemy_img = pygame.image.load('assets/images/Enemies/enemyBlack4.png').convert_alpha()
damage1_img = pygame.image.load('assets/images/Damage/playerShip2_damage3.png').convert_alpha()
powerup1_img = pygame.image.load('assets/images/Power-ups/shield_gold.png').convert_alpha()
powerup2_img = pygame.image.load('assets/images/Power-ups/bolt_gold.png').convert_alpha()
powerup3_img = pygame.image.load('assets/images/Power-ups/star_gold.png').convert_alpha()
ufo_img = pygame.image.load('assets/images/enemyUFO.png').convert_alpha()
ship_damaged_img = pygame.image.load('assets/images/playerDamaged.png').convert_alpha()
ship_left_img = pygame.image.load('assets/images/playerLeft.png').convert_alpha()
ship_right_img = pygame.image.load('assets/images/playerRight.png').convert_alpha()

# Sounds
EXPLOSION = pygame.mixer.Sound('assets/sounds/explosion.ogg')
SHOOT = pygame.mixer.Sound('assets/sounds/shoot.wav')
HIT = pygame.mixer.Sound('assets/sounds/hit.wav')
pygame.mixer.music.load('assets/sounds/start_background.ogg')
    
# Stages
START = 0
PLAYING = 1
END = 2
PAUSE = 3

bullets_shot = 0
bullets_hit = 0

# make objects
''' stars '''
num_stars = 325
stars = []
for i in range(num_stars):
    x = random.randrange(0, 1599)
    y = random.randrange(0, 899)
    r = random.randrange(1, 6)
    s = [x, y, r, r]
    stars.append(s)

# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, normal, left, right):
        super().__init__()

        self.normal = normal
        self.left = left
        self.right = right
        self.image = normal
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image) 
        self.rect.x = x
        self.rect.y = y
        self.shield = 3
        self.speed = 5

    def move_normal(self):
        self.image = self.normal

    def move_left(self):
        self.rect.x -= self.speed
        self.image = self.left
    
    def move_right(self):
        self.rect.x += self.speed
        self.image = self.right

    def move_up(self):
        self.rect.y -= self.speed
        self.image = self.normal

    def move_down(self):
        self.rect.y += self.speed
        self.image = self.normal

    def diagonal_up_right(self):
        self.rect.x += self.speed
        self.rect.y -= self.speed

    def shoot(self):
        pygame.mixer.Sound.play(SHOOT)
        laser = Laser(laser_img)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        lasers.add(laser)

    def update(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.top < 700:
            self.rect.top = 700
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


        power_list = pygame.sprite.spritecollide(self, powerups, True,
                                               pygame.sprite.collide_mask)

        hit_list = pygame.sprite.spritecollide(self, bombs, True,
                                               pygame.sprite.collide_mask)

        mob_list = pygame.sprite.spritecollide(self, mobs, True,
                                               pygame.sprite.collide_mask)


        if len(power_list) > 0:
            self.shield += 1

        if len(mob_list) > 0:
            self.shield -= 1

        if len(hit_list) > 0:
            self.shield -= 1

        if self.shield == 0:
            self.kill()
            
class Laser(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < -5:
            self.kill()

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image) 
        self.rect.x = x
        self.rect.y = y

    def drop_bomb(self):
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)

    def update(self):
        hit_list = pygame.sprite.spritecollide(self, lasers, True,
                                               pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            self.kill()
            player.score += 1
            player.shots_hit += 1
            fleet.speed += 1
            pygame.mixer.Sound.play(EXPLOSION)

        if self.rect.y > HEIGHT:
            self.kill()

class Gmob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image) 
        self.rect.x = x
        self.rect.y = y
        self.shield = 3

    def drop_bomb(self):
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)

    def update(self):
        hit_list = pygame.sprite.spritecollide(self, lasers, True,
                                               pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            self.shield -= 1
            player.shots_hit += 1
            pygame.mixer.Sound.play(HIT)

        if self.shield == 0:
            self.kill()
            player.score += 2
            fleet.speed += 1
            pygame.mixer.Sound.play(EXPLOSION)
        
        if self.rect.y > HEIGHT:
            self.kill()

class Bmob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image) 
        self.rect.x = x
        self.rect.y = y
        self.shield = 5

    def drop_bomb(self):
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)

    def update(self):
        hit_list = pygame.sprite.spritecollide(self, lasers, True,
                                               pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            self.shield -= 1
            player.shots_hit += 1
            pygame.mixer.Sound.play(HIT)


        if self.shield == 0:
            self.kill()
            player.score += 3
            fleet.speed += 1
            pygame.mixer.Sound.play(EXPLOSION)
        
        if self.rect.y > HEIGHT:
            self.kill()

class Bomb(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speed = 5

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()

class Fleet():
    def __init__(self, mobs):
        self.mobs = mobs
        self.speed = 1
        self.moving_right = True
        self.drop_speed = 30
        self.bomb_rate = 60

    def move(self):
        hits_edge = False
        
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed

                if m.rect.right >= WIDTH:
                    hits_edge = True
            else:
                m.rect.x -= self.speed

                if m.rect.left <= 0:
                    hits_edge = True

        if hits_edge:
            self.reverse()
            self.move_down()

    def reverse(self):
        self.moving_right = not self.moving_right

    def move_down(self):
        for m in mobs:
            m.rect.y += self.drop_speed

    def choose_bomber(self):
        rand = random.randrange(self.bomb_rate)
        mob_list = mobs.sprites()

        if len(mob_list) > 0 and rand == 0:
            bomber = random.choice(mob_list)
            bomber.drop_bomb()

    def update(self):
        self.move()
        self.choose_bomber()

class ShieldPowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speed = 6
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()

class Shield(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Ufo(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image) 
        self.rect.x = x
        self.rect.y = y
        self.speed = 7

    def update(self):
        if stage == START:
            self.rect.x += self.speed
            
            if self.rect.right > 1600 or self.rect.left < 0:
                self.speed *= -1

# Game helper functions
def show_title_screen():
    title_txt = FONT_XL.render("Galaxy Runner", 1, WHITE)
    screen.blit(title_txt, [WIDTH/4, 50])

def show_title_screen2():
    title2_txt = FONT_XL.render("Press (SPACE) to begin", 1, WHITE)
    screen.blit(title2_txt, [WIDTH/7, 150])

def show_end_screen():
    end_txt = FONT_XL.render("Game Over!", 1, WHITE)
    w = end_txt.get_width()
    screen.blit(end_txt, (WIDTH/2 - w/2, 100))

def show_end_screen2():
    end2_txt = FONT_XL.render("Press (R) to restart", 1, WHITE)
    w = end2_txt.get_width()
    screen.blit(end2_txt, (WIDTH/2 - w/2, 200))

def accuracy_screen():
    accuracy_formula = "Accuracy: " + str(player.shots_hit) + "/" + str(player.shots_fired)
    bullets_txt = FONT_XL.render(accuracy_formula, 1, WHITE)
    screen.blit(bullets_txt, [50, 400])
    
def show_stats(player):
    score_txt = FONT_XL.render(str(player.score), 1, WHITE)
    screen.blit(score_txt, [1400, 50])

def check_end():
    global stage
    
    if len(mobs) == 0:
        stage = END
    elif len(player) == 0:
        stage = END

def draw_stars():
    for s in stars:
        pygame.draw.ellipse(screen, WHITE, s)

def mobs_killed():
    mobs_txt = FONT_XL.render("Mobs Killed: " + str(fleet.speed), 1, WHITE)
    screen.blit(mobs_txt, [50, 500])

def show_score():
    stats_txt = FONT_XL.render("Final Score: " + str(player.score), 1, WHITE)
    screen.blit(stats_txt, [50, 600])

def show_end():
    show_end_screen()
    show_end_screen2()
    accuracy_screen()
    mobs_killed()
    show_score()

def show_start():
    show_title_screen()
    show_title_screen2()
    ufos.draw(screen)

def setup():
    global stage, done
    global player, ship, mobs, fleet, ufos
    global bombs, lasers, powerups, shield, shield2, shield3, shield4, shield5

    'make game objects'
    ship = Ship(750, 800, player_img, ship_left_img, ship_right_img)

    'level'
    level = 1

    ''' Make sprite groups '''
    player = pygame.sprite.GroupSingle()
    player.score = 0
    player.shots_fired = 0
    player.shots_hit = 0
    player.add(ship)

    lasers = pygame.sprite.Group()
    bombs = pygame.sprite.Group()

    bmob2 = Bmob(300, 100, benemy_img)
    bmob3 = Bmob(500, 100, benemy_img)
    bmob4 = Bmob(700, 100, benemy_img)
    bmob5 = Bmob(900, 100, benemy_img)
    bmob6 = Bmob(1100, 100, benemy_img)
    gmob7 = Gmob(400, 200, genemy_img)
    gmob8 = Gmob(600, 200, genemy_img)
    gmob9 = Gmob(800, 200, genemy_img)
    gmob10 = Gmob(1000, 200, genemy_img)
    mob11 = Mob(500, 300, enemy_img)
    mob12 = Mob(700, 300, enemy_img)
    mob13 = Mob(900, 300, enemy_img)

    mobs = pygame.sprite.Group()
    
    fleet = Fleet(mobs)

    fleet1 = (bmob2, bmob3, bmob4, bmob5, bmob6, gmob7, gmob8, gmob9, gmob10, mob11,
              mob12, mob13)
    
    if level == 1:
        mobs.add(fleet1)

    powerup1 = ShieldPowerUp(386, -5798, powerup1_img)
    powerup2 = ShieldPowerUp(600, -9342, powerup1_img)
    powerups = pygame.sprite.Group()
    powerups.add(powerup1, powerup2)

    ufo1 = Ufo(10, 500, ufo_img)
    ufo2 = Ufo(1490, 300, ufo_img)
    ufo3 = Ufo(1490, 700, ufo_img)
    ufos = pygame.sprite.Group()
    ufos.add(ufo1, ufo2, ufo3)

    shield_1 = Shield(50, 50, powerup1_img)
    shield_2 = Shield(100, 50, powerup1_img)
    shield_3 = Shield(150, 50, powerup1_img)
    shield_4 = Shield(200, 50, powerup1_img)
    shield_5 = Shield(250, 50, powerup1_img)

    shield = pygame.sprite.GroupSingle()
    shield.add(shield_1)
    shield2 = pygame.sprite.GroupSingle()
    shield2.add(shield_2)
    shield3 = pygame.sprite.GroupSingle()
    shield3.add(shield_3)
    shield4 = pygame.sprite.GroupSingle()
    shield4.add(shield_4)
    shield5 = pygame.sprite.GroupSingle()
    shield5.add(shield_5)

    ''' set stage '''
    stage = START
    done = False
    
# Game loop
setup()
pygame.mixer.music.play(-1)

while not done:
    # Input handling (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True

            if event.key == pygame.K_SPACE:
                if stage == START:
                    stage = PLAYING
            elif event.key == pygame.K_r:
                if stage == END:
                    setup()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if stage == PLAYING:
                if event.button == 1:
                    ship.shoot()
                    player.shots_fired += 1

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_a]:
        ship.move_left()
    elif pressed[pygame.K_d]:
        ship.move_right()
    elif pressed[pygame.K_w]:
        ship.move_up()
    elif pressed[pygame.K_s]:
        ship.move_down()
    else:
        ship.move_normal()
        
    # Game logic (Check for collisions, update points, etc.)
    if stage == START:
        ufos.update()
    elif stage == PLAYING:
        player.update()
        lasers.update()
        bombs.update()
        fleet.update()
        mobs.update()
        powerups.update()
        shield.update()
        shield2.update()
        shield3.update()
        shield4.update()
        shield5.update()
        
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.fill(BLACK)
    draw_stars()
    check_end()
    if stage == START:
        show_start()
    elif stage == PLAYING:
        lasers.draw(screen)
        bombs.draw(screen)
        player.draw(screen)
        mobs.draw(screen)
        show_stats(player)
        powerups.draw(screen)
        if ship.shield == 6:
            shield.draw(screen)
            shield2.draw(screen)
            shield3.draw(screen)
            shield4.draw(screen)
            shield5.draw(screen)
        elif ship.shield == 5:
            shield.draw(screen)
            shield2.draw(screen)
            shield3.draw(screen)
            shield4.draw(screen)
        elif ship.shield == 4:
            shield.draw(screen)
            shield2.draw(screen)
            shield3.draw(screen)
        elif ship.shield == 3:
            shield.draw(screen)
            shield2.draw(screen)
        elif ship.shield == 2:
            shield.draw(screen)
    elif stage == END:
        show_end()
        
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
