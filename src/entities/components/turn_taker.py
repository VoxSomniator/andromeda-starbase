# measures energy for turns, is accessed by the Time Manager.
# the method to start an entity's turn will be here. TurnTaker will have to nudge the connected AI.
from src.entities.components.component import Component


class TurnTaker(Component):

    def __init__(self, owner):
        Component.__init__(self, owner=owner)

        self.energy = 0 #  energy starts at 0, is pushed negative by actions

    def tick(self):
        # Called by the time manager every tick for every entity.
        # regenerates energy, then if it's positive, returns True.
        # the time manager will sort entities currently taking their turn, then call take_turn on each.
        if self.owner.stats:
            self.energy += self.owner.stats.regen

        if self.energy >= 0:
            return True

        return False

    def change_energy(self, difference):
        self.energy += difference
