import pygame, sys, math, time, random, copy
from dataclasses import dataclass, field
from collections.abc import Callable
from gacha import *
from VisualComponents import *
from combat import *
from standardClasses import *
import stateVars

player= None

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
    global player, oponent
    pygame.init()
    initFonts()
    stateVars.viewScreen = ViewScreen.Test
    stateVars.selectLevel = Levels.Cemetery

    screen_size = screen_width, screen_height = (1600, 900)
    screen = pygame.display.set_mode(screen_size)
    screen_rect = pygame.rect.Rect(0, 0, screen_width, screen_height)

    Image(ViewScreen.WorldMap, 0, 0, screen_width, screen_height, "assets\worldmap.png")
    BattleBkgrdImage(ViewScreen.Battle, 0, 0, screen_width, screen_height)
    
    randomNumber = random.randint(0, 10)

    player = Player(10, 10, 100, 100)
    stateVars.player = player
    spawnEnemy()

    player.attacks.insert(0, Attack(10.0, True, "Fire Ball", "Shoots a \nfire ball", 20.0))
    player.attacks.insert(0, Attack(10.0, False, "Punch", "punch 'em \nin the face"))

    quitButton = Button(ViewScreen.Test, 100, 0, 100, 40, "Quit", Font.large, myQuit)

    randomNumberText = Text(ViewScreen.Test, 0, 0, Font.large, None, f"{randomNumber}")
    playerHealthText = DynamicText(ViewScreen.Test, 0, 50, Font.large, lambda self: f"{player.health}")
    oponentHealthText = DynamicText(ViewScreen.Test, 0, 100, Font.large, lambda self: f"{stateVars.oponent.health}")
    
    playerAttackButton = Button(ViewScreen.Test, 100, 50, 150, 40, "Player Attack", pygame.font.Font(size=30), lambda: player.physicalAttack(oponent))
    opponentAttackButton = Button(ViewScreen.Test, 100, 100, 150, 40, "Opponent Attack", pygame.font.Font(size=30), lambda: oponent.physicalAttack(player))

    worldMapButton = Button(ViewScreen.Test, 500, 0, 100, 50, "To World Map", pygame.font.Font(size=20), lambda: changeScreen(ViewScreen.WorldMap))
    returnTestButton = Button(ViewScreen.WorldMap, 500, 0, 100, 50, "Return To Screen", pygame.font.Font(size=20), lambda: changeScreen(ViewScreen.Test))

    worldMapButton = Button(ViewScreen.Test, 500, 100, 100, 50, "To Battle", pygame.font.Font(size=20), lambda: changeScreen(ViewScreen.Battle))
    worldMapButton = Button(ViewScreen.WorldMap, 1400, 50, 100, 50, "To Battle", pygame.font.Font(size=20), lambda: changeScreen(ViewScreen.Battle))
    returnTestButton = Button(ViewScreen.Battle, 500, 100, 100, 50, "Return To Screen", pygame.font.Font(size=20), lambda: changeScreen(ViewScreen.Test))

    level0 = LevelButton(ViewScreen.WorldMap, 300, 300, Levels.Cemetery)
    level1 = LevelButton(ViewScreen.WorldMap, 700, 525, Levels.Woods)
    levelLine01 = Line(ViewScreen.WorldMap, 300, 300, 700, 525)
    level2 = LevelButton(ViewScreen.WorldMap, 1250, 800, Levels.Meadows)
    levelLine12 = Line(ViewScreen.WorldMap, 700, 525, 1250, 800)

    playerWorldMap = PlayerWorldMap(ViewScreen.WorldMap, 300-12.5, 300-50)

    worldMapButton = Button(ViewScreen.Test, 0, 300, 100, 50, "Play Gacha", pygame.font.Font(size=20), lambda: changeScreen(ViewScreen.GachaScreen))
    returnTestButton = Button(ViewScreen.GachaScreen, 0, 300, 100, 50, "Return To Screen", pygame.font.Font(size=20), lambda: changeScreen(ViewScreen.Test))

    levelNames = {Levels.Cemetery : "Cemetery", Levels.Woods : "Woods", Levels.Meadows : "Meadows"}
    DynamicText(ViewScreen.WorldMap, 1400, 0, Font.large, lambda x: levelNames[stateVars.selectLevel])

    player.genText((0, 0), oponent)
    #oponent.genText((400, 0))

    genGacha(player)

    viewSurfaces = {veiwScreen : pygame.Surface(screen_size) for veiwScreen in ViewScreen}

    while True:
        screen.fill(Color.black)
        for surface in viewSurfaces.values():
            surface.fill(Color.black)

        checkEvents(playerWorldMap)

        for visualComponent in visualComponents:
            visualComponent.draw(viewSurfaces[visualComponent.viewScreen])

        screen.blit(viewSurfaces[stateVars.viewScreen], screen_rect)

        pygame.display.flip()


if __name__ == "__main__":
    main()