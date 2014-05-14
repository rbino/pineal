from imports import *
import colorsys

class Color:
    def __init__(self, h=0, map=None):
        self._h = float(h) if 0.0<=float(h)<=1.0 else float(h)%1.0
        self.r, self.g, self.b = 0,0,0
        self._hsv_start, self._hsv_end = 0.0, 1.0
        if map:
            self.map = map
        self.map()

    # methods to map h to (r,g,b)
    # map() is the default
    def grey(self):
        self.map = self.grey
        self.r, self.g, self.b = [self._h]*3
        return self
    def hsv(self, *args):
        self.map = self.hsv

        if len(args)==2:
            self._hsv_start, self._hsv_end = args

        h = self._hsv_start + (self._hsv_end-self._hsv_start)*self._h
        self.r, self.g, self.b = colorsys.hsv_to_rgb(h,1,1)
        return self
    def black(self):
        self.map = self.black
        self.r, self.g, self.b = [0.0]*3
        return self
    def white(self):
        self.map = self.white
        self.r, self.g, self.b = [1.0]*3
        return self
    def mono(self, *args):
        self.map = self.mono
        if len(args)==3:
            self.r, self.g, self.b = args
    map = grey
    #

    def __float__(self):
        return self._h

    def __add__(self, f):
        return Color(self._h + f, self.map).map()
    __radd__ = __add__

    def __sub__(self, f):
        return Color(self._h - f, self.map).map()
    def __rsub__(self, f):
        return Color(f - self._h, self.map).map()

    def __div__(self, f):
        return Color(self._h / f, self.map).map()
    def __rdiv__(self, f):
        return Color(f / self._h, self.map).map()

    def __mul__(self, f):
        return Color(self._h * f, self.map).map()
    __rmul__ = __mul__

    def __iter__(self):
        return (self.r, self.g, self.b)

    def __call__(self, h=None):
        if not h:
            return self._h
        else:
            self._h = self._h = float(h) if 0.0<=float(h)<=1.0 else float(h)%1.0
            self.map()