# scene
import pyxel
from player import Player
from enemy import EnemyPool
from bullet import BulletPool
from blast import BlastPool
from shot import ShotPool
from waves import Waves
from gui import GuiGameover,GuiTitle,GuiGameclear
import state
import pad
from cam import Cam

# タイトル
class SceneTitle:
    def __init__(self) -> None: #正しい初期化がバグを防ぐ（今月の標語）
        EnemyPool.init()
        ShotPool.init()
        BulletPool.init()
        BlastPool.init()
        Cam.init()
        state.setup(state.GAME_TITLE)
        self.g = GuiTitle()

    def update(self):
        return SceneStage() if pad.btnStart() else self

    def draw(self):
        self.g.draw()

# ステージ
class SceneStage:
    def __init__(self) -> None:
        pyxel.play(3, 13)
        state.setup(state.GAME_STAGE)
        self.player = Player.create()
        self.wave = Waves()
        pyxel.playm(1, loop=True)

    def update(self):
        if pad.btnReset():
            pyxel.stop()
            return SceneTitle()
        # bomb
        if state.bombBegin:
            EnemyPool.bomb()
            BulletPool.bomb()
            state.bombBegin = False
        # 当たり判定 shot->enemy enemy->player bullet->player
        for shot in ShotPool.pool():
            for enemy in EnemyPool.pool(shot.cidx):
                if shot.hit(enemy):
                    break
        for enemy in EnemyPool.pool(self.player.cidx):
            if self.player.hit(enemy): # 自機や敵は一回当たったらそのフレームは
                break
        for bullet in BulletPool.pool():
            if self.player.hit(bullet):# もうチェックせんでええねん
                break
        # update
        self.wave.update()
        state.update()
        ShotPool.update()
        EnemyPool.update()
        BulletPool.update()
        BlastPool.update()
        Cam.update()
        # gameover
        return SceneGameover() if state.scene == state.GAME_CLEAR or \
             not self.player.update() or \
             state.isTimeover() else self
       
    def draw(self):
        ShotPool.draw()
        EnemyPool.draw()
        BulletPool.draw()
        BlastPool.draw()
        self.player.draw()

# ゲームオーバー
class SceneGameover:
    def __init__(self) -> None:
        self.g = GuiGameclear() if state.scene == state.GAME_CLEAR else GuiGameover()
        state.setup(state.GAME_OVER)
        pyxel.stop(0)
        pyxel.stop(1)
        pyxel.stop(2)

    def update(self):
        ShotPool.update()
        EnemyPool.update()
        BulletPool.update()
        BlastPool.update()
        Cam.update()
        return SceneTitle() if pad.btnStart() else self

    def draw(self):
        ShotPool.draw()
        EnemyPool.draw()
        BulletPool.draw()
        BlastPool.draw()
        self.g.draw()
