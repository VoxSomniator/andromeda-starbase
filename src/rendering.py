"""
Rendering, viewports, fake "camera" and such.
I'm going to try to do some fancy tricks with multiple consoles in tcod for different game windows,
then layering them for the game screen.
"""
import tcod


def render_all(console, level, screen_width, screen_height, viewport_x, viewport_y, viewport_width, viewport_height,
               camera_x, camera_y):
    # viewport x/y: position of the viewport on the screen
    # camera x/y: position of the viewport's in-world view

    # renders the WHOLE SCREEN. Call every frame/update for full refresh.

    viewport_console = render_viewport(level, camera_x, camera_y, viewport_width, viewport_height)

    console.clear(ch=ord(' '), fg=(255, 255, 255), bg=(255, 255, 255))

    # blit various panels onto main console
    viewport_console.blit(dest=console, dest_x=viewport_x, dest_y=viewport_y, src_x=0, src_y=0,
                          width=viewport_width, height=viewport_height)

    console.default_fg = (255, 255, 255)
    console.default_bg = (0, 0, 0)

    tcod.console_flush(console)
    pass

def render_viewport(level, start_x, start_y, width, height):
    # renders the view of the world/level. Does not include UIs like targeting lines.
    # returns an offscreen console of the viewport. Coordinates are in level-space.
    # implement FOV here later.

    area_tiles = level.get_rect_tiles(start_x, start_y, width, height)

    viewport_console = tcod.console.Console(width, height, 'F')

    for x in range(width):
        for y in range(height):
            viewport_console.default_fg = area_tiles[x][y].fg
            viewport_console.default_bg = area_tiles[x][y].bg
            viewport_console.put_char(x, y, ord(area_tiles[x][y].glyph))

    return viewport_console
    pass