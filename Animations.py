from dataclasses import dataclass
from combat import *
import time


animations = []

class Animation:
    def __post_init__(self):
        global animations
        animations.append(self)

    def update(self):
        pass

@dataclass
class MoveAnimation(Animation):
    actor: Image
    toX: float
    toY: float
    speed: float
    toX2: float
    toY2: float
    speed2: float
    onEnd: Callable[[], None]

    def __post_init__(self):
        super().__post_init__()
        self.isAnimating = False

    def start(self):
        self.startTime = time.time()
        self.isAnimating = True
        self.startX = self.actor.x
        self.startY = self.actor.y
    
    def update(self):
        if self.isAnimating:
            completion = (time.time() - self.startTime)*self.speed
            if completion > 1.0:
                completion = ((time.time() - self.startTime) - 1/self.speed)*self.speed2
                if completion > 1.0:
                    self.isAnimating = False
                    self.onEnd()
                self.actor.x = self.toX2*completion + self.toX*(1-completion)
                self.actor.y = self.toY2*completion + self.toY*(1-completion)
            else:
                self.actor.x = self.toX*completion + self.startX*(1-completion)
                self.actor.y = self.toY*completion + self.startY*(1-completion)

@dataclass
class ShrinkAnimation(Animation):
    actor: Image
    speed: float
    onEnd: Callable[[], None]

    def __post_init__(self):
        super().__post_init__()
        self.isAnimating = False

    def start(self):
        self.startTime = time.time()
        self.isAnimating = True
        self.startX = self.actor.width
        self.startY = self.actor.height
    
    def update(self):
        if self.isAnimating:
            completion = (time.time() - self.startTime)*self.speed
            if completion > 1.0:
                self.isAnimating = False
                self.onEnd()
            else:
                self.actor.width = self.startX*(1-completion)
                self.actor.height = self.startY*(1-completion)




