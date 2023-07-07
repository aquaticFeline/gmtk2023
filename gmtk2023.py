import pygame, sys, math, time, random
from dataclasses import dataclass

def main():
    pygame.init()

    screen_size = screen_width, screen_height = (1000, 500)
    screen = pygame.display.set_mode(screen_size)

    font = pygame.font.Font(size = 60)
    white = (255, 255, 255)
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

    player = CombatActor(10, 50, 50)
    oponent = CombatActor(10, 50, 50)
    
    lastTime = time.time()

    while True:
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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

        pygame.display.flip()


if __name__ == "__main__":
    main()