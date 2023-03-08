# bulle actor とりあえずシンプルな直進弾のみで
from blast import *
from vec2 import Vec2
from sprite import Sprite
from pool import PoolMan
from player import Player

class BulletPool(PoolMan):
    @classmethod
    def create(cls, bullet, pos): #連動で消せるように作った親をもたせたほうがいいかな？
        cls._pool.append(bullet(pos))

    @classmethod
    def bomb(cls):
        for e in cls._pool:
            e.bomb()

class BulletEntity:
    def __init__(self):
        self.sprite:Sprite = None
        self.hp = 1
        self.atk = 1

    @property
    def pos(self):
        return self.sprite.pos
        
    def bomb(self):
        self.hp = 0

    def damage(self, atk): #bulletには特にいらんけど
        pass

    def dead(self): #死亡時の追加処理
        pass

    def update(self): #汎用
        if self.sprite.isOut():
            self.hp = 0
        self.sprite.pos += self.v
        return self.hp > 0

    def draw(self):
        self.sprite.draw()

# class BulletA(BulletEntity): #下　没
#     def __init__(self, p):
#         super().__init__()
#         self.sprite = Sprite(p.x, p.y, 'bulletA1')
#         self.v = Vec2(0, 3)

class BulletB(BulletEntity): #時期狙い
    def __init__(self, p):
        super().__init__()
        self.sprite = Sprite(p.x, p.y, 'bulletA1')
        self.v = (Player.player.pos - self.sprite.pos).normalize() * 3
