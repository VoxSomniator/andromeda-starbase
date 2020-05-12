# turn and time system.
from src.entities.components.turn_taker import TurnTaker
from operator import attrgetter

"""
This is going to be KIND OF a mess

see: http://www.roguebasin.com/index.php?title=An_elegant_time-management_system_for_roguelikes

every entity that does things will have a TurnTaker component.
These entities have an "energy" value. Taking actions pushes the energy down to negatives.

Every game loop/tick of time calls a turn_tick function in every TurnTaker.
One at a time, in any order, every entity's energy is increased by its Regen value. 
    Then if it's 0 or more, that entity is added to a current_turn list.
    
The current_turn list is sorted by energy- it will probably be slightly positive based on regen after increasing.

In order of most energy to least, every entity's energy is set back to 0 and it takes its turn.
    In case of equal energy, maybe sort this later but idk for now
    This may not come up depending on how granular ticks end up being, but it will give the advantage to
    faster creatures/quicker actions taken last turn.

Most AI things will call their AI component and take their turn, while the player entity's TurnTaker will
    switch to the "player input" gamestate and wait for instructions.


game state wise:
by default, in "PROCESS_TURNS" mode. Saves the current turn order, and when the player comes up, diverts to
    PLAYER_TURN mode.
"""

class TimeManager:

    def __init__(self):
        self.active_turn_takers = [] #  entities with non-negative energy waiting to take their turns.

    def process_tick(self, entities):
        # called whenever the active turn takers list is empty, to progress time and get new active entities.
        # no return, alters self.active_turn_takers. Only for internal use!
        self.active_turn_takers = []

        turn_takers = self.find_all_turn_takers(entities)  # turntaker components

        # tick all of them, add actives to the list
        for component in turn_takers:
            if component.tick():
                self.active_turn_takers.append(component)

        self.active_turn_takers.sort(key=attrgetter('energy'), reverse=True)

    def get_next_turn(self, entities):
        # called at the start of every PROCESS_TURNS loop.
        # if there are entities waiting to take their turns, return the first.
        # if no entities are waiting, process the next tick.

        while not self.active_turn_takers:
            self.process_tick(entities)

        return self.active_turn_takers.pop(0).owner

    def find_all_turn_takers(self, entities):
        # returns a list of TurnTaker objects. We don't need to deal with the entities they're part of I don't think.
        turn_takers = []

        for entity in entities:
            for component in entity.components:
                if isinstance(component, TurnTaker):
                    turn_takers.append(component)

        return turn_takers