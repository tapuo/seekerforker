#Poolの本体
class Pool:
    def __init__(self):
        self._entity = []
    
    def __iter__(self):
        yield from self._entity

    def __len__(self):
        return len(self._entity)

    def append(self, t):
        self._entity.append(t)

    def update(self):#全updateをまわし、生きてるのだけ残す
        self._entity = [t for t in self._entity if t.update()]

    def draw(self):
        for a in self._entity:
            a.draw()

#PoolManを継承したオブジェクトを通して生成とか更新をする
class PoolMan:
    _pool = None

    @classmethod
    def init(cls):
        cls._pool = Pool()
    
    @classmethod
    def update(cls):
        cls._pool.update()

    @classmethod
    def draw(cls):
        cls._pool.draw()

    @classmethod
    def length(cls):
        return len(cls._pool)

    @classmethod
    def pool(cls):
        return cls._pool

#分割対応版、Enemyで使う
class CPoolMan:
    #敵だけ分割して当たり判定　０と９はダミー
    _pool = None
    _cpool = [[] for i in range(10)]

    @classmethod
    def init(cls):
        cls._pool = Pool()
        cls._cpool = [[] for i in range(10)]
    # idx領域とその前後にアペンド
    @classmethod
    def cappend(cls, a, idx):
        cls._cpool[idx-1].append(a)
        cls._cpool[idx].append(a)
        cls._cpool[idx+1].append(a)

    @classmethod
    def draw(cls):
        cls._pool.draw()

    @classmethod
    def length(cls):
        return len(cls._pool)
    # idx領域のpool分を返す
    @classmethod
    def pool(cls, idx):
        return cls._cpool[idx]

    @classmethod
    def update(cls):
        cls._cpool = [[] for i in range(10)] #分割poolをリセット
        cls._pool.update() #cpoolへの再挿入はここでやっとるで

#分割用インデックス 1->8
def cpoolIndex(_y) -> int:
    return min(8, max(int(_y / 20)+1, 1))

