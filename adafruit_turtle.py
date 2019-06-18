import displayio
import board
import gc
import math

class color:
    WHITE = 0xFFFF
    BLACK = 0x0000
    RED =  0xF800
    BLUE = 0x001F


class turtle:

    def __init__(self, display=board.DISPLAY):
        self._display = display
        self._w = self._display.width
        self._h = self._display.height
        self._x = self._w//2
        self._y = self._h//2
        self._speed = 6
        self._heading = 90

        self._splash = displayio.Group(max_size=3)

        self._bg_bitmap = displayio.Bitmap(self._w, self._h, 1)
        self._bg_palette = displayio.Palette(1)
        self._bg_palette[0] = color.WHITE
        self._bg_sprite = displayio.TileGrid(self._bg_bitmap,
                                            pixel_shader=self._bg_palette,
                                            x=0, y=0)
        self._splash.append(self._bg_sprite)

        self._fg_bitmap = displayio.Bitmap(self._w, self._h, 5)
        self._fg_palette = displayio.Palette(5)
        self._fg_palette.make_transparent(0)
        self._fg_palette[1] = color.WHITE
        self._fg_palette[2] = color.BLACK
        self._fg_palette[3] = color.RED
        self._fg_palette[4] = color.BLUE
        self._fg_sprite = displayio.TileGrid(self._fg_bitmap,
                                            pixel_shader=self._fg_palette,
                                            x=0, y=0)
        self._splash.append(self._fg_sprite)

        self._turtle_bitmap = displayio.Bitmap(8, 8, 2)
        self._turtle_palette = displayio.Palette(2)
        self._turtle_palette.make_transparent(0)
        self._turtle_palette[1] = color.BLACK
        for i in range(4):
            self._turtle_bitmap[4-i, i] = 1
            self._turtle_bitmap[i, 4+i] = 1
            self._turtle_bitmap[4+i, 7-i] = 1
            self._turtle_bitmap[4+i, i] = 1
        self._turtle_sprite = displayio.TileGrid(self._turtle_bitmap,
                                            pixel_shader=self._turtle_palette,
                                            x=-100, y=-100)
        self._drawturtle()
        self._splash.append(self._turtle_sprite)

        self._penstate = False
        self._pencolor = None
        self.pencolor(color.BLACK)

        print("Splash!")
        self._display.show(self._splash)
        self._display.refresh_soon()
        gc.collect()
        self._display.wait_for_frame()

    def _drawturtle(self):
        self._turtle_sprite.x = self._x - 4
        self._turtle_sprite.y = self._y - 4


    # Turtle motion
    def forward(self, distance):
        x1 = int(self._x + math.sin(math.radians(self._heading))*distance)
        y1 = int(self._y + math.cos(math.radians(self._heading))*distance)
        x0 = self._x
        y0 = self._y
        print("From", x0, y0, "to", x1, y1)
        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = x1 - x0
        dy = abs(y1 - y0)
        err = dx / 2
        ystep = -1
        if y0 < y1:
            ystep = 1
        while x0 <= x1:
            if steep:
                self._fg_bitmap[y0, x0] = 1
                self._x = y0
                self._y = x0
                self._drawturtle()
            else:
                self._fg_bitmap[x0, y0] = 1
                self._x = x0
                self._y = y0
                self._drawturtle()
            err -= dy
            if err < 0:
                y0 += ystep
                err += dx
            x0 += 1

    def pencolor(self, c):
        #if not c in self.fg_palette:
        #    raise RuntimeError("Color must be one of the 'color' class items")
        self._pencolor = c

    # Tell turtle's state
    def pos(self):
        return (self._x - self._w//2, self._y - self._h//2)
    def position(self):
        return self.pos()

    # Pen control
    def pendown(self):
        self._penstate = True
    def pd(self):
        self.pendown()
    def down(self):
        self.pendown()
    def isdown(self):
        return self._penstate

    def penup(self):
        self._penstate = False
    def pu(self):
        self.penup()
    def up(self):
        self.penup()