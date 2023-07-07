from dataclasses import dataclass
from collections.abc import Callable
from standardClasses import *
import pygame, time
import stateVars

@dataclass
class VisualComponent:
    viewScreen: ViewScreen

    def __post_init__(self):
        visualComponents.append(self)

    def isValid(self):
        global viewScreen
        return self.viewScreen == stateVars.viewScreen

    def draw(self, surface):
        pass

@dataclass
class DynamicText(VisualComponent):
    x: float
    y: float
    font: pygame.font.Font
    getText: Callable[[VisualComponent], str]

    def draw(self, surface):
        myText = self.font.render(f"{self.getText(self)}", True, Color.white)
        myTextRect = myText.get_rect()
        myTextRect = myTextRect.move(self.x, self.y)
        surface.blit(myText, myTextRect)

@dataclass
class Text(DynamicText):
    text: str

    def __post_init__(self):
        super().__post_init__()
        self.getText = lambda x: self.text

@dataclass
class Button(VisualComponent):
    x: float
    y: float
    width: float
    height: float
    text: str
    font: pygame.font.Font
    action: Callable[[], None]

    def __post_init__(self):
        super().__post_init__()
        buttons.append(self)

    def draw(self, surface):
        mouse = pygame.mouse.get_pos()
        rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        if self.x < mouse[0] < self.x+self.width and self.y < mouse[1] < self.y+self.height:
            pygame.draw.rect(surface, Color.gray, rect)
        else:
            pygame.draw.rect(surface, Color.white, rect)    
        ButtonText = self.font.render(f"{self.text}", True, Color.black)
        surface.blit(ButtonText, rect)

    def checkAction(self):
        mouse = pygame.mouse.get_pos()
        if self.x < mouse[0] < self.x+self.width and self.y < mouse[1] < self.y+self.height:
            self.action()
            return True
        return False

@dataclass
class LevelButton(VisualComponent):
    x: float
    y: float

    def __post_init__(self):
        super().__post_init__()
        levelButtons.append(self)
        self.radius = 15

    def draw(self, surface):
        mouse = pygame.mouse.get_pos()
        if self.x-self.radius < mouse[0] < self.x+self.radius and self.y-self.radius < mouse[1] < self.y+self.radius:
            pygame.draw.circle(surface, Color.white, (self.x, self.y), self.radius+5)
            pygame.draw.circle(surface, Color.black, (self.x, self.y), self.radius+2.5)
        pygame.draw.circle(surface, Color.white, (self.x, self.y), self.radius)

    def checkAction(self, playerWorldMap):
        mouse = pygame.mouse.get_pos()
        if self.x-self.radius < mouse[0] < self.x+self.radius and self.y-self.radius < mouse[1] < self.y+self.radius:
            playerWorldMap.x = self.x - 12.5
            playerWorldMap.y = self.y - 50
            return True
        return False

@dataclass
class Line(VisualComponent):
    startX: float
    startY: float
    endX: float
    endY: float

    def draw(self, surface):
        pygame.draw.line(surface, Color.white, (self.startX, self.startY), (self.endX, self.endY))

@dataclass
class PlayerWorldMap(VisualComponent):
    x: float
    y: float

    def __post_init__(self):
        super().__post_init__()
        self.image = pygame.image.load("assets/stick man.png")
        self.image = pygame.transform.scale(self.image, (25, 50))

    def draw(self, surface):
        rect = self.image.get_rect()
        rect = rect.move(self.x, self.y)
        surface.blit(self.image, rect)

@dataclass
class GachaAnimation(VisualComponent):
    completion: float = 0.0
    reward: int = 0
    animationStartTime: float = 0
    animationPlaying: bool = False
    
    def __post_init__(self):
        super().__post_init__()
        self.leftImage = pygame.image.load("assets/whiteBox.png")
        self.leftImage = pygame.transform.scale(self.leftImage, (50, 200))
        self.rightImage = pygame.image.load("assets/whiteBox.png")
        self.rightImage = pygame.transform.scale(self.rightImage, (50, 200))
        self.center = 250
        self.top = 50
        self.animationScale = 150

    def draw(self, surface):
        if self.animationPlaying:
            self.completion = (time.time() - self.animationStartTime)/3.0
            if self.completion > 1:
                self.completion = 1
                self.animationPlaying = False

        leftRect = self.leftImage.get_rect()
        leftRect = leftRect.move(self.center-50-self.animationScale*self.completion, self.top)
        surface.blit(self.leftImage, leftRect)

        rightRect = self.rightImage.get_rect()
        rightRect = rightRect.move(self.center+self.animationScale*self.completion, self.top)
        surface.blit(self.rightImage, rightRect)

        centerRect = pygame.rect.Rect(self.center-self.animationScale*self.completion, self.top+25, 2*self.animationScale*self.completion, 150)
        pygame.draw.rect(surface, Color.white, centerRect)  

