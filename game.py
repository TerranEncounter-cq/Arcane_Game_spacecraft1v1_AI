import pygame
import os
import sys
import neat
from enum import Enum
pygame.font.init()
pygame.mixer.init()

#Window
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spacecraft1v1")
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
BULLET_FIRE_SOUND.set_volume(0.5)
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
BULLET_FIRE_SOUND.set_volume(0.5)
ROCKET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'missile_sound.wav'))
ROCKET_FIRE_SOUND.set_volume(0.5)
ROCKET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'missile_hit.wav'))
ROCKET_HIT_SOUND.set_volume(0.5)
#Font
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
ROCKET_FONT = pygame.font.SysFont('comicsans', 20)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
#Gameplay
FPS = 144
HEALTH = 10
VEL = 5 #VELOCITY
BULLET_VEL = 20
MAX_BULLET = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
BULLET_WIDTH, BULLET_HEIGHT = 10, 5

MAX_ROCKET = 3
ROCKET_VEL = 10
ROCKET_WIDTH, ROCKET_HEIGHT = 30, 24

ACC = 1.0
WEAPON_ACC = 0.01
TYPE0 = 0
TYPE1 = 1
#Event
YELLOW_HIT = pygame.USEREVENT + 1 #Unique event id
RED_HIT = pygame.USEREVENT + 2
YELLOW_ROCKET_HIT = pygame.USEREVENT + 3
RED_ROCKET_HIT = pygame.USEREVENT + 4
#Image
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
YELLOW_SPACESHIP_LEFT = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow_left.png'))
YELLOW_SPACESHIP_LEFT = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_LEFT, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
YELLOW_SPACESHIP_RIGHT = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow_right.png'))
YELLOW_SPACESHIP_RIGHT = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_RIGHT, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
YELLOW_SPACESHIP_UP = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow_up.png'))
YELLOW_SPACESHIP_UP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_UP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
YELLOW_SPACESHIP_DOWN = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow_down.png'))
YELLOW_SPACESHIP_DOWN = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_DOWN, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
RED_SPACESHIP_LEFT = pygame.image.load(
    os.path.join('Assets', 'spaceship_red_left.png'))
RED_SPACESHIP_LEFT = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_LEFT, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
RED_SPACESHIP_RIGHT = pygame.image.load(
    os.path.join('Assets', 'spaceship_red_right.png'))
RED_SPACESHIP_RIGHT = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_RIGHT, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
RED_SPACESHIP_UP = pygame.image.load(
    os.path.join('Assets', 'spaceship_red_up.png'))
RED_SPACESHIP_UP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_UP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
RED_SPACESHIP_DOWN = pygame.image.load(
    os.path.join('Assets', 'spaceship_red_down.png'))
RED_SPACESHIP_DOWN = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_DOWN, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

YELLOW_ROCKET = pygame.image.load(
    os.path.join('Assets', 'yellow_rocket.png'))
YELLOW_ROCKET = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_ROCKET, (ROCKET_WIDTH, ROCKET_HEIGHT)), 180)
RED_ROCKET = pygame.image.load(
    os.path.join('Assets', 'red_rocket.png'))
RED_ROCKET = pygame.transform.scale(
    RED_ROCKET, (ROCKET_WIDTH, ROCKET_HEIGHT))
SPACE_BG = pygame.transform.scale(
    pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

class movement(Enum):
    STAY = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

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

class game:

    def draw_window(self, red, yellow, red_bullets, yellow_bullets, red_rockets, yellow_rockets,  
        red_health, yellow_health, red_rocket_ammo, yellow_rocket_ammo, yellow_HB, red_HB,
        red_movement_type, yellow_movement_type):

        WIN.blit(SPACE_BG, (0, 0))
        pygame.draw.rect(WIN, BlACK, BORDER)
        yellow_HB.hp = yellow_health
        yellow_HB.draw(WIN)
        red_HB.hp = red_health
        red_HB.draw(WIN)

        #Health text
        # red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
        # yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
        #WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
        #WIN.blit(yellow_health_text, (10, 10))

        red_rocket_text = ROCKET_FONT.render("Rocket: " + str(red_rocket_ammo), 1, WHITE)
        yellow_rocket_text = ROCKET_FONT.render("Rocket: " + str(yellow_rocket_ammo), 1, WHITE)
        
        WIN.blit(red_rocket_text, (WIDTH - red_rocket_text.get_width() - 10, 35))
        WIN.blit(yellow_rocket_text, (10, 35))
        
        match red_movement_type:
            case movement.STAY:
                WIN.blit(RED_SPACESHIP_IMAGE, (red.x, red.y))
            case movement.LEFT:
                WIN.blit(RED_SPACESHIP_IMAGE, (red.x, red.y))
                #WIN.blit(RED_SPACESHIP_LEFT, (red.x, red.y))
            case movement.RIGHT:
                WIN.blit(RED_SPACESHIP_IMAGE, (red.x, red.y))
                #WIN.blit(RED_SPACESHIP_RIGHT, (red.x, red.y))
            case movement.UP:
                WIN.blit(RED_SPACESHIP_UP, (red.x, red.y))
            case movement.DOWN:
                WIN.blit(RED_SPACESHIP_DOWN, (red.x, red.y))

        match yellow_movement_type:
            case movement.STAY:
                WIN.blit(YELLOW_SPACESHIP_IMAGE, (yellow.x, yellow.y))
            case movement.LEFT:
                WIN.blit(YELLOW_SPACESHIP_IMAGE, (yellow.x, yellow.y))
                #WIN.blit(YELLOW_SPACESHIP_LEFT, (yellow.x, yellow.y))
            case movement.RIGHT:
                WIN.blit(YELLOW_SPACESHIP_IMAGE, (yellow.x, yellow.y))
                #WIN.blit(YELLOW_SPACESHIP_RIGHT, (yellow.x, yellow.y))
            case movement.UP:
                WIN.blit(YELLOW_SPACESHIP_UP, (yellow.x, yellow.y))
            case movement.DOWN:
                WIN.blit(YELLOW_SPACESHIP_DOWN, (yellow.x, yellow.y))

        for bullet, _ in red_bullets:
            pygame.draw.rect(WIN, RED, bullet)

        for bullet, _ in yellow_bullets:
            pygame.draw.rect(WIN, YELLOW, bullet)

        for rocket_coor, _ in red_rockets:
            WIN.blit(RED_ROCKET, (rocket_coor.x, rocket_coor.y))
        
        for rocket_coor, _ in yellow_rockets:
            WIN.blit(YELLOW_ROCKET, (rocket_coor.x, rocket_coor.y))

        pygame.display.update() # pygame.display.update() must be placed at the end the of the function!!!

    def draw_winner(self, text):
        draw_text = WINNER_FONT.render(text, 1, WHITE)
        WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(5000)

    def move_spacecraft(self, yellow, VELOCITY, movement_type):
        match movement_type:
            case movement.STAY:
                pass
            case movement.LEFT:
                yellow.x -= VELOCITY
            case movement.RIGHT:
                yellow.x += VELOCITY
            case movement.UP:
                yellow.y -= VELOCITY
            case movement.DOWN:
                yellow.y += VELOCITY
        
    def yellow_handle_movement(self, keys_pressed, yellow, yellow_cur_vel, VELOCITY, AI_input):
        if yellow_cur_vel < VELOCITY:
            yellow_cur_vel += 3 * ACC

        movement_type = movement.STAY
        if (keys_pressed[pygame.K_a] or AI_input == "A") and yellow.x - yellow_cur_vel > 0: #LEFT
            movement_type = movement.LEFT
        if (keys_pressed[pygame.K_d] or AI_input == "D") and yellow.x + yellow_cur_vel + yellow.width < BORDER.x: #RIGHT
            movement_type = movement.RIGHT
        if (keys_pressed[pygame.K_w] or AI_input == "W") and yellow.y - yellow_cur_vel > 0: #UP
            movement_type = movement.UP
        if (keys_pressed[pygame.K_s] or AI_input == "S") and yellow.y + yellow_cur_vel + yellow.height < HEIGHT - 10: #DOWN
            movement_type = movement.DOWN
        self.move_spacecraft(yellow, VELOCITY, movement_type)
        return movement_type

    def red_handle_movement(self, keys_pressed, red, red_cur_vel, VELOCITY, AI_input):
        if red_cur_vel < VELOCITY:
            red_cur_vel += 3 * ACC 
        
        movement_type = movement.STAY
        if (keys_pressed[pygame.K_LEFT] or AI_input == "A") and red.x - red_cur_vel > BORDER.x + BORDER.width: #LEFT
            movement_type = movement.LEFT
        if (keys_pressed[pygame.K_RIGHT] or AI_input == "D") and red.x + red_cur_vel + red.width < WIDTH: #RIGHT
            movement_type = movement.RIGHT
        if (keys_pressed[pygame.K_UP] or AI_input == "W") and red.y - red_cur_vel > 0: #UP
            movement_type = movement.UP
        if (keys_pressed[pygame.K_DOWN] or AI_input == "S") and red.y + red_cur_vel + red.height < HEIGHT - 10: #DOWN
            movement_type = movement.DOWN
        self.move_spacecraft(red, VELOCITY, movement_type)
        return movement_type

    def handle_weapon(self, yellow_bullets, red_bullets, yellow, red, VELOCITY, TYPE):
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
                for _ in range(damage):
                    if (TYPE == 0):
                        pygame.event.post(pygame.event.Event(RED_HIT))
                    elif (TYPE == 1):
                        pygame.event.post(pygame.event.Event(RED_ROCKET_HIT))
                yellow_bullets.remove(each)
            if bullet.x > WIDTH:
                yellow_bullets.remove(each)
        
        for each in red_bullets:
            bullet = each[0]
            cur_vel = each[1]
            bullet.x -= cur_vel
            if yellow.colliderect(bullet):
                for _ in range(damage):
                    if (TYPE == 0):
                        pygame.event.post(pygame.event.Event(YELLOW_HIT))
                    elif (TYPE == 1):
                        pygame.event.post(pygame.event.Event(YELLOW_ROCKET_HIT))
                red_bullets.remove(each)
            if bullet.x > WIDTH:
                red_bullets.remove(each)
            
    def handle_weapon_acceleration(self, weapon, VELOCITY):
        for each in weapon:
            if each[1] < VELOCITY:
                each[1] += 0.3 * each[1] + WEAPON_ACC * VELOCITY
    
    def handle_spacecraft_acceleration(self, cur_vel, VELOCITY):
        res = cur_vel
        if cur_vel - ACC * VELOCITY > 0:
            res -= 1 * ACC 
        return res

    def loop(self, run, AI):
        yellow_HB = HealthBar(10, 15, 250, 20, HEALTH)
        red_HB = HealthBar(WIDTH - 300 + 40, 15, 250, 20, HEALTH)
        self.yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        self.red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

        red_cur_vel = 0.0
        yellow_cur_vel = 0.0

        self.yellow_bullets = []
        self.red_bullets = []
        self.yellow_rockets = []
        yellow_rocket_ammo = MAX_ROCKET
        self.red_rockets = []
        red_rocket_ammo = MAX_ROCKET
        winner_text = ""

        red_health = 10
        yellow_health = 10

        clock = pygame.time.Clock()
        while run:
            clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit(0)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL and len(self.yellow_bullets) < MAX_BULLET:
                        bullet = pygame.Rect(
                            self.yellow.x + self.yellow.width, self.yellow.y + self.yellow.height//2 - 2, BULLET_WIDTH, BULLET_HEIGHT)
                        self.yellow_bullets.append([bullet, 0])
                        BULLET_FIRE_SOUND.play()

                    if event.key == pygame.K_LSHIFT and yellow_rocket_ammo > 0:
                        rocket = pygame.Rect(
                            self.yellow.x + self.yellow.width, self.yellow.y + self.yellow.height//2 - 2, ROCKET_WIDTH, ROCKET_HEIGHT)
                        self.yellow_rockets.append([rocket, 0])
                        yellow_rocket_ammo -= 1
                        ROCKET_FIRE_SOUND.play()

                    if event.key == pygame.K_RCTRL:
                        bullet = pygame.Rect and len(self.red_bullets) < MAX_BULLET(
                            self.red.x, self.red.y + self.red.height//2 - 2, BULLET_WIDTH, BULLET_HEIGHT)
                        self.red_bullets.append([bullet, 0])
                        BULLET_FIRE_SOUND.play()

                    if event.key == pygame.K_RSHIFT and red_rocket_ammo > 0:
                        rocket = pygame.Rect(
                                self.red.x, self.red.y + self.red.height//2 - 2, ROCKET_WIDTH, ROCKET_HEIGHT)
                        self.red_rockets.append([rocket, 0])
                        red_rocket_ammo -= 1
                        ROCKET_FIRE_SOUND.play()

                if event.type == RED_HIT:
                    red_health -= 1
                    BULLET_HIT_SOUND.play()

                if event.type == YELLOW_HIT:
                    yellow_health -= 1
                    BULLET_HIT_SOUND.play()

                if event.type == RED_ROCKET_HIT:
                    red_health -= 1
                    ROCKET_HIT_SOUND.play()
                if event.type == YELLOW_ROCKET_HIT:
                    yellow_health -= 1
                    ROCKET_HIT_SOUND.play()
                    
            if red_health <= 0:
                winner_text = "Yellow Wins!"

            if yellow_health <= 0:
                winner_text = "Red Wins!"

            if winner_text != "":
                self.draw_winner(winner_text) #Someone won the game
                return [winner_text, yellow_health, red_health]

            keys_pressed = pygame.key.get_pressed()
            if (not AI):
                yellow_movement_type = self.yellow_handle_movement(keys_pressed, self.yellow, yellow_cur_vel, VEL, "")
                red_movement_type    = self.red_handle_movement(keys_pressed, self.red, red_cur_vel, VEL, "")
            else:
                yellow_movement_type = self.yellow_handle_movement(keys_pressed, self.yellow, yellow_cur_vel, VEL, "")
                red_movement_type    = self.red_handle_movement(keys_pressed, self.red, red_cur_vel, VEL, "")

            self.handle_weapon(self.yellow_bullets, self.red_bullets, self.yellow, self.red, BULLET_VEL, TYPE0)
            self.handle_weapon(self.yellow_rockets, self.red_rockets, self.yellow, self.red, ROCKET_VEL, TYPE1)

            self.handle_weapon_acceleration(self.yellow_bullets, BULLET_VEL)
            self.handle_weapon_acceleration(self.red_bullets, BULLET_VEL)
            self.handle_weapon_acceleration(self.yellow_rockets, ROCKET_VEL)
            self.handle_weapon_acceleration(self.red_rockets, ROCKET_VEL)

            self.draw_window(self.red, self.yellow, self.red_bullets, self.yellow_bullets, self.red_rockets, self.yellow_rockets, 
                red_health, yellow_health, red_rocket_ammo, yellow_rocket_ammo, yellow_HB, red_HB,
                red_movement_type, yellow_movement_type)

            self.handle_spacecraft_acceleration(yellow_cur_vel, VEL)
            self.handle_spacecraft_acceleration(red_cur_vel, VEL)

    def train_ai(self, genome1, genome2, config):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
        self.genome1 = genome1
        run_main = True
        while run_main: 
            game_info = self.loop(run_main, True)
            winner_text, yellow_health, red_health = game_info
            yellow_bonus, red_bonus = 0, 0
            if winner_text == "Yellow Wins!":
                yellow_bonus = 5
            elif winner_text == "Red Wins!":
                red_bonus = 5
            output1 = net1.activate((self.yellow.x, self.yellow.y, self.red.x, self.red.y,  yellow_bonus))
            output2 = net2.activate((self.yellow.x, self.yellow.y, self.red.x, self.red.y, red_bonus))
            # output2 = net2.activate((self.yellow.x, self.yellow.y, self.red.x, self.red.y, 
            #                 self.yellow_bullets, self.yellow_rockets,
            #                 self.red_bullets, self.red_rockets, red_bonus))
            print(output1, output2)
            
            if yellow_health == HEALTH or red_health == HEALTH:
                self.calculate_fitness(genome1, genome2, game_info)
                break
    
    def calculate_fitness(self, genome1, genome2, game_info):
        pass