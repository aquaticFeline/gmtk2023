import pygame, sys, math, time, random, copy
from dataclasses import dataclass, field
from collections.abc import Callable
from gacha import *
from VisualComponents import *
from combat import *
from Animations import *
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
    initIcons()
    stateVars.viewScreen = ViewScreen.WorldMap
    stateVars.selectLevel = Levels.Cemetery

    screen_size = screen_width, screen_height = (1600, 900)
    screen = pygame.display.set_mode(screen_size)
    screen_rect = pygame.rect.Rect(0, 0, screen_width, screen_height)

    Image(ViewScreen.WorldMap, 0, 0, screen_width, screen_height, "assets\worldmap.png")
    BattleBkgrdImage(ViewScreen.Battle, 0, 0, screen_width, screen_height)
    
    randomNumber = random.randint(0, 10)

    playerImage = Image(ViewScreen.Battle, 400, 275, 225, 450, "assets\\protag.png")
    enemyImage = Image(ViewScreen.Battle, 1025, 275, 225, 450, "assets\\ranibowsprimkle.png")
    fireBallImage = Image(ViewScreen.Battle, 5000, 350, 250, 250, "assets\\fireball.png")
    waterBoltImage = Image(ViewScreen.Battle, 5000, 350, 250, 250, "assets\\waterbolt.png")
    enlightenmentImage = Image(ViewScreen.Battle, 5000, 350, 250, 250, "assets\\enlightenment.png")
    plantShroudImage = Image(ViewScreen.Battle, 5000, 350, 250, 250, "assets\\plantshroud.png")
    frostImage = Image(ViewScreen.Battle, 5000, 350, 250, 250, "assets\\frost.png")
    shadowfallImage = Image(ViewScreen.Battle, 5000, 350, 250, 250, "assets\\shadowfall.png")
    stateVars.enemyImage = enemyImage
    stateVars.playerImage = playerImage
    stateVars.fireBallImage = fireBallImage
    stateVars.waterBoltImage = waterBoltImage
    stateVars.enlightenmentImage = enlightenmentImage
    stateVars.plantShroudImage = plantShroudImage
    stateVars.frostImage = frostImage
    stateVars.shadowfallImage = shadowfallImage

    punchAttack = Attack(10.0, False, "Punch", "punch 'em \nin the face")
    punchAttackAnimation = MoveAnimation(stateVars.playerImage, 1025, 275, 0.4, 400, 275, 0.8, None)
    addAnimationToAttack(punchAttack, punchAttackAnimation)
        
    shredAttack =  Attack(10.0, False, "Shred", "Shreds the opponent with claws")
    shredAttackAnimation = MoveAnimation(stateVars.playerImage, 1025, 275, 0.4, 400, 275, 0.8, None)
    addAnimationToAttack(shredAttack, shredAttackAnimation)

    bonkAttack = Attack(15.0, False, "Bonk", "Staff bonk!")
    bonkAttackAnimation = MoveAnimation(stateVars.playerImage, 1025, 275, 0.4, 400, 275, 0.8, None)
    addAnimationToAttack(bonkAttack, bonkAttackAnimation)

    waterBoltAttack = Attack(10.0, True, "Water Bolt", "Shoots a bolt of water", 15.0)
    waterBoltAttackAnimation = FireAnimation(stateVars.waterBoltImage, 400, 450, 0.4, 2500, 450, None)
    addAnimationToAttack(waterBoltAttack, waterBoltAttackAnimation)
        
    plantShroudAttack = Attack(15.0, True, "Plant Shroud", "Circles the opponent in plants", 20.0)
    plantShroudAttackAnimation = AppearAnimation(stateVars.plantShroudImage, 1025, 450, 0.4, None)
    addAnimationToAttack(plantShroudAttack, plantShroudAttackAnimation)

    enlightenmentAttack = Attack(20.0, True, "Enlightenment", "Light rains down on opponent", 30.0)
    enlightenmentAttackAnimation = AppearAnimation(stateVars.enlightenmentImage, 1025, 450, 0.4, None)
    addAnimationToAttack(enlightenmentAttack, enlightenmentAttackAnimation)

    frostAttack = Attack(20.0, True, "Frost", "Chills opponent", 20.0)
    frostAttackAnimation = AppearAnimation(stateVars.frostImage, 1025, 450, 0.4, None)
    addAnimationToAttack(frostAttack, frostAttackAnimation)

    shadowfallAttack = Attack(25.0, True, "Shadowfall", "Opponent glimpses the shadow realm, briefly", 20.0)
    shadowfallAttackAnimation = AppearAnimation(stateVars.shadowfallImage, 1025, 450, 0.4, None)
    addAnimationToAttack(shadowfallAttack, shadowfallAttackAnimation)

    fireBallAttack = Attack(10.0, True, "Fire Ball", "Shoots a \nfire ball", 20.0)
    fireBallAttackAnimation = FireAnimation(stateVars.fireBallImage, 400, 450, 0.4, 2500, 450, None)
    addAnimationToAttack(fireBallAttack, fireBallAttackAnimation)

    stateVars.punchAttack = punchAttack
    stateVars.shredAttack = shredAttack
    stateVars.bonkAttack = bonkAttack
    stateVars.waterBoltAttack = waterBoltAttack
    stateVars.plantShroudAttack = plantShroudAttack
    stateVars.enlightenmentAttack = enlightenmentAttack
    stateVars.frostAttack = frostAttack
    stateVars.shadowfallAttack = shadowfallAttack
    stateVars.fireBallAttack = fireBallAttack

    player = Player(10, 10, 100, 100, money = 100, _mana = 20)
    stateVars.player = player
    spawnEnemy()

    punchAttack = Attack(10.0, False, "Punch", "punch 'em \nin the face")

    player.attacks.insert(0, Attack(0.0, False, "None", "None"))
    player.attacks.insert(0, fireBallAttack)
    player.attacks.insert(0, punchAttack)

    quitButton = Button(ViewScreen.Test, 100, 0, 100, 40, "Quit", Font.large, myQuit)

    randomNumberText = Text(ViewScreen.Test, 0, 0, Font.large, None, f"{randomNumber}")
    playerHealthText = DynamicText(ViewScreen.Test, 0, 50, Font.large, lambda self: f"{player.health}")
    oponentHealthText = DynamicText(ViewScreen.Test, 0, 100, Font.large, lambda self: f"{stateVars.oponent.health}")
    
    playerAttackButton = Button(ViewScreen.Test, 100, 50, 150, 40, "Player Attack", pygame.font.Font(size=30), lambda: player.physicalAttack(oponent))
    opponentAttackButton = Button(ViewScreen.Test, 100, 100, 150, 40, "Opponent Attack", pygame.font.Font(size=30), lambda: oponent.physicalAttack(player))

    worldMapButton = Button(ViewScreen.Test, 500, 0, 100, 50, "To World Map", pygame.font.Font(size=20), lambda: changeScreen(ViewScreen.WorldMap))
    worldMapButton = Button(ViewScreen.Battle, 1200, 850, 300, 50, "Run From Battle", pygame.font.Font(size=28), lambda: changeScreen(ViewScreen.WorldMap))
    #returnTestButton = Button(ViewScreen.WorldMap, 500, 0, 100, 50, "Return To Screen", pygame.font.Font(size=20), lambda: changeScreen(ViewScreen.Test))

    #Tutorial screen stuff
    Image(ViewScreen.Tutorial, 0, 0, screen_width, screen_height, "assets\\tutorialbg.png")
    returnTutorialButton = Button(ViewScreen.WorldMap, 0, 400, 100, 50, "Go to Tutorial", pygame.font.Font(size=20), lambda: changeScreen(ViewScreen.Tutorial))
    returnWorldMapButton = Button(ViewScreen.Tutorial, 0, 400, 100, 50, "Go to World Map", pygame.font.Font(size=20), lambda: changeScreen(ViewScreen.WorldMap)) 
    tutorialText = genMultilineText("plink plink", ViewScreen.Tutorial, 300, 100, pygame.font.Font(size=32))
    
    worldMapButton = Button(ViewScreen.Test, 500, 100, 100, 50, "To Battle", pygame.font.Font(size=20), lambda: changeScreen(ViewScreen.Battle))
    worldMapButton = Button(ViewScreen.WorldMap, 1400, 50, 150, 50, "To Battle", pygame.font.Font(size=32), lambda: changeScreen(ViewScreen.Battle))
    #returnTestButton = Button(ViewScreen.Battle, 500, 100, 100, 50, "Return To Screen", pygame.font.Font(size=20), lambda: changeScreen(ViewScreen.Test))

    level0 = LevelButton(ViewScreen.WorldMap, 300, 300, Levels.Cemetery)
    level1 = LevelButton(ViewScreen.WorldMap, 700, 525, Levels.Woods)
    levelLine01 = Line(ViewScreen.WorldMap, 300, 300, 700, 525)
    level2 = LevelButton(ViewScreen.WorldMap, 1250, 800, Levels.Meadows)
    levelLine12 = Line(ViewScreen.WorldMap, 700, 525, 1250, 800)

    playerWorldMap = PlayerWorldMap(ViewScreen.WorldMap, 300-75*0.5, 300-150)

    worldMapButton = Button(ViewScreen.Test, 0, 300, 100, 50, "Play Gacha", pygame.font.Font(size=20), lambda: changeScreen(ViewScreen.GachaScreen))
    returnTestButton = Button(ViewScreen.GachaScreen, 1300, 0, 250, 50, "Return To World Map", pygame.font.Font(size=32), lambda: changeScreen(ViewScreen.WorldMap))

    GoToGachaButton(ViewScreen.WorldMap, 1400, 650, 200, 400, "assets\\dabloon.png", lambda: changeScreen(ViewScreen.GachaScreen))

    levelNames = {Levels.Cemetery : "Cemetery", Levels.Woods : "Woods", Levels.Meadows : "Meadows"}
    DynamicText(ViewScreen.WorldMap, 1400, 0, Font.large, lambda x: levelNames[stateVars.selectLevel])
    
    punchAttackAnimation = MoveAnimation(playerImage, 1025, 275, 0.4, 400, 275, 0.8, None)
    addAnimationToAttack(punchAttack, punchAttackAnimation)

    stateVars.manaText = FadingText(ViewScreen.Battle, 50, 150, "    + mana", Font.large, (100, 150, 255), Icon.Mana, 0.5)
    stateVars.manaText2 = FadingText(ViewScreen.Battle, 1050, 250, "    + mana", Font.large, (100, 150, 255), Icon.Mana, 0.5)
    stateVars.damageText = FadingText(ViewScreen.Battle, 1050, 250, "    - health", Font.large, (255, 200, 50), Icon.Health, 0.5)
    stateVars.damageText2 = FadingText(ViewScreen.Battle, 400, 275, "    - health", Font.large, (255, 200, 50), Icon.Health, 0.5)
    stateVars.healthText = FadingText(ViewScreen.Battle, 50, 150, "     + health", Font.large, (255, 50, 50), Icon.Health, 0.5)
    stateVars.moneyText = FadingText(ViewScreen.Battle, 1050, 350, "    + dabloons", Font.large, (150, 150, 150), Icon.Coin, 0.5)
    #Button(ViewScreen.WorldMap, 0, 0, 250, 50, "Test", pygame.font.Font(size=32), lambda: testText.start())

    Button(ViewScreen.WorldMap, 0, 0, 150, 50, "Test Die", Font.medium, lambda: changeScreen(ViewScreen.DiedScreen))
    Button(ViewScreen.WorldMap, 0, 50, 150, 50, "Test Clear", Font.medium, lambda: changeScreen(ViewScreen.BattleClear))
    Button(ViewScreen.WorldMap, 0, 100, 150, 50, "Test Win", Font.medium, lambda: changeScreen(ViewScreen.Win))

    Text(ViewScreen.DiedScreen, 650, 200, Font.large, None, "You Died")

    regenPlayerText()
    #oponent.genText((400, 0))

    genGacha(player)

    viewSurfaces = {veiwScreen : pygame.Surface(screen_size) for veiwScreen in ViewScreen}

    while True:
        screen.fill(Color.black)
        for surface in viewSurfaces.values():
            surface.fill(Color.black)

        viewSurfaces[ViewScreen.GachaScreen].fill((173, 117, 66))

        checkEvents(playerWorldMap)

        for visualComponent in visualComponents:
            visualComponent.draw(viewSurfaces[visualComponent.viewScreen])

        for animation in animations:
            animation.update()

        screen.blit(viewSurfaces[stateVars.viewScreen], screen_rect)

        pygame.display.flip()


if __name__ == "__main__":
    main()