from dataclasses import dataclass
from collections.abc import Callable
#from gmtk2023 import *
from standardClasses import *
import pygame, time
import stateVars

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

def genMultilineText(text, viewScreen, x, y, font):
    out = []
    for i, line in enumerate(text.split('\n')):
        out.append(Text(viewScreen, x, y+font.get_linesize()*i, font, None, line))
    return out

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
        self.stars = [pygame.image.load("assets\\activeStar.png"), pygame.image.load("assets\\activeStar.png")]
        self.stars = [pygame.transform.scale(star, (25, 25)) for star in self.stars]

    def drawConfig(self):
        mouse = pygame.mouse.get_pos()
        backColor = Color.gray if self.x < mouse[0] < self.x+self.width and self.y < mouse[1] < self.y+self.height else Color.white
        textColor = Color.black
        star = self.stars[0] if self.x < mouse[0] < self.x+self.width and self.y < mouse[1] < self.y+self.height else self.stars[1]
        return backColor, textColor, star

    def draw(self, surface):
        backColor, textColor, star = self.drawConfig()

        rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, backColor, rect) 
        ButtonText = self.font.render(f"{self.text}", True, textColor)
        ButtonTextRect = ButtonText.get_rect()
        ButtonTextRect = ButtonTextRect.move((rect.width - ButtonTextRect.width)/2.0, (rect.height - ButtonTextRect.height)/2.0)
        ButtonTextRect = ButtonTextRect.move(self.x, self.y)
        surface.blit(ButtonText, ButtonTextRect)

    def checkAction(self):
        mouse = pygame.mouse.get_pos()
        if self.x < mouse[0] < self.x+self.width and self.y < mouse[1] < self.y+self.height:
            self.action()
            return True
        return False

@dataclass
class DisableButton(Button):
    isDisabled: Callable[[], bool]

    def __post_init__(self):
        super().__post_init__()
        self.stars.append(pygame.image.load("assets\\disableStar.png"))
        self.stars = [pygame.transform.scale(star, (25, 25)) for star in self.stars]

    def drawConfig(self):
        if self.isDisabled():
            backColor = Color.darkGrey
            textColor = Color.black
            star = None
            return backColor, textColor, star
        return super().drawConfig()

    def checkAction(self):
        return not self.isDisabled() and super().checkAction() 

@dataclass
class LevelButton(VisualComponent):
    x: float
    y: float
    level: Levels

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
            stateVars.selectLevel = self.level
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
class HollowRect(VisualComponent):
    x: float
    y: float
    width: float
    height: float
    weight: float

    def draw(self, surface):
        smallRect = pygame.rect.Rect(self.x+self.weight, self.y+self.weight, self.width-self.weight*2, self.height-self.weight*2)
        bigRect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, Color.white, bigRect)
        pygame.draw.rect(surface, Color.black, smallRect)

@dataclass
class Image(VisualComponent):
    x: float
    y: float
    width:float
    height: float
    imageFile: str

    def __post_init__(self):
        super().__post_init__()
        self.image = pygame.image.load(self.imageFile)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw(self, surface):
        imageRect = self.image.get_rect()
        imageRect = imageRect.move(self.x, self.y)
        surface.blit(self.image, imageRect)

levelImageFiles = {Levels.Cemetery : "assets\\cemetery_map.png", Levels.Woods : "assets\\forest_map.png", Levels.Meadows : "assets\\meadow_map.png"}

@dataclass
class BattleBkgrdImage(VisualComponent):
    x: float
    y: float
    width:float
    height: float

    def __post_init__(self):
        super().__post_init__()
        self.images = {}
        for ele in levelImageFiles:
            self.images[ele] = pygame.image.load(levelImageFiles[ele])
            self.images[ele] = pygame.transform.scale(self.images[ele], (self.width, self.height))

    def draw(self, surface):
        self.image = self.images[stateVars.selectLevel]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        imageRect = self.image.get_rect()
        imageRect = imageRect.move(self.x, self.y)
        surface.blit(self.image, imageRect)


