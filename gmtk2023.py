import pygame, sys, math, time, random
from dataclasses import dataclass
from collections.abc import Callable

def myQuit():
    pygame.quit()
    sys.exit()

def main():
    pygame.init()

    buttons = []

    screen_size = screen_width, screen_height = (1000, 500)
    screen = pygame.display.set_mode(screen_size)

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
    class Button:
        x: float
        y: float
        width: float
        height: float
        text: str
        font: pygame.font.Font
        action: Callable[[], None]

        def __post_init__(self):
            buttons.append(self)

        def draw(self, surface):
            mouse = pygame.mouse.get_pos()
            rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
            if self.x < mouse[0] < self.x+self.width and self.y < mouse[1] < self.y+self.height:
                pygame.draw.rect(surface, gray, rect)
            else:
                pygame.draw.rect(surface, white, rect)    
            ButtonText = self.font.render(f"{self.text}", True, black)
            screen.blit(ButtonText, rect)

        def checkAction(self):
            mouse = pygame.mouse.get_pos()
            if self.x < mouse[0] < self.x+self.width and self.y < mouse[1] < self.y+self.height:
                self.action()




    player = CombatActor(10, 50, 50)
    oponent = CombatActor(10, 50, 50)

    quitButton = Button(100, 0, 100, 40, "Quit", font, myQuit)
    
    playerAttackButton = Button(100, 50, 150, 40, "Player Attck", pygame.font.Font(size=30), lambda: player.attack(oponent))
    opponentAttackButton = Button(100, 100, 150, 40, "Oponent Attack", pygame.font.Font(size=30), lambda: oponent.attack(player))
    
    lastTime = time.time()

    while True:
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                myQuit()
            if evt.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    button.checkAction()

        if pygame.key.get_pressed()[pygame.K_SPACE] and lastTime - time.time() < -0.1:
            lastTime = time.time()
            randomNumber = random.randint(0, 10)

            
        if pygame.key.get_pressed()[pygame.K_a] and lastTime - time.time() < -0.1:
            lastTime = time.time()
            player.attack(oponent)
        
        screen.fill(black)
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

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()