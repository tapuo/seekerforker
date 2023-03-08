#state
#スコア、タイマー、その他もろもろグローバルな変数詰め合わせ、便利
#TODO セーブ
import pyxel

#const
#scene遷移
GAME_TITLE:int = 0
GAME_STAGE:int = 1
GAME_BOSSDEAD:int = 2
# GAME_CLEARDEMO:int = 3
GAME_CLEAR:int = 4
GAME_OVER:int = 5

#global
#ui
score:int = 0
hiscore:int = 0
time:float = 90.0
_inittime:float = 0.0
scene:int = GAME_TITLE # 現在のシーン
damageCnt:int = 0 # player 
playerhp:int = 0
bosshp:int = 0
warpCnt:int = 0
bombBegin:bool = False # もっとどうにか

def scoreAdd(p):
    global score,hiscore
    score += p
    hiscore = max(hiscore, score)

def setup(_s:int): #
    global score,time,_inittime,damageCnt,playerhp,bosshp,scene
    scene = _s
    if _s == GAME_TITLE:
        score = 0
        time = 90.0
        damageCnt = 0
        playerhp = 0
        bosshp = 0
        _inittime = pyxel.frame_count

def playerStatus(p):
    global damageCnt,playerhp
    damageCnt = p.damageCnt
    playerhp = p.hp

def isTimeover() -> bool:
    return time <= 0

def update():
    global time,warpCnt
    warpCnt -= 1
    if scene >= GAME_BOSSDEAD: #クリアした時点でカウントストップ
        return
    time = max(0.0, 90.0 - (pyxel.frame_count - _inittime) / 60.0)
