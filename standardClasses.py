from enum import Enum
import pygame, sys
import stateVars
from dataclasses import dataclass

visualComponents = []
buttons = []
levelButtons = []

class ViewScreen(Enum):
    Test = 0
    WorldMap = 1
    GachaScreen = 2
    Battle = 3
    DiedScreen = 4
    BattleClear = 5
    YouWin = 6

def myQuit():
    pygame.quit()
    sys.exit()

def changeScreen(iViewScreen):
    #global viewScreen
    stateVars.viewScreen = iViewScreen

class Color:
    white = (255, 255, 255)
    gray = (100, 100, 100)
    darkGrey = (50, 50, 50)
    black = (0, 0, 0)

class Font:
    large = None
    medium = None
    small = None
    def font(**kwargs):
        return pygame.font.Font(kwargs)

class Levels(Enum):
    Cemetery = 0
    Woods = 1
    Meadows = 2

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

class Icon(Enum):
    Health = 0
    Mana = 1
    PhysicalStrength = 2
    MagicalStrength = 3
    HealPotion = 4
    ManaPotion = 5
    Coin = 6

def initFonts():
    Font.large = pygame.font.Font(size = 60)
    Font.medium = pygame.font.Font(size = 32)
    Font.small = pygame.font.Font(size = 18)
    #pygame.font.Font(size = 28).


def initIcons():
    #global iconImages, iconImageFiles
    stateVars.iconImageFiles = {
        Icon.Health : "assets\\health.png", 
        Icon.Mana : "assets\\mana.png", 
        Icon.PhysicalStrength : "assets\\physicalstrength.png", 
        Icon.MagicalStrength : "assets\\magical_strength.png", 
        Icon.HealPotion : "assets\\healthpotion.png", 
        Icon.ManaPotion : "assets\\manapotion.png", 
        Icon.Coin : "assets\\coin.png", 
    }
    for icon in stateVars.iconImageFiles:
        stateVars.iconImages[icon] = pygame.image.load(stateVars.iconImageFiles[icon])
