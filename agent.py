# AI todolist:
# - reset
# - reward
# - play(action)
# - play(weapon)
# - game_iteration
# - end of the game
from enum import Enum
import main_agent

class rewards(Enum):
    DAMAGE_CAUSED = 0.1 #(the higher the better)
    DAMAGE_RECEIVERD = -0.1 #(the lower the better)
    WON = 5 #(bonus if won)
    WINNING_TIME = 1 #(the shorter the better given the game won)

class game(Enum):
    INITIAL = 0
    ONGOING = 1
    FINISHED = 2

class agent:
    def __init__(self):
        self.my_movement = [0, 0, 0, 0, 0]
        self.weapon = [0, 0, 0]
        self.rewards_arr = [0, 0, 0, 0]
        self.status = game.INITIAL
    
    def reset():
        main_agent.main()

    def update_game_status(self, game_status):
        self.status = game_status

    def update_parameter(my_coor, rival_coor, yellow_health, red_health,
                    yellow_bullets, red_bullets, yellow_rockets, red_rockets): # let the agent perceive the status of the game
        my_x, my_y = my_coor
        rival_x, rival_y = rival_coor