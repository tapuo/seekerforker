#Vec2,Rect
import pyxel

#べくとる
#乱数とかclampとかつけたい気もするが、余計な気もする
class Vec2:
    __slots__ = ['x','y']
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, v):
        return Vec2(self.x + v.x, self.y + v.y)

    def __sub__(self, v):
        return Vec2(self.x - v.x, self.y - v.y)

    def __mul__(self, a):
        return Vec2(self.x * a, self.y * a)

    def __truediv__(self, a):
        return Vec2(self.x / a, self.y / a)

    def __pos__(self):
        return Vec2(self.x, self.y)

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    @property
    def norm(self):
        return pyxel.sqrt(float(self.x * self.x + self.y * self.y))

    def normalize(self):
        l = pyxel.sqrt(float(self.x * self.x + self.y * self.y))
        return Vec2(self.x / l, self.y / l)

    def dot(self, v):
        return self.x * v.x + self.y * v.y

    def cross(self, v):
        return self.x * v.y - self.y * v.x

    @staticmethod
    def lerp(v1, v2, t:float):
        return v2 * t + v1 * (1.0 - t)

#矩形
class Rect:
    __slots__ = ['x','y','w','h']
    def __init__(self, x, y, w, h) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    #中心をずらす
    def offset(self, p):
        return Rect(self.x + p.x, self.y + p.y, self.w, self.h)
    #すり抜け無罪 :-)
    def intersect(self, r):
        return (max(self.x, r.x) <= min(self.x + self.w, r.x + r.w) and 
                max(self.y, r.y) <= min(self.y + self.h, r.y + r.h))

#test
def test():
    r1 = Rect(0,0,10,10)
    r2 = Rect(5,5,7,7)
    r3 = Rect(12,13,5,5)
    r4 = Rect(2,3,1,12)
    print("r1,r2 is " + str(r1.intersect(r2)))
    print("r1,r3 is " + str(r1.intersect(r3)))
    print("r1,r4 is " + str(r1.intersect(r4)))

if __name__ == "__main__":
    test()
