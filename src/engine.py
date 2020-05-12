# game loop!
# start_game is called from Main on launch and contains the whole loop I guess.

from src import setup_game
import tcod
import time
from src import input_handlers
from src.command_stream.command import CommandType
from src.entities.entity import Entity
from src.world.level import Level
from src.world.tiles import Tile
from src.turns import process_tick
from src.game_state import GameStates

# imports for testing entities
from src.entities.components import turn_taker
from src.entities.components import ai_jiggle


class Game:
    # the game. whole thing.

    def __init__(self):
        self.constants = setup_game.get_constants()
        self.player = Entity('Player', Tile('◉', (255, 255, 255)), 20, 20, solid=True)
        self.level = Level(90, 55)
        self.level.add_entity(self.player)

        self.quit_game = False
        self.game_state = GameStates.PLAYER_TURN

        test_critter = Entity(name='Critter', x=30, y=30, solid=True)
        test_critter_turns = turn_taker.TurnTaker(test_critter, 100)
        test_critter_jiggle = ai_jiggle.AiJiggle(test_critter)
        test_critter.add_component(test_critter_turns)
        test_critter.add_component(test_critter_jiggle)
        self.level.add_entity(test_critter)

        self.start_game()

    def start_game(self):
        self.screen_changed = True

        tcod.console_set_custom_font('fonts/consolas12x12_gs_tc.png',
                                     tcod.FONT_LAYOUT_TCOD | tcod.FONT_TYPE_GREYSCALE)

        self.main_console:tcod.Console = tcod.console_init_root(w=self.constants['screen_width'],
                                                                h=self.constants['screen_height'],
                                                                title=self.constants['window_title'], fullscreen=False,
                                                                renderer=self.constants['renderer'], order='F',
                                                                vsync=True)

        while not tcod.console_is_window_closed():

            # modes for different game states.

            if self.quit_game:
                # todo: saving and stuff
                return True

            if self.game_state == GameStates.PLAYER_TURN:
                self.state_player_turn()

            if self.game_state == GameStates.ENEMY_TURN:
                self.state_enemy_turn()

            # update screen
            if self.screen_changed:
                self.update_screen(self.main_console)
                self.screen_changed = False

            time.sleep(0.04)  # this just makes the game pause between every loop so it doesn't throttle the CPU
                            # todo - button event queue thing

    def begin_player_turn(self):
        # called by the player's Player component, on the player's turn in order.
        self.game_state = GameStates.PLAYER_TURN

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
                self.game_state = GameStates.ENEMY_TURN

    def state_enemy_turn(self):
        process_tick(entities=self.level.entities)
        self.screen_changed = True  # todo - maybe make this smarter? small performance thing.
        self.game_state = GameStates.PLAYER_TURN

    def update_screen(self, console:tcod.Console):
        # clear screen
        console.clear(ch=ord(' '), fg=(255, 255, 255), bg=(0, 0, 0))

        # draw new things, player etc
        tiles = self.level.display_map()
        for x in range(self.level.width):
            for y in range(self.level.height):
                console.default_fg = tiles[x][y].fg
                console.default_bg = tiles[x][y].bg
                console.put_char(x, y, ord(tiles[x][y].glyph))

        console.default_fg = (255, 255, 255)
        console.default_bg = (0, 0, 0)

        # flush console to screen
        tcod.console_flush(console)
