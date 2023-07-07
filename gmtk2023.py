import pygame, sys, math, time, random
from dataclasses import dataclass
from collections.abc import Callable
from standardClasses import *
from VisualComponents import *
import stateVars


@dataclass
class CombatActor:
    strength: float
    _health: float
    maxHealth: float

    @property 
    def health(self):
        return self._health

    @health.setter
    def health(self, val):
        self._health = val
        if val <= 0:
            self.die()

    def attack(self, target):
        target.health -= self.strength

    def die(self):
        print(self, " died")

def checkEvents(playerWorldMap):
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            myQuit()
        if evt.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if(button.isValid()):
                    if button.checkAction():
                        break
            for levelButton in levelButtons:
                if(levelButton.isValid()):
                    if levelButton.checkAction(playerWorldMap):
                        break

def main():
    pygame.init()
    initFonts()
    stateVars.viewScreen = ViewScreen.Test

    screen_size = screen_width, screen_height = (1000, 500)
    screen = pygame.display.set_mode(screen_size)
    screen_rect = pygame.rect.Rect(0, 0, screen_width, screen_height)

    
    randomNumber = random.randint(0, 10)

    player = CombatActor(10, 50, 50)
    oponent = CombatActor(10, 50, 50)

    quitButton = Button(ViewScreen.Test, 100, 0, 100, 40, "Quit", Font.large, myQuit)

    randomNumberText = Text(ViewScreen.Test, 0, 0, Font.large, None, f"{randomNumber}")
    playerHealthText = DynamicText(ViewScreen.Test, 0, 50, Font.large, lambda self: f"{player.health}")
    oponentHealthText = DynamicText(ViewScreen.Test, 0, 100, Font.large, lambda self: f"{oponent.health}")
    
    playerAttackButton = Button(ViewScreen.Test, 100, 50, 150, 40, "Player Attck", pygame.font.Font(size=30), lambda: player.attack(oponent))
    opponentAttackButton = Button(ViewScreen.Test, 100, 100, 150, 40, "Oponent Attack", pygame.font.Font(size=30), lambda: oponent.attack(player))

    worldMapButton = Button(ViewScreen.Test, 500, 0, 100, 50, "To World Map", pygame.font.Font(size=20), lambda: changeScreen(ViewScreen.WorldMap))
    returnTestButton = Button(ViewScreen.WorldMap, 500, 0, 100, 50, "Return To Screen", pygame.font.Font(size=20), lambda: changeScreen(ViewScreen.Test))

    level0 = LevelButton(ViewScreen.WorldMap, 50, 50)
    level1 = LevelButton(ViewScreen.WorldMap, 150, 100)
    levelLine = Line(ViewScreen.WorldMap, 50, 50, 150, 100)

    playerWorldMap = PlayerWorldMap(ViewScreen.WorldMap, 37.5, 0)
    
    lastTime = time.time()

    viewSurfaces = {veiwScreen : pygame.Surface(screen_size) for veiwScreen in ViewScreen}

    while True:
        screen.fill(Color.black)
        for surface in viewSurfaces.values():
            surface.fill(Color.black)

        checkEvents(playerWorldMap)

        if pygame.key.get_pressed()[pygame.K_SPACE] and lastTime - time.time() < -0.1:
            lastTime = time.time()
            randomNumber = random.randint(0, 10)
            randomNumberText.text = f"{randomNumber}"
            
        if pygame.key.get_pressed()[pygame.K_a] and lastTime - time.time() < -0.1:
            lastTime = time.time()
            player.attack(oponent)

        for visualComponent in visualComponents:
            visualComponent.draw(viewSurfaces[visualComponent.viewScreen])

        screen.blit(viewSurfaces[stateVars.viewScreen], screen_rect)

        pygame.display.flip()


if __name__ == "__main__":
    main()