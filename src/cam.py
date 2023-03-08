#cam
#なんかカメラ、たぶんシェイクぐらいしかすることない
import pyxel

class Cam:
    _task = None

    @classmethod
    def init(cls):
        cls._task = cls.taskNone()
    
    @classmethod
    def taskNone(cls):
        while True:
            yield
    
    @classmethod
    def taskShake(cls):
        for i in range(12):
            pyxel.camera(pyxel.rndi(-2,2), pyxel.rndi(-2,2))
            yield
            yield
        cls._task = cls.taskNone()
        pyxel.camera(0,0)
        yield

    @classmethod
    def taskPush(cls): #縦揺れ
        for y in [1,4,6,5,3,0]:
            pyxel.camera(0,-y)
            yield
        cls._task = cls.taskNone()
        yield

    @classmethod
    def shake(cls):
        cls._task = cls.taskShake()
    
    @classmethod
    def push(cls):
        cls._task = cls.taskPush()
    
    @classmethod
    def update(cls):
        next(cls._task)

