import pygame
import os
import sys
import neat
import random
import math
import numpy as np
import time
from enum import Enum
pygame.font.init()
pygame.mixer.init()

# ni ji zi wan ma?
DIANNAO = True
#Window
WIDTH, HEIGHT = 900, 500
BORDER_X = WIDTH//2 - 5
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spacecraft1v1")
BORDER = pygame.Rect(BORDER_X, 0, 10, HEIGHT)
#Color
WHITE = (255, 255, 255)
BlACK = (0, 0, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
#Sound
MUTE = True
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
FPS = 60
HEALTH = 5
VEL = 5 #VELOCITY
BULLET_VEL = 20
MAX_BULLET = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
BULLET_WIDTH, BULLET_HEIGHT = 10, 5

MAX_ROCKET = 3
ROCKET_VEL = 10
ROCKET_WIDTH, ROCKET_HEIGHT = 30, 24

ACC = 0.1
WEAPON_ACC = 0.1
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

movement_d = {0: movement.STAY, 1: movement.LEFT, 2: movement.RIGHT, 3: movement.UP, 4: movement.DOWN}

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

class RandomActionExplorer:
    def __init__(self, initial_epsilon=0.2, decay_factor=0.995, min_epsilon=0.01):
        self.epsilon = initial_epsilon
        self.decay_factor = decay_factor
        self.min_epsilon = min_epsilon

    def should_explore(self):
        return random.random() < self.epsilon

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon * self.decay_factor, self.min_epsilon)

class game:
    def __init__(self):
        self.yellow_HB = HealthBar(10, 15, 250, 20, HEALTH)
        self.red_HB = HealthBar(WIDTH - 300 + 40, 15, 250, 20, HEALTH)
        self.yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        self.red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        self.mute = MUTE

        self.red_cur_vel = 0.0
        self.yellow_cur_vel = 0.0

        self.yellow_bullets = []
        self.red_bullets = []
        self.yellow_rockets = []
        self.yellow_rocket_ammo = MAX_ROCKET
        self.red_rockets = []
        self.red_rocket_ammo = MAX_ROCKET
        self.winner_text = ""

        self.red_health = 10
        self.yellow_health = 10

        self.system_bullet_timer = FPS
        self.draw = 0
        #self.sys_red_bullets = []
        #self.sys_yellow_bullets = []

    def reset(self, DEFAULT=True):
        if DEFAULT:
            yellow_x = 100
            yellow_y = 300
            red_x = 700
            red_y = 300
        else:
            yellow_x = random.randint(0, BORDER.x - SPACESHIP_WIDTH)
            yellow_y = random.randint(0, HEIGHT - 10 - SPACESHIP_HEIGHT)
            red_x = random.randint(BORDER.x + BORDER.width, WIDTH - SPACESHIP_WIDTH)
            red_y = random.randint(0, HEIGHT - 10- SPACESHIP_HEIGHT)

        self.yellow = pygame.Rect(yellow_x, yellow_y, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        self.red = pygame.Rect(red_x, red_y, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        self.red_cur_vel = 0.0
        self.yellow_cur_vel = 0.0

        self.yellow_bullets = []
        self.red_bullets = []
        self.yellow_rockets = []
        self.yellow_rocket_ammo = MAX_ROCKET
        self.red_rockets = []
        self.red_rocket_ammo = MAX_ROCKET
        self.winner_text = ""

        self.red_health = HEALTH
        self.yellow_health = HEALTH

        self.system_bullet_timer = FPS
        self.sys_red_bullets = []
        self.sys_yellow_bullets = []
        self.draw = 0
        
    def draw_window(self, red, yellow, red_bullets, yellow_bullets, red_rockets, yellow_rockets,  
        red_health, yellow_health, red_rocket_ammo, yellow_rocket_ammo, yellow_HB, red_HB,
        red_movement_type, yellow_movement_type, sys_red_bullets, sys_yellow_bullets):

        WIN.blit(SPACE_BG, (0, 0))
        pygame.draw.rect(WIN, BlACK, BORDER)
        yellow_HB.hp = yellow_health
        yellow_HB.draw(WIN)
        red_HB.hp = red_health
        red_HB.draw(WIN)

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
        
        for bullet in sys_red_bullets:
            pygame.draw.rect(WIN, YELLOW, bullet)

        for bullet in sys_yellow_bullets:
            pygame.draw.rect(WIN, YELLOW, bullet)

        pygame.display.update() # pygame.display.update() must be placed at the end the of the function!!!

    def draw_winner(self, text):
        draw_text = WINNER_FONT.render(text, 1, WHITE)
        WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(100)

    def move_spacecraft(self, yellow_or_red, movement_type):
        if yellow_or_red:
            match movement_type:
                case movement.STAY:
                    pass
                case movement.LEFT:
                    self.yellow.x -= VEL
                case movement.RIGHT:
                    self.yellow.x += VEL
                case movement.UP:
                    self.yellow.y -= VEL
                case movement.DOWN:
                    self.yellow.y += VEL
        else:
             match movement_type:
                case movement.STAY:
                    pass
                case movement.LEFT:
                    self.red.x -= VEL
                case movement.RIGHT:
                    self.red.x += VEL
                case movement.UP:
                    self.red.y -= VEL
                case movement.DOWN:
                    self.red.y += VEL
        
    def yellow_handle_movement(self, keys_pressed, yellow, yellow_cur_vel, VELOCITY, AI_input=None):
        if yellow_cur_vel < VELOCITY:
            yellow_cur_vel += 3 * ACC

        movement_type = movement.STAY
        if keys_pressed:
            if keys_pressed[pygame.K_a] and yellow.x - yellow_cur_vel > 0:  # LEFT
                movement_type = movement.LEFT
            if keys_pressed[pygame.K_d] and yellow.x + yellow_cur_vel + yellow.width < BORDER.x:  # RIGHT
                movement_type = movement.RIGHT
            if keys_pressed[pygame.K_w] and yellow.y - yellow_cur_vel > 0:  # UP
                movement_type = movement.UP
            if keys_pressed[pygame.K_s] and yellow.y + yellow_cur_vel + yellow.height < HEIGHT - 10:  # DOWN
                movement_type = movement.DOWN
        else:  # AI control
            if AI_input == movement.LEFT and yellow.x - yellow_cur_vel > 0:  # LEFT
                movement_type = movement.LEFT
            if AI_input == movement.RIGHT and yellow.x + yellow_cur_vel + yellow.width < BORDER.x:  # RIGHT
                movement_type = movement.RIGHT
            if AI_input == movement.UP and yellow.y - yellow_cur_vel > 0:  # UP
                movement_type = movement.UP
            if AI_input == movement.DOWN and yellow.y + yellow_cur_vel + yellow.height < HEIGHT - 10:  # DOWN
                movement_type = movement.DOWN
        
        self.move_spacecraft(True, movement_type)
        return movement_type


    def red_handle_movement(self, keys_pressed, red, red_cur_vel, VELOCITY, AI_input=None):
        if red_cur_vel < VELOCITY:
            red_cur_vel += 3 * ACC 

        movement_type = movement.STAY
        if keys_pressed:
            if keys_pressed[pygame.K_LEFT] and red.x - red_cur_vel > BORDER.x + BORDER.width:  # LEFT
                movement_type = movement.LEFT
            if keys_pressed[pygame.K_RIGHT] and red.x + red_cur_vel + red.width < WIDTH:  # RIGHT
                movement_type = movement.RIGHT
            if keys_pressed[pygame.K_UP] and red.y - red_cur_vel > 0:  # UP
                movement_type = movement.UP
            if keys_pressed[pygame.K_DOWN] and red.y + red_cur_vel + red.height < HEIGHT - 10:  # DOWN
                movement_type = movement.DOWN
        else:  # AI control
            if AI_input == movement.LEFT and red.x - red_cur_vel > BORDER.x + BORDER.width:  # LEFT
                movement_type = movement.LEFT
            if AI_input == movement.RIGHT and red.x + red_cur_vel + red.width < WIDTH:  # RIGHT
                movement_type = movement.RIGHT
            if AI_input == movement.UP and red.y - red_cur_vel > 0:  # UP
                movement_type = movement.UP
            if AI_input == movement.DOWN and red.y + red_cur_vel + red.height < HEIGHT - 10:  # DOWN
                movement_type = movement.DOWN
        
        self.move_spacecraft(False, movement_type)
        return movement_type


    def handle_weapon(self, yellow_bullets, red_bullets, VELOCITY, TYPE, from_system):
        damage = 1
        if VELOCITY == BULLET_VEL:
            damage *= 1
        elif VELOCITY == ROCKET_VEL:
            damage *= 3

        yellow_bullets_to_remove = []
        for each in yellow_bullets:
            if not from_system:
                bullet = each[0]
                cur_vel = each[1]
            else:
                bullet = each
                cur_vel = VELOCITY

            bullet.x += cur_vel
            if self.red.colliderect(bullet):
                for _ in range(damage):
                    if (TYPE == 0):
                        pygame.event.post(pygame.event.Event(RED_HIT))
                    elif (TYPE == 1):
                        pygame.event.post(pygame.event.Event(RED_ROCKET_HIT))
                yellow_bullets_to_remove.append(each)
            elif bullet.x > WIDTH:
                yellow_bullets_to_remove.append(each)

        for bullet in yellow_bullets_to_remove:
            yellow_bullets.remove(bullet)

        red_bullets_to_remove = []
        for each in red_bullets:
            if not from_system:
                bullet = each[0]
                cur_vel = each[1]
            else:
                bullet = each
                cur_vel = VELOCITY

            bullet.x -= cur_vel
            if self.yellow.colliderect(bullet):
                for _ in range(damage):
                    if (TYPE == 0):
                        pygame.event.post(pygame.event.Event(YELLOW_HIT))
                    elif (TYPE == 1):
                        pygame.event.post(pygame.event.Event(YELLOW_ROCKET_HIT))
                red_bullets_to_remove.append(each)
            elif bullet.x < 0:
                red_bullets_to_remove.append(each)

        for bullet in red_bullets_to_remove:
            red_bullets.remove(bullet)


    def handle_weapon_acceleration(self, weapon, VELOCITY):
        for each in weapon:
            if each[1] < VELOCITY:
                each[1] += 0.3 * each[1] + WEAPON_ACC * VELOCITY
            #each[1] = VELOCITY

    def handle_spacecraft_acceleration(self, cur_vel, VELOCITY):
        res = cur_vel
        if cur_vel - ACC * VELOCITY > 0:
            res -= 1 * ACC 
        return res

    def loop(self, run, net1, net2, explorer1, explorer2, AI=False):
        clock = pygame.time.Clock()
        early_ender = 0
        AI_timer = 0
        ai_decisions = self.get_decision(net1, net2, explorer1, explorer2)
        behavior_metrics = {
            'yellow': {'idle_count': 0, 'bullet_used': 0, 'danger_count': 0, 'out_of_bounds_count': 0},
            'red': {'idle_count': 0, 'bullet_used': 0, 'danger_count': 0, 'out_of_bounds_count': 0}
        }

        while run:
            #self.system_bullet_timer += 1
            # if self.system_bullet_timer >= FPS:
            #     self.system_bullet_timer = 0
            #     self.random_bullet(0)
            clock.tick(FPS)
            AI_timer += 1
            if AI_timer >= FPS / 10:
                ai_decisions = self.get_decision(net1, net2, explorer1, explorer2)
                AI_timer = 0
            else:
                self.get_decision(net1, net2, explorer1, explorer2)
            #print(ai_decisions)
            early_ender += 1
            if early_ender >= 5*FPS:
                self.draw = 1
                run = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit(0)
                if not AI:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LCTRL and len(self.yellow_bullets) < MAX_BULLET:
                            bullet = pygame.Rect(
                                self.yellow.x + self.yellow.width, self.yellow.y + self.yellow.height//2 - 2, BULLET_WIDTH, BULLET_HEIGHT)
                            self.yellow_bullets.append([bullet, BULLET_VEL])
                            if not MUTE: BULLET_FIRE_SOUND.play()

                        if event.key == pygame.K_LSHIFT and self.yellow_rocket_ammo > 0:
                            rocket = pygame.Rect(
                                self.yellow.x + self.yellow.width, self.yellow.y + self.yellow.height//2 - 2, ROCKET_WIDTH, ROCKET_HEIGHT)
                            self.yellow_rockets.append([rocket, ROCKET_VEL])
                            self.yellow_rocket_ammo -= 1
                            if not MUTE: ROCKET_FIRE_SOUND.play()

                        if event.key == pygame.K_RCTRL and len(self.red_bullets) < MAX_BULLET:
                            bullet = pygame.Rect (
                                self.red.x, self.red.y + self.red.height//2 - 2, BULLET_WIDTH, BULLET_HEIGHT)
                            self.red_bullets.append([bullet, BULLET_VEL])
                            if not MUTE: BULLET_FIRE_SOUND.play()

                        if event.key == pygame.K_RSHIFT and self.red_rocket_ammo > 0:
                            rocket = pygame.Rect(
                                    self.red.x, self.red.y + self.red.height//2 - 2, ROCKET_WIDTH, ROCKET_HEIGHT)
                            self.red_rockets.append([rocket, ROCKET_VEL])
                            self.red_rocket_ammo -= 1
                            if not MUTE: ROCKET_FIRE_SOUND.play()

                if event.type == RED_HIT:
                    self.red_health -= 1
                    if not MUTE: BULLET_HIT_SOUND.play()

                if event.type == YELLOW_HIT:
                    self.yellow_health -= 1
                    if not MUTE: BULLET_HIT_SOUND.play()

                if event.type == RED_ROCKET_HIT:
                    self.red_health -= 1
                    if not MUTE: ROCKET_HIT_SOUND.play()
                if event.type == YELLOW_ROCKET_HIT:
                    self.yellow_health -= 1
                    if not MUTE: ROCKET_HIT_SOUND.play()
                    
            if self.red_health <= 0:
                self.winner_text = "Yellow Wins!"

            if self.yellow_health <= 0:
                self.winner_text = "Red Wins!"

            if self.winner_text != "":
                self.draw_winner(self.winner_text) #Someone won the game
                return behavior_metrics
            
            if not AI:
                keys_pressed = pygame.key.get_pressed()
                yellow_movement_type = self.yellow_handle_movement(keys_pressed, self.yellow, self.yellow_cur_vel, VEL, "")
                red_movement_type    = self.red_handle_movement(keys_pressed, self.red, self.red_cur_vel, VEL, "")
            else:
                yellow_movement_type = self.yellow_handle_movement(None, self.yellow, self.yellow_cur_vel, VEL, ai_decisions['decision1_movement'])
                red_movement_type = self.red_handle_movement(None, self.red, self.red_cur_vel, VEL, ai_decisions['decision2_movement'])

                if ai_decisions['decision1_movement'] == "STAY" and not ai_decisions['decision1_fire_bullet'] and not ai_decisions['decision1_fire_rocket']:
                    behavior_metrics['yellow']['idle_count'] += 1
                if ai_decisions['decision2_movement'] == "STAY" and not ai_decisions['decision2_fire_bullet'] and not ai_decisions['decision2_fire_rocket']:
                    behavior_metrics['red']['idle_count'] += 1

                # Handle bullets and rockets based on AI decisions
                if ai_decisions['decision1_fire_bullet'] and len(self.yellow_bullets) < MAX_BULLET:
                    bullet = pygame.Rect(self.yellow.x + self.yellow.width, self.yellow.y + self.yellow.height//2 - 2, BULLET_WIDTH, BULLET_HEIGHT)
                    self.yellow_bullets.append([bullet, BULLET_VEL])
                    behavior_metrics['yellow']['bullet_used'] += 1
                    if not MUTE: BULLET_FIRE_SOUND.play()
                if ai_decisions['decision1_fire_rocket'] and self.yellow_rocket_ammo > 0:
                    rocket = pygame.Rect(
                    self.yellow.x + self.yellow.width, self.yellow.y + self.yellow.height//2 - 2, ROCKET_WIDTH, ROCKET_HEIGHT)
                    self.yellow_rockets.append([rocket, ROCKET_VEL])
                    self.yellow_rocket_ammo -= 1
                    if not MUTE: ROCKET_FIRE_SOUND.play()
                if ai_decisions['decision2_fire_bullet'] and len(self.red_bullets) < MAX_BULLET:
                    bullet = pygame.Rect(
                    self.red.x, self.red.y + self.red.height//2 - 2, BULLET_WIDTH, BULLET_HEIGHT)
                    self.red_bullets.append([bullet, BULLET_VEL])
                    behavior_metrics['red']['bullet_used'] += 1
                    if not MUTE: BULLET_FIRE_SOUND.play()
                if ai_decisions['decision2_fire_rocket'] and self.red_rocket_ammo > 0:
                    rocket = pygame.Rect(
                    self.red.x, self.red.y + self.red.height//2 - 2, ROCKET_WIDTH, ROCKET_HEIGHT)
                    self.red_rockets.append([rocket, ROCKET_VEL])
                    self.red_rocket_ammo -= 1
                    if not MUTE: ROCKET_FIRE_SOUND.play()

            self.handle_weapon(self.yellow_bullets, self.red_bullets, BULLET_VEL, TYPE0, False)
            self.handle_weapon(self.yellow_rockets, self.red_rockets, ROCKET_VEL, TYPE1, False)

            self.handle_weapon_acceleration(self.yellow_bullets, BULLET_VEL)
            self.handle_weapon_acceleration(self.red_bullets, BULLET_VEL)
            self.handle_weapon_acceleration(self.yellow_rockets, ROCKET_VEL)
            self.handle_weapon_acceleration(self.red_rockets, ROCKET_VEL)
            #self.handle_weapon_acceleration(self.sys_yellow_bullets, BULLET_VEL)
            #self.handle_weapon_acceleration(self.sys_red_bullets, BULLET_VEL)

            self.draw_window(self.red, self.yellow, self.red_bullets, self.yellow_bullets, self.red_rockets, self.yellow_rockets, 
                self.red_health, self.yellow_health, self.red_rocket_ammo, self.yellow_rocket_ammo, self.yellow_HB, self.red_HB,
                red_movement_type, yellow_movement_type, [], [])

            self.handle_spacecraft_acceleration(self.yellow_cur_vel, VEL)
            self.handle_spacecraft_acceleration(self.red_cur_vel, VEL)
            
        return behavior_metrics
    
    def random_bullet(self, quantity):
        x_coor = BORDER_X

        for _ in range(quantity):
            y_coor = random.randint(0, HEIGHT)
            if len(self.sys_red_bullets) < quantity:
                bullet = pygame.Rect(x_coor, y_coor, BULLET_WIDTH, BULLET_HEIGHT)
                self.sys_red_bullets.append(bullet)
            
        for _ in range(quantity):
            y_coor = random.randint(0, HEIGHT)
            if len(self.sys_yellow_bullets) < quantity:
                bullet = pygame.Rect(x_coor, y_coor, BULLET_WIDTH, BULLET_HEIGHT)
                self.sys_yellow_bullets.append(bullet)
    
    def push_rival_weapon(self, input, bullet_list, YELLOW):
        MAX_DIST = math.sqrt(WIDTH**2 + HEIGHT**2)
        for i in range(MAX_BULLET):
            if i < len(bullet_list):
                if YELLOW:
                    dist = math.dist([self.yellow.x, self.yellow.x], [bullet_list[i][0].x, bullet_list[i][0].y])
                else:
                    dist = math.dist([self.red.x, self.red.x], [bullet_list[i][0].x, bullet_list[i][0].y])
                input.append(dist / MAX_DIST)
            else:
                input.append(1.0)

    def push_self_weapon(self, input, bullet_list, YELLOW):
        MAX_DIST = math.sqrt(WIDTH**2 + HEIGHT**2)
        for i in range(MAX_BULLET):
            if i < len(bullet_list):
                if YELLOW:
                    dist = math.dist([self.red.x, self.red.x], [bullet_list[i][0].x, bullet_list[i][0].y])
                else:
                    dist = math.dist([self.yellow.x, self.yellow.x], [bullet_list[i][0].x, bullet_list[i][0].y])
                input.append(dist / MAX_DIST)
            else:
                input.append(1.0)

    def get_decision(self, net1, net2, explorer1, explorer2):
        def normalize(val):
            if val > 1.0:
                val = 1.0
            elif val < 0.0:
                val = 0.0
            return val 
        
        if explorer1.should_explore():
            decision1_movement = random.choice(list(movement_d.values()))
            decision1_fire_bullet = random.choice([True, False])
            decision1_fire_rocket = random.choice([True, False])
        else:
            scaled_x_self = normalize(self.yellow.x / (WIDTH * 0.5))
            scaled_y_self = normalize(self.yellow.y / HEIGHT)
            scaled_x_rival = normalize((self.red.x - (WIDTH * 0.5)) / (WIDTH * 0.5))
            scaled_y_rival = normalize(self.red.y / HEIGHT)
            scaled_red_health = normalize(self.red_health / HEALTH)
            scaled_yellow_health = normalize(self.yellow_health / HEALTH)
            scaled_rocket_self = normalize(self.yellow_rocket_ammo / MAX_ROCKET)

            input1 = [scaled_x_self, scaled_y_self, scaled_x_rival, scaled_y_rival, scaled_red_health, scaled_yellow_health, scaled_rocket_self]
            #print(input1)
            self.push_rival_weapon(input1, self.red_bullets, True)
            self.push_rival_weapon(input1, self.red_rockets, True)
            self.push_self_weapon(input1, self.yellow_bullets, True)
            self.push_self_weapon(input1, self.yellow_rockets, True)
            output1 = net1.activate(tuple(input1))
            decision1_movement, decision1_fire_bullet, decision1_fire_rocket = self.get_ai_decision(output1)
            #print("output1", output1)
            #print("output1 (weapon)", decision1_movement, decision1_fire_bullet, decision1_fire_rocket)


        # For red spacecraft
        if explorer2.should_explore():
            decision2_movement = random.choice(list(movement_d.values()))
            decision2_fire_bullet = random.choice([True, False])
            decision2_fire_rocket = random.choice([True, False])
        else:
            scaled_x_self = normalize((self.red.x - (WIDTH * 0.5))/ (WIDTH * 0.5))
            scaled_y_self = normalize(self.red.y / HEIGHT)
            scaled_x_rival = normalize(self.yellow.x / (WIDTH * 0.5))
            scaled_y_rival = normalize(self.yellow.y / HEIGHT)
            scaled_red_health = normalize(self.red_health / HEALTH)
            scaled_yellow_health = normalize(self.yellow_health / HEALTH)
            scaled_rocket_self = normalize(self.red_rocket_ammo / MAX_ROCKET)

            input2 = [scaled_x_self, scaled_y_self, scaled_x_rival, scaled_y_rival, scaled_red_health, scaled_yellow_health, scaled_rocket_self]

            self.push_rival_weapon(input2, self.yellow_bullets, False)
            self.push_rival_weapon(input2, self.yellow_rockets, False)
            self.push_self_weapon(input2, self.red_bullets, False)
            self.push_self_weapon(input2, self.red_rockets, False)

            #print(input2)
            
            output2 = net2.activate(tuple(input2))
            decision2_movement, decision2_fire_bullet, decision2_fire_rocket = self.get_ai_decision(output2)
            #print("output2", output2)
            #print("output2 (weapon)", decision2_movement, decision2_fire_bullet, decision2_fire_rocket)
            # Collecting the AI decisions into a dictionary
        #print(decision2_movement)
        ai_decisions = {
            'decision1_movement': decision1_movement,
            'decision1_fire_bullet': decision1_fire_bullet,
            'decision1_fire_rocket': decision1_fire_rocket,
            'decision2_movement': decision2_movement,
            'decision2_fire_bullet': decision2_fire_bullet,
            'decision2_fire_rocket': decision2_fire_rocket,
        }

        return ai_decisions

    def train_ai(self, genome1, genome2, config, start_time):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
        explorer1 = RandomActionExplorer()
        explorer2 = RandomActionExplorer()
        win_streak_yellow = 0
        win_streak_red = 0

        run = True
        while run:  # Training loop
            # Execute the loop function with AI decisions
            behavior_metrics = self.loop(run, net1, net2, explorer1, explorer2, AI=DIANNAO)
            elapsed_time = time.time() - start_time  # Calculate elapsed time
            #print(elapsed_time)

            if self.winner_text == "Yellow Wins!":
                win_streak_yellow += 1
                win_streak_red = 0
            elif self.winner_text == "Red Wins!":
                win_streak_red += 1
                win_streak_yellow = 0

            self.calculate_fitness(genome1, genome2, behavior_metrics, win_streak_yellow, win_streak_red)
            if elapsed_time > 60:
                run = False
            self.reset(False)
        # # Optional: You can decay epsilon after each round/iteration if desired.
        explorer1.decay_epsilon()
        explorer2.decay_epsilon()


    def calculate_fitness(self, genome1, genome2, behavior_metrics, win_streak_yellow, win_streak_red):
        def calculate_individual_fitness(base_health, damage_bonus, survival_bonus, idle_penalty, bullet_waste_penalty, danger_penalty, out_of_bounds_penalty, win_bonus, behavior_metrics, winner_text, target_text, win_streak, rocket_ammo):
            idle_count = behavior_metrics["idle_count"]
            bullet_used = behavior_metrics["bullet_used"]
            danger_count = behavior_metrics["danger_count"]
            out_of_bounds_count = behavior_metrics["out_of_bounds_count"]

            win_streak_bonus = 50
            rocket_waste_penalty = 20
            draw_penalty = -50
            damage_dealt = HEALTH - base_health
            fitness = CONSTANTS['base_fitness'] + damage_dealt * damage_bonus
            fitness += base_health * survival_bonus
            fitness += win_streak * win_streak_bonus
            # Penalize for undesirable behaviors
            fitness -= idle_count * idle_penalty
            fitness -= bullet_used * bullet_waste_penalty
            fitness -= danger_count * danger_penalty
            fitness -= out_of_bounds_count * out_of_bounds_penalty
            fitness -= (MAX_ROCKET - rocket_ammo) * rocket_waste_penalty
            fitness -= self.draw * draw_penalty

            if winner_text == target_text:
                fitness += win_bonus

            return fitness

        CONSTANTS = {
            'base_fitness': 100,
            'damage_bonus': 10,
            'win_bonus': 500,
            'survival_bonus': 5,
            'idle_penalty': 5,
            'bullet_waste_penalty': 3,
            'danger_penalty': 10,
            'out_of_bounds_penalty': 15,
        }

        yellow_behavior = behavior_metrics['yellow']
        red_behavior = behavior_metrics['red']

        genome1.fitness = calculate_individual_fitness(self.red_health, CONSTANTS['damage_bonus'], CONSTANTS['survival_bonus'], CONSTANTS['idle_penalty'], CONSTANTS['bullet_waste_penalty'], CONSTANTS['danger_penalty'], CONSTANTS['out_of_bounds_penalty'], CONSTANTS['win_bonus'], yellow_behavior, self.winner_text, "Yellow Wins!", win_streak_yellow, self.yellow_rocket_ammo)
        print("genome1.fitness: ", genome1.fitness)

        genome2.fitness = calculate_individual_fitness(self.yellow_health, CONSTANTS['damage_bonus'], CONSTANTS['survival_bonus'], CONSTANTS['idle_penalty'], CONSTANTS['bullet_waste_penalty'], CONSTANTS['danger_penalty'], CONSTANTS['out_of_bounds_penalty'], CONSTANTS['win_bonus'], red_behavior, self.winner_text, "Red Wins!", win_streak_red, self.red_rocket_ammo)
        print("genome2.fitness: ", genome2.fitness)



    def get_ai_decision(self, outputs):
        """
        Interpret the AI's outputs to determine the actions.
        Returns the chosen actions based on the values in the outputs.
        """
        # Decision for movement based on the highest value among the first four outputs
        movement_map = {
            0: movement.STAY,
            1: movement.LEFT,
            2: movement.RIGHT,
            3: movement.UP,
            4: movement.DOWN
        }

        movement_decision = movement_map[np.argmax(outputs[:4])]

        # Decision for firing bullet and rocket based on the last two outputs
        fire_bullet_decision = outputs[-2] > 0.5
        fire_rocket_decision = outputs[-1] > 0.5
        
        return movement_decision, fire_bullet_decision, fire_rocket_decision
