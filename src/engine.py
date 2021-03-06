# game loop!
# start_game is called from Main on launch and contains the whole loop I guess.

from src import setup_game, rendering
import tcod
import time
from src import input_handlers
from src.command_stream.command import CommandType
from src.entities.entity import Entity
from src.world.level import Level
from src.world.tiles import Tile
from src.turns import TimeManager
from src.game_state import GameStates

from src.entities.components import player

# imports for testing entities
from src.entities.components import turn_taker
from src.entities.components import ai_jiggle
from src.entities.components import stats
from src.entities.components import vision


class Game:
    # the game. whole thing.

    def __init__(self):
        self.level = Level(200, 140)
        self.renderer = rendering.Renderer(rendering.Window(2, 2, 86, 41))

        # testing entities, move to spawning code somewhere later.
        self.player = Entity('Player', Tile('◉', (255, 255, 255)), 20, 20, solid=True)
        self.player.player = player.Player(self.player)
        self.player.turn_taker = turn_taker.TurnTaker(self.player)
        self.player.stats = stats.Stats(self.player, 1000, 200)
        self.level.add_entity(self.player)
        self.player.vision = vision.Vision(self.player, 30)

        test_critter = Entity(name='Critter', x=25, y=20, solid=True)
        test_critter.turn_taker = turn_taker.TurnTaker(test_critter)
        test_critter.ai = ai_jiggle.AiJiggle(test_critter)
        test_critter.stats = stats.Stats(test_critter, 1000, 100)
        self.level.add_entity(test_critter)

        # game state
        self.time_manager = TimeManager()
        self.current_entity = None # current entity taking its turn

        self.quit_game = False
        self.game_state = GameStates.PROCESS_TURNS

        self.start_game()

    def start_game(self):
        self.screen_changed = True

        tcod.console_set_custom_font('fonts/consolas12x12_gs_tc.png',
                                     tcod.FONT_LAYOUT_TCOD | tcod.FONT_TYPE_GREYSCALE)



        while not tcod.console_is_window_closed():

            # modes for different game states.

            """
            game loop order:
            start in PROCESS_TURNS mode.
            if turn-takers list is empty, tell time manager to tick all entities, and get list of current turn-takers
            for first item in list:
                if enemy, change state to ENEMY_TURN
                if player, PLAYER_TURN. later states like TARGET or INVENTORY will always go back to PLAYER_TURN.
                after either, remove entity from list and set state back to PROCESS_TURNS
            
            once in process_turns, if the list is empty, it will restart the process
            if the list is NOT empty, it will process the next entity.
            """

            if self.quit_game:
                # todo: saving and stuff
                return True

            if self.game_state == GameStates.PROCESS_TURNS:
                self.state_process_turn()

            if self.game_state == GameStates.PLAYER_TURN:
                self.state_player_turn()

            if self.game_state == GameStates.ENEMY_TURN:
                self.state_enemy_turn(self.current_entity)

            # update screen
            if self.screen_changed:
                self.update_screen()
                self.screen_changed = False

            time.sleep(0.012)  # this just makes the game pause between every loop so it doesn't throttle the CPU
                            # todo - button event queue thing

    def state_process_turn(self):
        # run the time managing, tick/advance entities. Default state that branches into other entity turns.
        self.current_entity = self.time_manager.get_next_turn(self.level.entities)

        # check if it's a player
        if self.current_entity.player:
            self.game_state = GameStates.PLAYER_TURN
            return

        else:
            self.game_state = GameStates.ENEMY_TURN
            return

    def state_player_turn(self):
        # process player turn. returns True to quit the game.
        # get first command from input
        command = input_handlers.handle_keys()

        # process command
        if command:
            if command.command_type is CommandType.quit:
                self.quit_game = True

            if command.command_type is CommandType.move:
                self.player.move(command.data)
                self.screen_changed = True
                self.game_state = GameStates.PROCESS_TURNS

    def state_enemy_turn(self, entity):
        if entity:
            if entity.ai:
                    entity.ai.turn()
        else:
            print("Problem- enemy turn called on None object")

        self.current_entity = None

        self.screen_changed = True  # todo - maybe make this smarter? small performance thing.
        self.game_state = GameStates.PROCESS_TURNS

    def update_screen(self):
        self.renderer.render_all(self.level, camera_x=self.player.x, camera_y=self.player.y, fov_entity=self.player)
