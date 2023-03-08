# shot actor 直進弾のみ
import pyxel
from vec2 import Vec2
from sprite import Sprite
from pool import PoolMan,cpoolIndex
import sound

class ShotPool(PoolMan):
    @classmethod
    def create(cls, shot, p):
        cls._pool.append(shot(p))

class ShotEntity:
    def __init__(self, p):
        self.sprite:Sprite = None
        self.hp = 1
        self.atk = 1
        self.cidx = cpoolIndex(p.y)

    @property
    def pos(self):
        return self.sprite.pos
        
    def hit(self, s):
        if self.sprite.intersect(s.sprite):
            self.damage(s.atk)
            s.damage(self.atk)
            return True
        return False

    def damage(self, atk):
        self.hp -= atk

    def update(self): #汎用
        if self.sprite.isOut():
            self.hp = 0
        self.sprite.pos += self.v
        self.cidx = cpoolIndex(self.sprite.pos.y)
        return self.hp > 0

    def draw(self):
        self.sprite.draw()

class ShotA(ShotEntity):
    def __init__(self, p):
        super().__init__(p)
        self.sprite = Sprite(p.x, p.y, 'shotB')
        self.v = Vec2(0, -4)
        self.hp = 1
        self.atk = 1

class ShotB(ShotEntity):
    def __init__(self, p):
        ShotPool.create(ShotB2, p + Vec2(5,2))
        ShotPool.create(ShotB2, p + Vec2(10,4))
        ShotPool.create(ShotB2, p + Vec2(-5,2))
        ShotPool.create(ShotB2, p + Vec2(-10,4))
        super().__init__(p)
        self.sprite = Sprite(p.x, p.y, 'shotB')
        self.v = Vec2(0, -3)
        self.hp = 1
        self.atk = 1

class ShotB2(ShotEntity):
    def __init__(self, p):
        super().__init__(p)
        self.sprite = Sprite(p.x, p.y, 'shotB')
        self.v = Vec2(0, -3)
        self.hp = 1
        self.atk = 1

class ShotC(ShotEntity):
    def __init__(self, p):
        sound.se(10, 0)
        ShotPool.create(ShotC1, p + Vec2(7,-4)) #これでいいのか？
        ShotPool.create(ShotC2, p + Vec2(-7,-4)) #もうちょっとなんかこう
        super().__init__(p)
        self.sprite = Sprite(p.x, p.y, 'shotB')
        self.v = Vec2(0, -5)
        self.hp = 1
        self.atk = 1

class ShotC1(ShotEntity):
    def __init__(self, p):
        super().__init__(p)
        self.sprite = Sprite(p.x, p.y, 'shotB')
        self.v = Vec2(1, -4)
        self.hp = 1
        self.atk = 1

class ShotC2(ShotEntity):
    def __init__(self, p):
        super().__init__(p)
        self.sprite = Sprite(p.x, p.y, 'shotB')
        self.v = Vec2(-1, -4)
        self.hp = 1
        self.atk = 1
