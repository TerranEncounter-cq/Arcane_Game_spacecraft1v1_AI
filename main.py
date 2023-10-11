import pygame
import os
import sys

pygame.font.init()
pygame.mixer.init()

#Health bar add-on
class HealthBar():
    def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp

    def draw(self, surface):
        #calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))

#Window
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game")
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
#Color
WHITE = (255, 255, 255)
BlACK = (0, 0, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
#Sound
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND.set_volume(0.0)
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
BULLET_FIRE_SOUND.set_volume(0.7)
#Font
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
ROCKET_FONT = pygame.font.SysFont('comicsans', 20)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
#Gameplay
FPS = 60
VEL = 5 #VELOCITY
BULLET_VEL = 15
MAX_BULLET = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
BULLET_WIDTH, BULLET_HEIGHT = 10, 5

MAX_ROCKET = 10
ROCKET_VEL = 20
ROCKET_WIDTH, ROCKET_HEIGHT = 20, 8

ACC = 0.03
#Event
YELLOW_HIT = pygame.USEREVENT + 1 #Unique event id
RED_HIT = pygame.USEREVENT + 2
#Image
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE_BG = pygame.transform.scale(
    pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_rockets, yellow_rockets,  
    red_health, yellow_health, red_rocket_ammo, yellow_rocket_ammo, yellow_HB, red_HB):

    WIN.blit(SPACE_BG, (0, 0))
    pygame.draw.rect(WIN, BlACK, BORDER)
    yellow_HB.hp = yellow_health
    yellow_HB.draw(WIN)
    red_HB.hp = red_health
    red_HB.draw(WIN)

    #Health text
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    #WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    #WIN.blit(yellow_health_text, (10, 10))

    red_rocket_text = ROCKET_FONT.render("Rocket: " + str(red_rocket_ammo), 1, WHITE)
    yellow_rocket_text = ROCKET_FONT.render("Rocket: " + str(yellow_rocket_ammo), 1, WHITE)
    
    WIN.blit(red_rocket_text, (WIDTH - red_rocket_text.get_width() - 10, 35))
    WIN.blit(yellow_rocket_text, (10, 35))
    
    WIN.blit(YELLOW_SPACESHIP_IMAGE, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP_IMAGE, (red.x, red.y))


    for bullet, _ in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet, _ in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    for rocket, _ in red_rockets:
        pygame.draw.rect(WIN, CYAN, rocket)
    
    for rocket, _ in yellow_rockets:
        pygame.draw.rect(WIN, PURPLE, rocket)

    pygame.display.update() # pygame.display.update() must be placed at the end the of the function!!!

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def yellow_handle_movement(keys_pressed, yellow, yellow_cur_vel, VELOCITY):
    if yellow_cur_vel < VELOCITY:
        yellow_cur_vel += 20 * ACC * VELOCITY 

    if keys_pressed[pygame.K_a] and yellow.x - yellow_cur_vel > 0: #LEFT
        yellow.x -= yellow_cur_vel
    if keys_pressed[pygame.K_d] and yellow.x + yellow_cur_vel + yellow.width < BORDER.x: #RIGHT
        yellow.x += yellow_cur_vel
    if keys_pressed[pygame.K_w] and yellow.y - yellow_cur_vel > 0: #UP
        yellow.y -= yellow_cur_vel
    if keys_pressed[pygame.K_s] and yellow.y + yellow_cur_vel + yellow.height < HEIGHT - 10: #DOWN
        yellow.y += yellow_cur_vel

def red_handle_movement(keys_pressed, red, red_cur_vel, VELOCITY):
    if red_cur_vel < VELOCITY:
        red_cur_vel += 1.7 * ACC * VELOCITY 
        
    if keys_pressed[pygame.K_LEFT] and red.x - red_cur_vel > BORDER.x + BORDER.width: #LEFT
        red.x -= red_cur_vel
    if keys_pressed[pygame.K_RIGHT] and red.x + red_cur_vel + red.width < WIDTH: #RIGHT
        red.x += red_cur_vel
    if keys_pressed[pygame.K_UP] and red.y - red_cur_vel > 0: #UP
        red.y -= red_cur_vel
    if keys_pressed[pygame.K_DOWN] and red.y + red_cur_vel + red.height < HEIGHT - 10: #DOWN
        red.y += red_cur_vel

def handle_weapon(yellow_bullets, red_bullets, yellow, red, VELOCITY):
    damage = 1
    if VELOCITY == BULLET_VEL:
        damage *= 1
    elif VELOCITY == ROCKET_VEL:
        damage *= 3

    for each in yellow_bullets:
        bullet = each[0]
        cur_vel = each[1]
        bullet.x += cur_vel
        if red.colliderect(bullet):
            for i in range(damage):
                pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(each)
        if bullet.x > WIDTH:
            yellow_bullets.remove(each)
    
    for bullet, cur_vel in red_bullets:
        bullet = each[0]
        cur_vel = each[1]
        bullet.x -= cur_vel
        if yellow.colliderect(bullet):
            for i in range(damage):
                pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(each)
        if bullet.x > WIDTH:
            red_bullets.remove(each)
        
def handle_weapon_acceleration(weapon, VELOCITY):
    for each in weapon:
        if each[1] < VELOCITY:
            each[1] += ACC * VELOCITY

def handle_spacecraft_acceleration(spacecraft, cur_vel, VELOCITY):
    if cur_vel - ACC * VELOCITY > 0:
        cur_vel -= 0 * ACC * VELOCITY

def main():
    pygame.init()

    yellow_HB = HealthBar(10, 15, 250, 20, 10)
    red_HB = HealthBar(WIDTH - 300 + 40, 15, 250, 20, 10)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_cur_vel = 0
    yellow_cur_vel = 0

    yellow_bullets = []
    red_bullets = []
    yellow_rockets = []
    yellow_rocket_ammo = MAX_ROCKET
    red_rockets = []
    red_rocket_ammo = MAX_ROCKET
    winner_text = ""

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLET:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, BULLET_WIDTH, BULLET_HEIGHT)
                    yellow_bullets.append([bullet, 0])
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_LSHIFT and yellow_rocket_ammo > 0:
                    rocket = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, ROCKET_WIDTH, ROCKET_HEIGHT)
                    yellow_rockets.append([rocket, 0])
                    yellow_rocket_ammo -= 1
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL:
                    bullet = pygame.Rect and len(red_bullets) < MAX_BULLET(
                        red.x, red.y + red.height//2 - 2, BULLET_WIDTH, BULLET_HEIGHT)
                    red_bullets.append([bullet, 0])
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RSHIFT and yellow_rocket_ammo >= 0:
                    rocket = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, ROCKET_WIDTH, ROCKET_HEIGHT)
                    red_rockets.append([rocket, 0])
                    red_rocket_ammo -= 1
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text) #Someone won the game
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow, yellow_cur_vel, VEL)
        red_handle_movement(keys_pressed, red, red_cur_vel, VEL)
        handle_spacecraft_acceleration(yellow, yellow_cur_vel, VEL)
        handle_spacecraft_acceleration(red, red_cur_vel, VEL)

        handle_weapon(yellow_bullets, red_bullets, yellow, red, BULLET_VEL)
        handle_weapon(yellow_rockets, red_rockets, yellow, red, ROCKET_VEL)

        handle_weapon_acceleration(yellow_bullets, BULLET_VEL)
        handle_weapon_acceleration(red_bullets, BULLET_VEL)
        handle_weapon_acceleration(yellow_rockets, ROCKET_VEL)
        handle_weapon_acceleration(red_rockets, ROCKET_VEL)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_rockets, yellow_rockets, 
            red_health, yellow_health, red_rocket_ammo, yellow_rocket_ammo, yellow_HB, red_HB)

    main()

if __name__ == "__main__":
    main()