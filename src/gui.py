#gui
#各種uiの表示、なんかtweenがほしいな
import pyxel
import state
from blast import BlastPool
from shot import ShotPool
from enemy import EnemyPool
from bullet import BulletPool

#draw all
def draw():
    _draw_score()
    if state.scene == state.GAME_STAGE: #stageのみ描画
        _draw_life()
    #_draw_stat()

#score
def _draw_score():
    pyxel.text(12, 2, "1UP", 8)
    pyxel.text(8, 8, "{:5}".format(state.score), 7)
    pyxel.text(42, 2, "HIGH SCORE", 8)
    pyxel.text(54, 8, "{:5}".format(state.hiscore), 7)
    pyxel.text(100, 2, "TIME", 8)
    pyxel.text(92, 8, "{:>6.2f}".format(state.time), 7)

#HPゲージ、残機
def _draw_life():
    #player ダメージゲージ　満タン、ダメージを食らうと０になり、徐々に回復
    playerDcnt = max(0, state.damageCnt)
    c = 12 if playerDcnt <= 0 else 8
    w = (180 - playerDcnt) / 9
    pyxel.rect(2, 156, 20, 2, 1)
    pyxel.rect(2, 156, w, 2, c)
    #残機
    c = 12 if state.playerhp >= 4 else 1
    pyxel.rect(8,152,2,3,c)
    c = 12 if state.playerhp >= 3 else 1
    pyxel.rect(5,152,2,3,c)
    c = 12 if state.playerhp >= 2 else 1
    pyxel.rect(2,152,2,3,c)
    #boss
    w = state.bosshp
    c = 10 if w >= 20 else 8
    c = 12 if w >= 50 else c
    if w > 0:
        pyxel.rect(10, 14, 100, 2, 1)
        pyxel.rect(10, 14, w, 2, c)

#debug
def _draw_stat():
    pyxel.text(0, 20, "E:{0}".format(EnemyPool.length()), 15)
    pyxel.text(0, 26, "S:{0}".format(ShotPool.length()), 15)
    pyxel.text(0, 34, "B:{0}".format(BlastPool.length()), 15)
    pyxel.text(0, 40, "B:{0}".format(BulletPool.length()), 15)

#TODO ゲームオーバー時、ボーナス等なしのシンプル版
class GuiGameover:
    def __init__(self) -> None:
        self.t1 = "GAME OVER"
        # self.t2= "NO BONUS"
        self._d = self.draw1()

    def draw1(self):
        yield from range(5)
        #下から上がってくる
        for i in range(160,70,-1):
            pyxel.text(42, i, self.t1, 8)
            yield
        while True:
            pyxel.text(42, 70, self.t1, 8)
            yield

    def draw(self):
        next(self._d)

# クリア時のスコアカウント演出　残機、残タイマー、ボス撃破、倒した敵数等
# タイマーはちょびっと、残機はおおめ、
class GuiGameclear:
    def __init__(self) -> None:
        sc = state.score
        #この辺の数字は最後に決めるで
        lifeB = state.playerhp * 1000
        # bossB = 10000
        time = pyxel.ceil(state.time)
        timeB = int(time) * 100
        #          1234567890123456789012345
        total = lifeB + 10000 + timeB
        state.scoreAdd(total)
        self.t1 = "GAME CLEAR"
        self.t2 = "BONUS"
        self.t3 = "LIFE {0}x1000 = {1:5}".format(state.playerhp, lifeB)
        self.t4 = "BOSS CLEAR  = 10000"
        self.t5 = "TIME {0:2}x100 = {1:5}".format(time, timeB)
        # self.t6 = "TOTAL       = {0:5}".format(total)
        self.t6 = "1UP         = {0:5}".format(sc)
        self.t7 = "TOTAL SCORE = {0:5}".format(state.score)
        self._d = self.draw1()

    def t(self, y):
        # クリアボーナス
        pyxel.text(42, y + 70, self.t1, 8)

        pyxel.text(25, y + 80, self.t2, 10)
        pyxel.text(25, y + 86, self.t3, 10)
        pyxel.text(25, y + 92, self.t4, 10)
        pyxel.text(25, y + 98, self.t5, 10)
        pyxel.text(25, y + 104, self.t6, 10)
        pyxel.text(25, y + 120, self.t7, 7)

    def draw1(self):
        yield from range(5)
        #下から上がってくる
        for i in range(90,0,-1):
            self.t(i)
            yield
        while True:
            self.t(0)
            yield

    def draw(self):
        next(self._d)

class GuiTitle:
    def __init__(self) -> None:
        #          1234567890123456789012345
        self.t1 = "SEEKER FORKER"
        self.t2 = "PUSH A BUTTON"
        self.t3 = "90SEC MODE"
        self.t4 = "(C) 2022 LIMITCYCLE/UMMB"
        self._d = self.draw1()

    def draw1(self):
        yield from range(15)
        for i in range(40):
            pyxel.text(34, 60, self.t1, 10)
            yield
        for i in range(40):
            pyxel.text(34, 60, self.t1, 10)
            pyxel.text(12, 148, self.t4, 13)
            yield
        while True:
            for i in range(20):
                pyxel.text(34, 60, self.t1, 10)
                pyxel.text(34, 116, self.t2, 7)
                pyxel.text(12, 148, self.t4, 13)
                pyxel.text(40, 108, self.t3, 9)
                yield
            for i in range(20):
                pyxel.text(34, 60, self.t1, 10)
                pyxel.text(34, 116, self.t2, 1)
                pyxel.text(12, 148, self.t4, 13)
                pyxel.text(40, 108, self.t3, 9)
                yield

    def draw(self):
        next(self._d)

