# player actor
# 自機　アーベ・ツァデ
# ダメージ制、３秒ほどショットが止まる
import pyxel
from sprite import Sprite
from pool import cpoolIndex
from shot import ShotPool,ShotC
from blast import BlastPool,BlastA
import pad
import state
from cam import Cam
import sound

class Player:
    player = None

    @classmethod
    def create(cls):
        cls.player = Player()
        return cls.player

    def __init__(self):
        self.sprite = Sprite(60, 180, 'player')
        self.sprite.flash(100)
        self.hp = 4
        self.atk = 1 #体当たり防止、無敵時は０
        self.cidx = cpoolIndex(180)
        self.damageCnt = 0 #ダメージカウンター
        self.task = self.taskStart()
    #task
    def taskMain(self):
        while True:
            #clear check
            if state.scene == state.GAME_BOSSDEAD:
                self.task = self.taskClear()
            #control
            self.sprite.pos += pad.dpadVec2() * 1.5
            self.sprite.clamp()
            self.cidx = cpoolIndex(self.sprite.pos.y)
            if self.damageCnt <=0 and pad.btnShot():
                ShotPool.create(ShotC, self.sprite.pos)
            # if pad.btnBomb():
            #     state.bombBegin = True
            yield
    
    def taskStart(self): # スタート時、下から出てくる
        state.warpCnt = 100
        for r in range(46):
            y = 180 - pyxel.sin(r * 2) * 80
            self.sprite.pos.y = y
            yield
        yield from range(10)
        for y in range(100,130):
            self.sprite.pos.y = y
            yield
            yield
        self.isDemo = False
        self.task = self.taskMain()
        yield
        
    def taskClear(self): # 上に飛んでく
        yield from range(120)
        state.warpCnt = 100
        yield from range(30)
        for r in range(90):
            y = (1 - pyxel.cos(r)) * 160
            self.sprite.pos.y -= y
            yield
        yield from range(30)
        state.scene = state.GAME_CLEAR
        while True:
            yield
        
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
        if self.damageCnt > 0: #無敵
            return
        self.damageCnt = 180
        self.sprite.flash(180) #光ったり揺れたりするぞ
        Cam.shake()
        sound.se(11,5)
        self.hp -= atk
        if(self.hp <= 0): #死亡時は爆発
            BlastPool.create(BlastA, self.pos)

    def update(self):
        self.damageCnt -= 1
        self.atk = 0 if self.damageCnt > 0 else 1
        state.playerStatus(self)
        next(self.task)
        return self.hp > 0

    def draw(self):
        #無敵
        if self.damageCnt > 0:
            c = pyxel.frame_count % 16
            r = pyxel.frame_count % 4 + 8
            pyxel.circb(int(self.pos.x), self.pos.y-2, r, c)
        self.sprite.draw()
