# Enemy actor
# クラスメソッド多過ぎか？
import pyxel
from vec2 import Vec2
from sprite import Sprite,SpriteAnime
import state
from pool import CPoolMan,cpoolIndex
from bullet import BulletPool,BulletB
from blast import BlastPool,BlastA,BlastB
from player import Player
import sound
from cam import Cam

class EnemyPool(CPoolMan):
    @classmethod
    def create(cls, enemy, pos, idx):
        e = enemy(pos, idx)
        cls._pool.append(e)
        cls._cpool[0].append(e)

    @classmethod
    def isAlive(cls): #ウェーブ終了待ち専用
        while len(cls._pool) > 0:
            yield

    @classmethod
    def bomb(cls):
        for e in cls._pool:
            e.bomb()

class EnemyEntity:
    def __init__(self, idx):
        self.hp = 1
        self.idx = idx #編隊内でのindex、弾を撃つとかのラベルに使う
        self.sprite:Sprite = None #型ヒント慣れないなあ
        self.score = 0 #撃破時
        self.dscore = 0 #ショットを当てたとき（主にボス用）
        self.task = None #実態はサブクラスで定義
        self.blast = BlastA #爆発パターン
        self.damageSe = 0 #ダメージ音、定義したときだけ鳴らす

    def taskend(self): # 画面外に出るまで待って消す
        while not self.sprite.isOut():
            yield
        self.hp = 0
        while True:
            yield

    @property
    def pos(self):
        return self.sprite.pos

    def bomb(self): #音なし、爆発あり、スコアあり、一応deadと分けとく
        self.hp = 0
        state.scoreAdd(self.score)
        BlastPool.create(self.blast, self.pos)

    def damage(self, atk:int):
        if not self.sprite.isIn(): #少し見えてからじゃないと当たらんよ
            return
        self.hp -= atk
        self.sprite.flash(20)
        state.scoreAdd(self.dscore)
        if self.damageSe:
            sound.se(self.damageSe, 5)
        if self.hp <= 0:
            self.dead()

    def dead(self): #死亡時の処理（音とか爆発とか）
        state.scoreAdd(self.score)
        sound.se(11, 3)
        BlastPool.create(self.blast, self.pos)

    def update(self):
        next(self.task)
        self.sprite.pos += self.v
        if self.hp > 0: # 生きてる場合は移動後の領域で再代入
            EnemyPool.cappend(self, cpoolIndex(self.sprite.pos.y))
        return self.hp > 0

    def draw(self):
        self.sprite.draw()

#
# 敵個別設定
#
def rc2vec(row, col): #15x20マス
    return Vec2(row * 8 + 4, -col * 8 - 4)

#A1 Ｌ字
class EnemyA(EnemyEntity):
    @staticmethod
    def create(x):
        EnemyPool.create(EnemyA, rc2vec(x, 0), 0)

    def __init__(self, p, idx):
        super().__init__(idx)
        self.sprite = Sprite(p.x, p.y, 'enemyA3')
        self.v = Vec2(0, 1.0)
        self.score = 100
        self.dscore = 10
        self.hp = 10
        self.atk = 1
        self.dx = 0.05 if p.x < 60 else -0.05
        self.task = self.task1()

    def task1(self):
        #1
        while self.pos.y < 80:
            yield
        #2
        BulletPool.create(BulletB, self.pos)
        for i in range(10):
            self.v.x += self.dx
            yield
        BulletPool.create(BulletB, self.pos)
        for i in range(10):
            self.v.x += self.dx
            yield
        BulletPool.create(BulletB, self.pos)
        for i in range(10):
            self.v.x += self.dx
            yield
        self.task = self.taskend()
        yield

#等速直進 idx==1 bullet
class EnemyB(EnemyEntity):
    @staticmethod
    def create(dx, w, h):
        for y in range(h):
            for x in range(w):
                EnemyPool.create(EnemyB, rc2vec(x*2+dx, y*2+1), 0)
        for x in range(w): #最終列は弾
            EnemyPool.create(EnemyB, rc2vec(x*2+dx, h*2+1), 1)

    def __init__(self, p, idx):
        super().__init__(idx)
        self.sprite = Sprite(p.x, p.y, 'enemyA5')
        self.v = Vec2(0, 1.2)
        self.score = 30
        self.hp = 1
        self.atk = 1
        self.task = self.task1()

    def task1(self):
        #1
        while self.pos.y < 15:
            yield
        if self.idx == 1:
            BulletPool.create(BulletB, self.pos)
        self.task = self.taskend()
        yield

# 上から出てきて整列し、一段ずつ降りる
class EnemyC(EnemyEntity):
    @staticmethod
    def create(dx, w, h):
        for y in range(h):
            for x in range(w):
                EnemyPool.create(EnemyC, rc2vec(x*2+dx, y+1), x+y*w)

    def __init__(self, p, idx):
        super().__init__(idx)
        self.sprite = Sprite(p.x, p.y, 'enemyA1')
        self.v = Vec2(0, 0)
        self.score = 10
        self.dscore = 10
        self.hp = 4
        self.atk = 1
        self.task = self.task1()

    def task1(self):
        #idx分待つ
        yield from range(self.idx * 5)
        #1
        self.v.y = 3.0
        while self.v.y > 0:
            self.v.y -= 0.07
            yield
        self.v.y = 0
        #揃うまで待つ
        yield from range(120 - self.idx % 6 * 5)
        #一段ずつ進む
        while not self.sprite.isOut():
            while self.v.y <= 1.0:
                self.v.y += 0.1
                yield
            self.v.y = 0
            yield from range(20)
        self.task = self.taskend()
        yield

#上で停止、弾、加速
class EnemyD(EnemyEntity):
    @staticmethod
    def create(x, y, idx):
        EnemyPool.create(EnemyD, rc2vec(x*2+2, y*2 + 2), idx)

    def __init__(self, p, idx):
        super().__init__(idx)
        self.sprite = Sprite(p.x, p.y, 'enemyA2')
        self.v = Vec2(0, 0.2)
        self.score = 30
        self.dscore = 10
        self.hp = 3
        self.atk = 1
        self.task = self.task1()

    def task1(self):
        while self.pos.y < -16:
            yield
        self.v.y = 2.0
        #1 減速して停止
        while self.v.y > 0:
            self.v.y -= 0.04
            yield
        self.v.y = 0
        #2 ウエイトと弾
        if self.idx == 1:
            BulletPool.create(BulletB, self.pos)
        yield from range(15)
        #3 加速して離脱
        while self.v.y < 3.0:
            self.v.y += 0.1
            yield
        self.v.y = 3.0
        self.task = self.taskend()
        yield
#画面端にちょこっと出て弾を撃って画面を横切り逃げていく　idxで位置 0-3
class EnemyE(EnemyEntity):
    @staticmethod
    def create(idx):
        EnemyPool.create(EnemyE, Vec2(0,0), idx)

    def __init__(self, p, idx):
        super().__init__(idx)
        #左上から反時計回りに4カ所
        p = [Vec2(-10, 40),Vec2(-10, 120),Vec2(130, 40),Vec2(130, 120)][idx]
        self.sprite = Sprite(p.x, p.y, 'enemyA6')
        self.v = [Vec2(1, 0),Vec2(1, 0),Vec2(-1, 0),Vec2(-1, 0)][idx]
        self.dx = 0.05 * [1,1,-1,-1][idx]
        self.score = 70
        self.dscore = 10
        self.hp = 5
        self.atk = 1
        self.task = self.task1()

    def task1(self):
        #1 画面端出現
        while not (2 < self.pos.x < 118):
            yield
        _v = self.v
        self.v = Vec2(0,0)
        #2 弾
        yield from range(10)
        BulletPool.create(BulletB, self.pos)
        yield from range(40)
        BulletPool.create(BulletB, self.pos)
        yield from range(30)
        #3 加速して離脱
        self.v = _v
        while -3.0 < self.v.x < 3.0:
            self.v.x += self.dx
            yield
        self.task = self.taskend()
        yield

# ボス　ビエラ・バスチラ 耐久でenemyFをばらまきつづける
class EnemyBoss1(EnemyEntity):
    @staticmethod
    def create():
        EnemyPool.create(EnemyBoss1, Vec2(60,-16), 0)

    def __init__(self, p, idx):
        super().__init__(idx)
        self.sprite = Sprite(p.x, p.y, 'enemyB1')
        self.v = Vec2(0, 0)
        self.score = 1000
        self.dscore = 10
        self.hp = 100
        self.atk = 1
        self.fMove = False
        self.task = self.task1()
        self.deg = 0.0

    def task1(self):
        #1
        self.v.y = 2.8
        while self.v.y > 0:
            self.v.y -= 0.07
            yield
        self.v.y = 0
        yield from range(30)
        self.fMove = True
        #2 弾 ３段階ぐらいに発展
        while self.hp > 50:
            yield from range(45)
            for i in range(10):
                EnemyPool.create(EnemyF, self.pos , 0)
            yield from range(45)
        EnemyPool.create(EnemyG, self.pos , 0)
        while self.hp > 20:
            yield from range(30)
            for i in range(30):
                EnemyPool.create(EnemyF, self.pos , 0)
            yield from range(30)
            EnemyPool.create(EnemyG, self.pos , 0)
            yield from range(30)
            for i in range(30):
                EnemyPool.create(EnemyF, self.pos , 0)
            yield from range(30)
        while True:
            yield from range(20)
            for i in range(20):
                EnemyPool.create(EnemyF, self.pos , 0)
            yield from range(20)
            EnemyPool.create(EnemyG, self.pos , 0)
   
   #ボス専用
    def update(self):
        state.bosshp = self.hp #とりあえず
        if self.fMove:
            self.pos.x = 60 + pyxel.sin(self.deg) * 40
            self.deg += 1.5
        # return super().update()
        next(self.task)
        self.sprite.pos += self.v
        if self.hp > 0:
            EnemyPool.cappend(self, cpoolIndex(self.sprite.pos.y)) # 移動後の領域で再代入
        else:
            Cam.shake()
            state.bombBegin = True
            sound.se(14,10)

        return self.hp > 0

#ボス弾、情報にランダムにばらまいて、しかる後に時期狙いで直進
class EnemyF(EnemyEntity):
    def __init__(self, p, idx):
        super().__init__(idx)
        self.sprite = SpriteAnime(p.x, p.y, 'enemyC')
        self.tp = Vec2(pyxel.rndf(10,110), pyxel.rndf(10,30))
        self.v = (self.tp - self.pos).normalize() * pyxel.rndf(2.0, 2.8)
        self.score = 10
        self.hp = 1
        self.atk = 1
        self.blast = BlastB
        self.task = self.task1()

    def task1(self):
        #1
        ve = (Player.player.pos - self.tp).normalize() * 3.0
        vs = self.v
        r = pyxel.rndi(50,80)
        rf = float(r)
        for i in range(r):
            self.v = Vec2.lerp(vs, ve, float(i) / rf)
            yield

        self.task = self.taskend()
        yield

class EnemyG(EnemyEntity):
    def __init__(self, p, idx):
        super().__init__(idx)
        self.sprite = SpriteAnime(p.x, p.y, 'bulletB')
        self.v = (Player.player.pos - self.pos).normalize() * 0.8
        self.score = 200
        self.hp = 4
        self.atk = 1
        # self.blast = BlastB
        self.damageSe = 15
        self.task = self.taskend()
