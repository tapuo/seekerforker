#sprite　座標当たり判定bltパターンなどの管理。ごちゃごちゃしてんなー
#計算ももうちょい省いた方がいい気もするが、気にするほどの負荷でもないかもしれない、しらんけど
import pyxel
from vec2 import Vec2,Rect
from res import spriteData,spriteCollider,animeData

class Sprite:
    def __init__(self, x, y, pat):
        self.pos = Vec2(x,y) #基点は左上のほうがええんかのう
        self._imgrect:Rect = spriteData(pat)
        self._hitrect:Rect = spriteCollider(pat)
        self._flipX = 1 #必要になったらどうにか
        self._flipY = 1
        self._bank = 0
        self._colorkey = 0
        self._flashCnt = 0 # 正の時は点滅（点滅させたいフレーム数だけぶっ込む）
    #パターン切り替え
    def pattern(self, pat):
        self._imgrect = spriteData(pat)
    #範囲チェック
    def clamp(self):
        self.pos.x = min(pyxel.width - self._imgrect.w / 2, max(self.pos.x, self._imgrect.w / 2))
        self.pos.y = min(pyxel.height - self._imgrect.h / 2, max(self.pos.y, self._imgrect.h / 2))
    #完全に画面の外（死亡判定用）
    def isOut(self):
        return not (-self._imgrect.w < self.pos.x < pyxel.width + self._imgrect.w and
                    -self._imgrect.h < self.pos.y < pyxel.height + self._imgrect.w)
    #中心が画面内（あたり判定用） でかキャラ用に描画領域をトリミングした上で2px程度に狭めたい
    def isIn(self):
        return 0 < self.pos.x < pyxel.width and 0 < self.pos.y < pyxel.height
    #当たり判定
    @property
    def hitrect(self) -> Rect:
        return self._hitrect.offset(self.pos)

    def intersect(self, s):
        return self.hitrect.intersect(s.hitrect)
    
    def flash(self, t):
        self._flashCnt = t

    def draw(self):
        self._flashCnt -= 1
        if self._flashCnt > 0 and pyxel.frame_count % 4 < 2:
            return
        pyxel.blt(  self.pos.x - self._imgrect.w / 2, self.pos.y - self._imgrect.h / 2, self._bank, 
                    self._imgrect.x, self._imgrect.y,
                    self._imgrect.w * self._flipX, self._imgrect.h * self._flipY, self._colorkey)

#名前テーブルをループさせるためだけの簡易リングバッファ
class RingBuf:
    def __init__(self, _data:list, _isLoop) -> None:
        self.data = _data # list
        self.size = len(_data)
        self.idx = -1
        self.isLoop = _isLoop
    
    def get(self): #もうちょいすっきり書けんかね
        if self.isLoop:
            self.idx = (self.idx + 1) % self.size
        else:
            self.idx = min(self.idx + 1, self.size - 1)
        return self.data[self.idx]

#アニメ対応 データの差し替えどうすべ、いらんか？　いらんな。停止ぐらいは入れてもいい
class SpriteAnime(Sprite):
    def __init__(self, x, y, _data, _loop = True):
        data = animeData(_data)
        super().__init__(x, y, data[0])
        self.animpat = RingBuf(data, _loop)
        self.patcnt = 0
        self.size = len(data)
        self.rate = 3 # フレームレートは共通でいいとは思うけどどうか

    def draw(self): #patの更新はupdateでやるべきかなあ
        self.patcnt += 1
        if self.patcnt >= self.rate:
            self.patcnt = 0
            self.pattern(self.animpat.get())
        super().draw()
