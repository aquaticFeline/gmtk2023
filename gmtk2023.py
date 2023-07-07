import pygame, sys, math, time, random
from dataclasses import dataclass
from collections.abc import Callable
from enum import Enum

class ViewScreen(Enum):
    Test = 0
    WorldMap = 1

def myQuit():
    pygame.quit()
    sys.exit()


viewScreen = ViewScreen.Test
def main():
    pygame.init()

    buttons = []
    visualComponents = []

    def changeScreen(iViewScreen):
        global viewScreen
        viewScreen = iViewScreen

    screen_size = screen_width, screen_height = (1000, 500)
    screen = pygame.display.set_mode(screen_size)
    screen_rect = pygame.rect.Rect(0, 0, screen_width, screen_height)

    font = pygame.font.Font(size = 60)
    white = (255, 255, 255)
    gray = (100, 100, 100)
    black = (0, 0, 0)
    
    randomNumber = random.randint(0, 10)

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

    @dataclass
    class VisualComponent:
        viewScreen: ViewScreen

        def __post_init__(self):
            visualComponents.append(self)

        def isValid(self):
            return self.viewScreen == viewScreen

        def draw(self, surface):
            pass

    @dataclass
    class DynamicText(VisualComponent):
        x: float
        y: float
        font: pygame.font.Font
        getText: Callable[[VisualComponent], str]

        def draw(self, surface):
            myText = self.font.render(f"{self.getText(self)}", True, white)
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
                pygame.draw.rect(surface, gray, rect)
            else:
                pygame.draw.rect(surface, white, rect)    
            ButtonText = self.font.render(f"{self.text}", True, black)
            surface.blit(ButtonText, rect)

        def checkAction(self):
            mouse = pygame.mouse.get_pos()
            if self.x < mouse[0] < self.x+self.width and self.y < mouse[1] < self.y+self.height:
                self.action()




    player = CombatActor(10, 50, 50)
    oponent = CombatActor(10, 50, 50)

    quitButton = Button(ViewScreen.Test, 100, 0, 100, 40, "Quit", font, myQuit)
    
    playerAttackButton = Button(ViewScreen.Test, 100, 50, 150, 40, "Player Attck", pygame.font.Font(size=30), lambda: player.attack(oponent))
    opponentAttackButton = Button(ViewScreen.Test, 100, 100, 150, 40, "Oponent Attack", pygame.font.Font(size=30), lambda: oponent.attack(player))

    worldMapButton = Button(ViewScreen.Test, 500, 0, 100, 50, "To World Map", pygame.font.Font(size=20), lambda: changeScreen(ViewScreen.WorldMap))

    randomNumberText = Text(ViewScreen.Test, 0, 0, font, None, f"{randomNumber}")
    playerHealthText = DynamicText(ViewScreen.Test, 0, 50, font, lambda self: f"{player.health}")
    oponentHealthText = DynamicText(ViewScreen.Test, 0, 100, font, lambda self: f"{oponent.health}")
    
    lastTime = time.time()

    viewSurfaces = {veiwScreen : pygame.Surface(screen_size) for veiwScreen in ViewScreen}

    while True:
        screen.fill(black)
        for surface in viewSurfaces.values():
            surface.fill(black)

        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                myQuit()
            if evt.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if(button.isValid()):
                        button.checkAction()

        if pygame.key.get_pressed()[pygame.K_SPACE] and lastTime - time.time() < -0.1:
            lastTime = time.time()
            randomNumber = random.randint(0, 10)
            randomNumberText.text = f"{randomNumber}"

            
        if pygame.key.get_pressed()[pygame.K_a] and lastTime - time.time() < -0.1:
            lastTime = time.time()
            player.attack(oponent)
        
        helloWorldText = font.render(f"{randomNumber}", True, white)
        helloWorldTextRect = helloWorldText.get_rect()
        screen.blit(helloWorldText, helloWorldTextRect)

        playerHelathText = font.render(f"{player.health}", True, white)
        playerHelathTextRect = playerHelathText.get_rect()
        playerHelathTextRect = playerHelathTextRect.move(0, 50)
        screen.blit(playerHelathText, playerHelathTextRect)

        oponentHelathText = font.render(f"{oponent.health}", True, white)
        oponentHelathTextRect = oponentHelathText.get_rect()
        oponentHelathTextRect = oponentHelathTextRect.move(0, 100)
        screen.blit(oponentHelathText, oponentHelathTextRect)

        for visualComponent in visualComponents:
            visualComponent.draw(viewSurfaces[visualComponent.viewScreen])

        screen.blit(viewSurfaces[viewScreen], screen_rect)

        pygame.display.flip()


if __name__ == "__main__":
    main()