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
            return _health

        @health.setter
        def health(self, val):
            self._health = val

        
    
    while True:
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            randomNumber = random.randint(0, 10)
        
        screen.fill(black)
        helloWorldText = font.render(f"{randomNumber}", True, white)
        helloWorldTextRect = helloWorldText.get_rect()
        screen.blit(helloWorldText, helloWorldTextRect)



        pygame.display.flip()


if __name__ == "__main__":
    main()