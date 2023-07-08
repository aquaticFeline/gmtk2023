from dataclasses import dataclass
from collections.abc import Callable
from gmtk2023 import *
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
class DisableButton(Button):
    isDisabled: Callable[[], bool]

    def draw(self, surface):
        if self.isDisabled():
            rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
            pygame.draw.rect(surface, Color.darkGrey, rect)    
            ButtonText = self.font.render(f"{self.text}", True, Color.black)
            surface.blit(ButtonText, rect)
            return
        super().draw(surface)

    def checkAction(self):
        return not self.isDisabled() and super().checkAction() 

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
        self.image = pygame.image.load(imageFile)
        self.image = pygame.transform.scale(self.image, (width, height))

    def draw(self, surface):
        imageRect = self.image.get_rect()
        imageRect = imageRect.move(self.x, self.y)
        surface.blit(self.image, imageRect)

@dataclass
class GachaAnimation(VisualComponent):
    getReward: Callable[[], Reward]
    player: Player
    completion: float = 0.0
    reward: Reward = None
    animationStartTime: float = 0
    animationPlaying: bool = False
    
    def __post_init__(self):
        super().__post_init__()
        self.leftImage = pygame.image.load("assets/leftscroll.png")
        self.leftImage = pygame.transform.scale(self.leftImage, (50, 200))
        self.rightImage = pygame.image.load("assets/rightscroll.png")
        self.rightImage = pygame.transform.scale(self.rightImage, (50, 200))
        self.center = 250
        self.top = 50
        self.animationScale = 150
        self.createRollButton()

    def roll(self):
        global buttons
        self.animationStartTime = time.time()
        self.animationPlaying = True
        self.player.money -= 5
        buttons.remove(self.rollButton)
        visualComponents.remove(self.rollButton)
        self.reward = self.getReward()

    def animationComplete(self):
        self.completion = 1
        self.animationPlaying = False
        self.createCollectButton()

    def collectReward(self):
        global buttons
        self.completion = 0
        self.createRollButton()
        buttons.remove(self.collectButton)
        visualComponents.remove(self.collectButton)
        self.reward.collect()

    def createRollButton(self):
        self.rollButton = DisableButton(self.viewScreen, self.center - 50, self.top+225, 100, 50, "Roll $5", Font.medium, self.roll, lambda: not self.player.canBuy(5))

    def createCollectButton(self):
        self.collectButton = Button(self.viewScreen, self.center - 50, self.top+125, 100, 50, "Collect", Font.medium, self.collectReward)
    
    def draw(self, surface):
        if self.animationPlaying:
            self.completion = (time.time() - self.animationStartTime)/3.0
            if self.completion > 1:
                self.animationComplete()


        leftRect = self.leftImage.get_rect()
        leftRect = leftRect.move(self.center-50-self.animationScale*self.completion, self.top)
        surface.blit(self.leftImage, leftRect)

        rightRect = self.rightImage.get_rect()
        rightRect = rightRect.move(self.center+self.animationScale*self.completion, self.top)
        surface.blit(self.rightImage, rightRect)

        centerRect = pygame.rect.Rect(self.center-self.animationScale*self.completion, self.top+12.5, 2*self.animationScale*self.completion+2, 175)
        #pygame.draw.rect(surface, (193, 190, 169), centerRect)

        if self.reward is not None:
            rewardSurface = pygame.Surface(centerRect.size)
            rewardSurface.fill((193, 190, 169))
            self.reward.draw(rewardSurface)
            surface.blit(rewardSurface, centerRect)

