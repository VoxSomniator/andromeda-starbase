from src.entities.components.component import Component
import tcod


class Vision(Component):
    # stores an entity's field of view maps and level memory.
    # accessed to check if cells are in field-of-view.

    def __init__(self, owner, radius):
        Component.__init__(self, owner)
        self.radius = radius

        self.fov_map:tcod.map.Map = tcod.map.Map(5, 5)
        self.update_fov()

    def update_fov(self):
        self.fov_map = self.owner.level.get_fov_map()
        self.fov_map.compute_fov(self.owner.x, self.owner.y, self.radius, True, tcod.FOV_PERMISSIVE_7)

    def is_square_visible(self, x, y):
        if x < 0 or x >= self.fov_map.width or y < 0 or y >= self.fov_map.height:
            return False
        else:
            return self.fov_map.fov[y][x]

