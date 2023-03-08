import pyxel
import background
import gui
import scene
import res

class Main:
    def __init__(self):
        pyxel.init(120, 160, title="SEEKER FORKER Ver.0.2", fps=60)
        res.resourceSetup()
        self.scene = scene.SceneTitle()
        self.background = background.Background()
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
