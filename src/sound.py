import pyxel

#SE 優先度に応じて再生する、チャンネルは3固定
currentPriority = 0

def se(s, p):
    global currentPriority #無音かプライオリティが同一なら鳴らせる
    ch3 = pyxel.play_pos(3) #サウンド番号がつねに0を返す気がする
    if ch3 != None and currentPriority > p:
        return
    pyxel.play(3, s)
    currentPriority = p
