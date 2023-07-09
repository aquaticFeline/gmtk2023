from dataclasses import dataclass
from standardClasses import *
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

@dataclass
class FireAnimation(Animation):
    actor: Image
    toX: float
    toY: float
    speed: float
    toX2: float
    toY2: float
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
                self.actor.x = self.toX2*completion + self.toX*(1-completion)
                self.actor.y = self.toY2*completion + self.toY*(1-completion)

#todo because this does not make images appear nor disappear 
@dataclass
class AppearAnimation(Animation):
    actor: Image
    xcoord: float
    ycoord: float
    width:float
    height: float
    speed: float
    onEnd: Callable[[], None]
    viewScreen: ViewScreen

    def __post_init__(self):
        super().__post_init__()
        self.isAnimating = False

    def start(self):
        self.startTime = time.time()
        self.isAnimating = True
        self.startX = self.actor.width
        self.startY = self.actor.height
        #self.image = Image(self.viewScreen, self.xcoord, self.ycoord, self.width, self.height, self.imageFile)
        self.actor.viewScreen = self.viewScreen
    
    def update(self):
        if self.isAnimating:
            completion = (time.time() - self.startTime)*self.speed
            if completion > 1.0:
                self.isAnimating = False
                self.actor.viewScreen = self.Test
                self.onEnd()


@dataclass
class FadingText(VisualComponent, Animation):
    x: float
    y: float
    text: str
    font: pygame.font.Font
    color: tuple
    icon: Icon
    speed: float

    def __post_init__(self):
        Animation.__post_init__(self)
        VisualComponent.__post_init__(self)
        self.isAnimating = False
        
    def start(self):
        self.isAnimating = True
        self.completion = 0
        self.startTime = time.time()
        
    def update(self):
        if self.isAnimating:
            self.completion = (time.time() - self.startTime)*self.speed
            if self.completion > 1.0:
                self.isAnimating = False

    def draw(self, surface):
        if self.isAnimating:
            myText = self.font.render(f"{self.text}", True, self.color)
            myTextRect = myText.get_rect()
            myTextRect = myTextRect.move(self.x, self.y-self.completion*100.0)
            myText.set_alpha(255*(1-self.completion))
            iconImg = pygame.transform.scale(stateVars.iconImages[self.icon], (self.font.get_linesize(), self.font.get_linesize()))
            myText.blit(iconImg, iconImg.get_rect())
            surface.blit(myText, myTextRect)






