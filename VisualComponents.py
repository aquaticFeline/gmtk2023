from dataclasses import dataclass
from collections.abc import Callable
from standardClasses import *
import pygame
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