import pyxel
from background import Background
import gui
from scene import SceneTitle
import res

class Main:
    def __init__(self):
        pyxel.init(120, 160, title="SEEKER FORKER Ver.0.2", fps=60)
        # pyxel.init(256, 192, title="SEEKER FORKER Ver.0.2", fps=60)
        # pyxel.colors.from_list(res.pal_1)
        res.resourceSetup()
        self.scene = SceneTitle()
        self.background = Background()
        # pyxel.font.load(0,0,"assets/font_msx.png") #フォント差し替え
        pyxel.font.load(0,0,"assets/font.png") #フォント差し替え
        pyxel.run(self.update, self.draw)

    def update(self):
        self.background.update()
        self.scene = self.scene.update()

    def draw(self):
        self.background.draw()
        self.scene.draw()
        gui.draw()

Main()