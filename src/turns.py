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
"""

def process_tick(entities):
    # called every game loop to do entity logic.
    print("debug- tick called.")

    turn_takers = find_all_turn_takers(entities)  # turntaker components
    active_turn_takers = []  # those with non-negative energy

    # tick all of them, add actives to the list
    for component in turn_takers:
        if component.tick():
            active_turn_takers.append(component)

    active_turn_takers.sort(key=attrgetter('energy'), reverse=True)

    # set off turns for active entities in order.
    for component in active_turn_takers:
        component.take_turn()


    return

def find_all_turn_takers(entities):
    # returns a list of TurnTaker objects. We don't need to deal with the entities they're part of I don't think.
    turn_takers = []

    for entity in entities:
        for component in entity.components:
            if isinstance(component, TurnTaker):
                turn_takers.append(component)

    return turn_takers