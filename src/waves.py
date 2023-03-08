#Wave 敵の出現管理
#１ウェーブを一括で作る、敵がいなくなったら次のウェーブ
#enemyとwaveは基本的にセットで仕込みたいが、ファイルが分かれてるとやりづらいな
from vec2 import Vec2
from enemy import *
import state

class Waves:
    def __init__(self):
        self.wave = self.wAll()
        # self.wave = self.testwaveBoss()

    def update(self):
        next(self.wave)
    
    @staticmethod
    def rc2vec(row, col):
        return Vec2(row * 8 + 4, -col * 8 - 4)

# 90sec　キャラバンモード
    def wAll(self):
        yield from range(120)   #wait 2sec
        yield from self.w1() #直進1　たまなしｘ4
        yield from self.w2() #隊列　2x7 3*11
        yield from self.w3() #直進2　たまアリｘ１０
        yield from self.w4() #L 左
        yield from self.w5() #段
        yield from self.w6() #L　右
        yield from self.w7() #隊列　6x12 Ex2
        yield from self.w8() #直進　たまアリｘ５
        yield from self.w5() #段
        yield from self.w9() #直進ｘ１０　Ｅｘ５
        yield from self.wB() #ボス
        state.scene = state.GAME_BOSSDEAD
        #終了
        while True:
            yield
        # yield from range(9999) #wait
        # self.wave = self.wAll()
        # yield

    #直進1　たまなしｘ4
    def w1(self):
        EnemyD.create(0,0,0)
        EnemyD.create(4,1,0)
        EnemyD.create(5,2,0)
        EnemyD.create(2,3,0)
        yield from EnemyPool.isAlive()

    #隊列　2x7 3*11
    def w2(self):
        EnemyB.create(2, 2, 7)
        yield from range(120) #wait 2sec
        EnemyB.create(8, 3, 11)
        yield from EnemyPool.isAlive()

    #直進2　たまアリｘ１０
    def w3(self):
        EnemyD.create(2,0,0)
        EnemyD.create(4,1,0)
        EnemyD.create(1,1,1)
        EnemyD.create(3,2,0)
        EnemyD.create(0,4,0)
        EnemyD.create(2,4,1)
        EnemyD.create(4,4,0)
        EnemyD.create(1,5,1)
        EnemyD.create(3,5,0)
        EnemyD.create(5,5,1)
        yield from EnemyPool.isAlive()

    #L 左
    def w4(self):
        EnemyA.create(3)
        yield from EnemyPool.isAlive()
        yield from range(30) #wait 2sec

    #段
    def w5(self):
        EnemyC.create(2, 6, 4) #とりあえず２，６、４こてい
        yield from EnemyPool.isAlive()

    #L　右
    def w6(self):
        EnemyA.create(12)
        yield from EnemyPool.isAlive()
        yield from range(30) #wait 2sec

    #隊列　6x12 Ex2
    def w7(self):
        EnemyB.create(2, 6, 12)
        yield from range(80)
        EnemyE.create(2)
        yield from range(80)
        EnemyE.create(0)
        yield from EnemyPool.isAlive()

    #直進　たまアリｘ５
    def w8(self):
        EnemyD.create(2,0,1)
        EnemyD.create(4,1,1)
        EnemyD.create(1,2,1)
        EnemyD.create(3,3,1)
        EnemyD.create(0,4,1)
        yield from EnemyPool.isAlive()

    #直進ｘ１０　Ｅｘ５
    def w9(self):
        EnemyD.create(0,0,0)
        EnemyD.create(4,1,0)
        EnemyD.create(5,2,0)
        EnemyD.create(2,3,0)
        EnemyD.create(3,3,1)
        EnemyD.create(1,4,0)
        EnemyD.create(0,5,0)
        EnemyD.create(2,5,1)
        EnemyD.create(4,5,0)
        EnemyD.create(1,6,1)
        EnemyD.create(3,6,0)
        EnemyD.create(5,6,1)
        yield from range(110)
        EnemyE.create(0)
        yield from range(40)
        EnemyE.create(3)
        yield from range(140)
        EnemyE.create(1)
        yield from range(40)
        EnemyE.create(2)
        yield from range(120)
        EnemyE.create(1)
        yield from EnemyPool.isAlive()

    def wB(self):
        EnemyBoss1.create()
        yield from EnemyPool.isAlive()

#
# 検証
#

# waveA L字
    def testwaveA(self):
        for i in range(120): #wait 2sec
            yield
        self.waveA(3)
        for i in range(90): #wait 2sec
            yield
        self.waveA(12)
        for i in range(90): #wait 2sec
            yield
        self.waveA(3)
        while EnemyPool.length() > 0:
            yield
        self.wave = self.testwaveA()
        yield

# waveB 等速直進
    def testwaveB(self):
        for i in range(60): #wait 1sec
            yield
        self.waveB(2, 2, 7)
        for i in range(120): #wait 1sec
            yield
        self.waveB(8, 3, 11)
        while EnemyPool.length() > 0:
            yield
        self.wave = self.testwaveB()
        yield

    def testwaveB2(self):
        for i in range(60): #wait 1sec
            yield
        self.waveB(2, 6, 7)
        while EnemyPool.length() > 0:
            yield
        self.wave = self.testwaveB2()
        yield

# waveC 上から出てきて整列し、一段ずつ降りる
    def testwaveC(self):
        for i in range(60): #wait 1sec
            yield
        self.waveC(2, 6, 4) #とりあえず２，６、４こてい
        while EnemyPool.length() > 0:
            yield
        self.wave = self.testwaveC()
        yield

# waveD 直進加速
    def testwaveD(self):
        for i in range(60): #wait 1sec
            yield
        self.waveD(0,0,0)
        self.waveD(4,1,0)
        self.waveD(5,2,0)
        self.waveD(2,3,0)
        self.waveD(3,3,1)
        self.waveD(1,4,0)
        self.waveD(0,5,0)
        self.waveD(2,5,1)
        self.waveD(4,5,0)
        self.waveD(1,6,1)
        self.waveD(3,6,0)
        self.waveD(5,6,1)
        while EnemyPool.length() > 0:
            yield
        self.wave = self.testwaveD()
        yield

# waveE 端からちょろっと
    def testwaveE(self):
        yield from range(20)
        self.waveE(0)
        yield from range(20)
        self.waveE(1)
        yield from range(60)
        self.waveE(2)
        yield from range(20)
        self.waveE(3)
        yield from EnemyPool.isAlive()
        self.wave = self.testwaveE()
        yield

    def testwaveE2(self):
        self.waveD(0,0,0)
        self.waveD(4,1,0)
        self.waveD(5,2,0)
        self.waveD(2,3,0)
        self.waveD(3,3,1)
        self.waveD(1,4,0)
        self.waveD(0,5,0)
        self.waveD(2,5,1)
        self.waveD(4,5,0)
        self.waveD(1,6,1)
        self.waveD(3,6,0)
        self.waveD(5,6,1)
        yield from range(110)
        self.waveE(0)
        yield from range(40)
        self.waveE(3)
        yield from range(140)
        self.waveE(1)
        yield from range(40)
        self.waveE(2)
        yield from range(120)
        self.waveE(1)
        yield from EnemyPool.isAlive()
        self.wave = self.testwaveE2()
        yield

# waveBoss ボス
    def testwaveBoss(self):
        yield from range(20)
        self.waveBoss(0)
        yield from EnemyPool.isAlive()
        self.wave = self.testwaveBoss()
        yield
