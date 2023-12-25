#リソース
#自動で切り出す仕組み作らんとやっとれんぞこれ
import pyxel
from vec2 import Rect

#パレット　オリジナル
# pal_0 = pyxel.colors.to_list()
#パレット　ＭＳＸ１風
pal_1 = [0x000000, #0
         0x010101, #1
         0x3eb849, #2
         0x74d07d, #3
         0x5955e0, #4
         0x8076f1, #5
         0xb95e51, #6
         0x65dbef, #7
         0xdb6559, #8
         0xff897d, #9
         0xccc35e, #a
         0xded087, #b
         0x3aa241, #c
         0xb766b5, #D
         0xcccccc, #e
         0xffffff, #f
        ]
#パレット　ＭＳＸ１風をオリジナルに寄せて並べ替えた物
pal_2 = [0x000000, #0
         0x2b335f, #1
         0xb766b5, #D
         0x3aa241, #c

         0xdb6559, #8
         0x8076f1, #5
         0x74d07d, #3
         0xffffff, #f

         0xff897d, #9
         0xb95e51, #6
         0xded087, #b
         0x3eb849, #2

         0x65dbef, #7
         0xcccccc, #e
         0x5955e0, #4
         0xccc35e, #a
        ]

#バンクの領域に名前。
#posを中央にするとサイズを２の倍数にする必要がある　どうしたもんか
_spriteData = {#ちゃんとトリミングしておきたい
    'player':  [  0,  8, 16,  8],
    'shotB':   [  0, 16,  8,  8],
    'blastA1': [  0, 64, 16, 16], 
    'blastA2': [ 16, 64, 16, 16], 
    'blastA3': [ 32, 64, 16, 16], 
    'blastA4': [ 48, 64, 16, 16], 
    'enemyA1': [  0, 48, 12,  8], #2-1
    'enemyA2': [ 16, 32, 16, 16], #1-2
    'enemyA3': [ 32, 32, 16, 24], #1-3
    'enemyA5': [  0, 32, 16, 16], #1-1
    'enemyA6': [ 16, 48, 16, 16], #2-2
    'enemyB1': [  0, 80, 16, 16], #1-1
    'enemyC1': [  0, 96,  8,  8], #1-1
    'enemyC2': [  8, 96,  8,  8], #1-1
    'enemyC3': [ 16, 96,  8,  8], #1-1
    'enemyC4': [ 24, 96,  8,  8], #1-1
    'blastB1': [  0,104,  8,  8], #1-1
    'blastB2': [  8,104,  8,  8], #1-1
    'blastB3': [ 16,104,  8,  8], #1-1
    'bulletA1':[  0, 24,  8,  8],    
    'bulletA2':[  8, 24,  8,  8],
    'bulletB1':[  0,128, 16, 16], 
    'bulletB2':[ 16,128, 16, 16], 
    'bulletB3':[ 32,128, 16, 16], 
    'bulletB4':[ 48,128, 16, 16], 
    }

def spriteData(key):
    x, y, w, h = _spriteData[key]
    return Rect(x, y, w, h)

#当たり判定の範囲　スプライト中心基準、半分のサイズ、オフセットは要検討
_spriteCollider = {
    'player':[2, 2],
    'shotB':[3, 3],
    'enemyA1':[6, 4],
    'enemyA2':[8, 8],
    'enemyA3':[8, 12],
    'enemyA5':[8, 8],
    'enemyA6':[8, 8],
    'enemyB1':[8, 8],
    'enemyC1':[4, 4],
    'bulletA1':[1, 1],
    'bulletA2':[2, 2],
    'bulletB':[6, 6],
    }

def spriteCollider(key):
    w, h = _spriteCollider.get(key, (0,0)) #当たり判定が不要な場合はとりあえず(0,0)
    return Rect(-w, -h, w * 2, h * 2)

#アニメテーブル
_animeData = {
    'blastA':['blastA1','blastA2','blastA3','blastA4'], #デフォ
    'blastB':['blastB1','blastB2','blastB3'], #ボス弾
    'enemyC':['enemyC1','enemyC2','enemyC3','enemyC4'],
    'bulletB':['bulletB1','bulletB2','bulletB3','bulletB4'],
}

def animeData(key):
    return _animeData[key]

#あれこれ読み込み
def resourceSetup():
    pyxel.load("assets/my_resource.pyxres", False, False)
    pyxel.images[0].load(0,0,"assets/img.png")
    # pyxel.image(0).load(0,0,"assets/img_msx.png")
