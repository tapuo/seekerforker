#blast 爆発いろいろ
from sprite import SpriteAnime
from pool import PoolMan

class BlastPool(PoolMan):
    @classmethod
    def create(cls, blast, p):
        cls._pool.append(blast(p))
#
class BlastEntity:
    def __init__(self):
        self.sprite:SpriteAnime = None
        self.hp = 1
        self.task = self.task1()
    
    def task1(self):
        yield from range(self.sprite.size * self.sprite.rate) #wait
        self.hp = 0
        while True:
            yield

    def update(self):
        next(self.task)
        return self.hp > 0

    def draw(self):
        self.sprite.draw()

class BlastA(BlastEntity):
    def __init__(self, p):
        super().__init__()
        self.sprite = SpriteAnime(p.x, p.y, 'blastA', False)

class BlastB(BlastEntity):
    def __init__(self, p):
        super().__init__()
        self.sprite = SpriteAnime(p.x, p.y, 'blastB', False)
