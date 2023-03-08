# 星
import pyxel
import state

class Star:
    __slots__ = ['x', 'y', 's', 'c']
    def __init__(self, c):
        self.x = pyxel.rndf(0, pyxel.width)
        self.y = pyxel.rndf(0, pyxel.height)
        self.s = pyxel.rndf(0.2, [0.7, 1.7, 2.5][c]) #スピード
        self.c = c

class Background:
    def __init__(self):
        self._star = []
        # self.col1 = [[14,8,4],[1,14,4]] #点滅カラー msx
        # self.col2 = [[6,9,7],[4,9,15]] #ワープカラー msx
        self.col1 = [[1,4,5],[0,2,5]] #点滅カラー
        self.col2 = [[5,9,12],[12,8,6]] #ワープカラー
        for i in range(80):
            self._star.append(Star(0))
        for i in range(60):
            self._star.append(Star(1))
        for i in range(40):
            self._star.append(Star(2))

    def update(self):
        v = 8.0 if state.warpCnt <= 80 else 3.0
        v = 5.0 if state.warpCnt <= 40 else v
        v = 2.0 if state.warpCnt <= 20 else v
        for i in self._star:
            i.y = (i.y + i.s * v) % pyxel.height

    def draw(self):
        pyxel.cls(0) # ここで全画面クリア
        idx = 0 if pyxel.frame_count % 15 < 8 else 1
        if state.warpCnt < 0:
            for i in self._star:
                pyxel.pset(i.x, i.y, self.col1[idx][i.c])
        elif state.warpCnt >= 80: #ワープは男のロマンなので根性で描画
            for i in self._star:
                pyxel.pset(i.x, i.y, self.col2[idx][i.c])
                pyxel.pset(i.x, i.y-1, self.col2[idx][i.c])
                pyxel.pset(i.x, i.y-2, self.col1[idx][i.c])
                pyxel.pset(i.x, i.y-3, self.col1[idx][i.c])
        elif state.warpCnt >= 40:
            for i in self._star:
                pyxel.pset(i.x, i.y, self.col2[idx][i.c])
                pyxel.pset(i.x, i.y-1, self.col2[idx][i.c])
                pyxel.pset(i.x, i.y-2, self.col2[idx][i.c])
                pyxel.pset(i.x, i.y-3, self.col2[idx][i.c])
                pyxel.pset(i.x, i.y-4, self.col1[idx][i.c])
                pyxel.pset(i.x, i.y-5, self.col1[idx][i.c])
                pyxel.pset(i.x, i.y-6, self.col1[idx][i.c])
        elif state.warpCnt >= 20:
            for i in self._star:
                pyxel.pset(i.x, i.y, self.col2[idx][i.c])
                pyxel.pset(i.x, i.y-1, self.col2[idx][i.c])
                pyxel.pset(i.x, i.y-2, self.col2[idx][i.c])
                pyxel.pset(i.x, i.y-3, self.col1[idx][i.c])
                pyxel.pset(i.x, i.y-4, self.col1[idx][i.c])
        else:
            for i in self._star:
                pyxel.pset(i.x, i.y, self.col2[idx][i.c])
                pyxel.pset(i.x, i.y-1, self.col1[idx][i.c])
                pyxel.pset(i.x, i.y-1, self.col1[idx][i.c])
