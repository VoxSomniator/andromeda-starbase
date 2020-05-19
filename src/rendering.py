"""
Rendering, viewports, fake "camera" and such.
I'm going to try to do some fancy tricks with multiple consoles in tcod for different game windows,
then layering them for the game screen.

Renderer object should store UI things like the position of sub-windows.
Renderer should be sent things that will change on unpredictable frames, like the current level/coordinates.
"""
import tcod

# eventually make this read from settings somewhere
screen_width = 90
screen_height = 55


class Window():
    # a description for a window/panel's location and size.
    # so far it's just a rectangle but additions might be useful later- background colors and console details, etc.

    def __init__(self, start_x, start_y, width, height):
        self.start_x = start_x
        self.start_y = start_y
        self.width = width
        self.height = height


class Renderer:

    def __init__(self, viewport_dimensions:Window):
        self.viewport = viewport_dimensions

        self.main_console: tcod.Console = tcod.console_init_root(w=screen_width,
                                                                 h=screen_height,
                                                                 title='Andromeda Starbase', fullscreen=False,
                                                                 renderer=tcod.RENDERER_SDL2, order='F',
                                                                 vsync=True)


    def render_all(self, level, camera_x, camera_y, fov_entity):
        # viewport x/y: position of the viewport on the screen
        # camera x/y: position of the viewport's in-world view

        # renders the WHOLE SCREEN. Call every frame/update for full refresh.

        viewport_console = self.render_viewport(level, camera_x, camera_y, self.viewport.width, self.viewport.height,
                                                fov_entity)

        self.main_console.clear(ch=ord(' '), fg=(255, 255, 255), bg=(255, 255, 255))

        # blit various panels onto main console
        viewport_console.blit(dest=self.main_console, dest_x=self.viewport.start_x, dest_y=self.viewport.start_y,
                              src_x=0, src_y=0, width=self.viewport.width, height=self.viewport.height)

        self.main_console.default_fg = (255, 255, 255)
        self.main_console.default_bg = (0, 0, 0)

        tcod.console_flush(console=self.main_console, keep_aspect=True, integer_scaling=True)
        pass

    def render_viewport(self, level, center_x, center_y, width, height, fov_entity):
        # renders the view of the world/level. Does not include UIs like targeting lines.
        # returns an offscreen console of the viewport. Coordinates are in level-space.
        # implement FOV here later.

        start_x = center_x - int(round(width/2.0))
        start_y = center_y - int(round(height/2.0))

        area_tiles = level.get_rect_tiles_in_fov(start_x, start_y, width, height, fov_entity=fov_entity)

        viewport_console = tcod.console.Console(width, height, 'F')

        for x in range(width):
            for y in range(height):
                viewport_console.default_fg = area_tiles[x][y].fg
                viewport_console.default_bg = area_tiles[x][y].bg
                viewport_console.put_char(x, y, ord(area_tiles[x][y].glyph))

        return viewport_console