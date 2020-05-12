# measures energy for turns, is accessed by the Time Manager.
# the method to start an entity's turn will be here. TurnTaker will have to nudge the connected AI.
from src.entities.components.component import Component


class TurnTaker(Component):

    def __init__(self, owner, regen):
        Component.__init__(self, owner=owner)

        self.energy = 0 #  energy starts at 0, is pushed negative by actions
        self.regen = regen #  regeneration per tick

    def tick(self):
        # Called by the time manager every tick for every entity.
        # regenerates energy, then if it's positive, returns True.
        # the time manager will sort entities currently taking their turn, then call take_turn on each.
        self.energy += self.regen

        if self.energy >= 0:
            return True

        return False

    def take_turn(self):
        self.energy = 0 # sets back to 0 before taking action. No multi-turn energy buildup (yet?)
        print("entity ", self.owner.name, " taking turn!")

        # searches other attached components for a turn() function and calls it- will be in AI or Player components.
        for component in self.owner.components:
            if callable(getattr(component, 'turn', False)):
                component.turn()

        self.energy -= 500

    def change_energy(self, difference):
        self.energy += difference
