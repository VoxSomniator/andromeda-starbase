# hub for creature stats like movement speed and regeneration.
# maybe split this up later into more things if stats come from different sources. Inventory and etc.
from src.entities.components.component import Component

class Stats(Component):

    def __init__(self, owner, move_cost, regen):
        Component.__init__(self, owner)
        self.move_cost = move_cost
        self.regen = regen