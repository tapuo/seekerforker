#入力いろいろ　入力は泥臭くなるよね
#都度取得してるけど、フレームごとにポーリングする方がええかなあ
import pyxel
from vec2 import Vec2

#ベーマガの息吹を感じる方向入力
_axis_table = (0, 8, 2, 0, 4, 7, 1, 0, 6, 9, 3, 0, 0, 0, 0, 0)
def dpad() -> int:
    a = int(pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP))
    a += int(pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)) * 2
    a += int(pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)) * 4
    a += int(pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)) * 8
    return _axis_table[a]

#入力をベクトルで返す、正規化済み
MOVETABLE = {
    1:Vec2(-1,1).normalize(),   2:Vec2(0,1),  3:Vec2(1,1).normalize(),
    4:Vec2(-1,0), 0:Vec2(0,0),    6:Vec2(1,0),
    7:Vec2(-1,-1).normalize(),  8:Vec2(0,-1), 9:Vec2(1,-1).normalize()}

def dpadVec2():
    return MOVETABLE[dpad()]

#連射付きショット space,z,padA
def btnShot() -> bool:
    return pyxel.btnp(pyxel.KEY_SPACE, 1, 6) or \
           pyxel.btnp(pyxel.KEY_Z, 1, 6) or \
           pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A, 0, 6)

#悪魔の捨てゲーぼたん r
def btnReset() -> bool:
    return pyxel.btn(pyxel.KEY_R)

#ボム ｘ
def btnBomb() -> bool:
    return pyxel.btn(pyxel.KEY_X)

#押しっぱなし対策つきボタン。前回取得したあとにボタンを放す必要がある
def _startdown() -> bool:
    return pyxel.btn(pyxel.KEY_SPACE) or \
           pyxel.btn(pyxel.KEY_Z) or \
           pyxel.btn(pyxel.GAMEPAD1_BUTTON_A)

_start_gettable = False #ボタンが離されて取得可能ならTrue
def btnStart() -> bool:
    global _start_gettable
    if _startdown() and _start_gettable:
        _start_gettable = False
        return True
    if not _startdown() and not _start_gettable: #一度ボタンを離したかチェック
        _start_gettable = True
    return False
