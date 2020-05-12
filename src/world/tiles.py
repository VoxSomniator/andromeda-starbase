# Characters displayed to the screen. Holds glyphs and colors neatly.
# later, functions for visual effects- like tile.dark returning the dark version, tile.fire returning a burning version


class Tile:

    def __init__(self, glyph, fg_color, bg_color=(0, 0, 0)):
        # glyph is a character, color is a (int, int, int) but can use the dictionary
        self.glyph = glyph
        self.fg = fg_color
        self.bg = bg_color