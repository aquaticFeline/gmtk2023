from enum import Enum
import pygame, sys
import stateVars

buttons = []
visualComponents = []

class ViewScreen(Enum):
    Test = 0
    WorldMap = 1

def myQuit():
    pygame.quit()
    sys.exit()

def changeScreen(iViewScreen):
    #global viewScreen
    stateVars.viewScreen = iViewScreen

class Color:
    white = (255, 255, 255)
    gray = (100, 100, 100)
    black = (0, 0, 0)

class Font:
    large = None
    medium = None
    small = None
    def font(**kwargs):
        return pygame.font.Font(kwargs)

def initFonts():
    Font.large = pygame.font.Font(size = 60)
    Font.medium = pygame.font.Font(size = 28)
    Font.small = pygame.font.Font(size = 12)