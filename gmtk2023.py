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
    stateVars.viewScreen = ViewScreen.CharacterCustomization
    stateVars.selectLevel = Levels.Cemetery
    pygame.display.set_caption("Furry Quest")

    screen_size = screen_width, screen_height = (1600, 900)
    screen = pygame.display.set_mode(screen_size)
    screen_rect = pygame.rect.Rect(0, 0, screen_width, screen_height)

    Image(ViewScreen.WorldMap, 0, 0, screen_width, screen_height, "assets\\worldmap.png")
    BattleBkgrdImage(ViewScreen.Battle, 0, 0, screen_width, screen_height)
    
    randomNumber = random.randint(0, 10)

    stateVars.commonImage = pygame.image.load("assets\\Common.png")
    stateVars.uncommonImage = pygame.image.load("assets\\Uncommon.png")
    stateVars.rareImage = pygame.image.load("assets\\Rare.png")
    stateVars.legendaryImage = pygame.image.load("assets\\Legendary.png")

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

    stateVars.enemyAnimation = MoveAnimation(enemyImage, 400, 275, 0.6, 1025, 275, 1.2, finishEnemyAnimate)

    punchAttack = Attack(10.0, False, "Punch", "punch 'em in the face")
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
    plantShroudAttackAnimation = AppearAnimation(stateVars.plantShroudImage, 1025, 450, 0.4, 0, 0.8, None, ViewScreen.Battle)
    addAnimationToAttack(plantShroudAttack, plantShroudAttackAnimation)

    #shortened to enlighten when displayed
    enlightenmentAttack = Attack(20.0, True, "Enlighten", "Light rains down on opponent", 30.0)
    enlightenmentAttackAnimation = AppearAnimation(stateVars.enlightenmentImage, 1025, 450, 0.4, 0, 0.8, None, ViewScreen.Battle)
    addAnimationToAttack(enlightenmentAttack, enlightenmentAttackAnimation)

    frostAttack = Attack(20.0, True, "Frost", "Chills opponent", 20.0)
    frostAttackAnimation = AppearAnimation(stateVars.frostImage, 1025, 450, 0.4, 0, 0.8, None, ViewScreen.Battle)
    addAnimationToAttack(frostAttack, frostAttackAnimation)

    shadowfallAttack = Attack(25.0, True, "Shadowfall", "Opponent glimpses the shadow realm, briefly", 20.0)
    shadowfallAttackAnimation = AppearAnimation(stateVars.shadowfallImage, 1025, 450, 0.4, 0, 0.8, None, ViewScreen.Battle) 
    addAnimationToAttack(shadowfallAttack, shadowfallAttackAnimation)

    fireBallAttack = Attack(10.0, True, "Fire Ball", "Shoots a fire ball", 20.0)
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

    player = Player(10, 10, 100, 100, money = 10, _mana = 0)
    stateVars.player = player
    spawnEnemy()

    punchAttack = Attack(10.0, False, "Punch", "punch 'em in the face")

    player.attacks.insert(0, Attack(0.0, False, "None", "None"))
    player.attacks.insert(0, Attack(0.0, False, "None", "None"))
    player.attacks.insert(0, punchAttack)

    quitButton = Button(ViewScreen.Test, 100, 0, 100, 40, "Quit", Font.large, myQuit)

    randomNumberText = Text(ViewScreen.Test, 0, 0, Font.large, None, f"{randomNumber}")
    playerHealthText = DynamicText(ViewScreen.Test, 0, 50, Font.large, lambda self: f"{player.health}")
    oponentHealthText = DynamicText(ViewScreen.Test, 0, 100, Font.large, lambda self: f"{stateVars.oponent.health}")
    
    playerAttackButton = Button(ViewScreen.Test, 100, 50, 150, 40, "Player Attack", pygame.font.Font(size=30), lambda: player.physicalAttack(oponent))
    opponentAttackButton = Button(ViewScreen.Test, 100, 100, 150, 40, "Opponent Attack", pygame.font.Font(size=30), lambda: oponent.physicalAttack(player))

    worldMapButton = Button(ViewScreen.Test, 500, 0, 100, 50, "To World Map", pygame.font.Font(size=20), lambda: changeScreen(ViewScreen.WorldMap))

    initBattleButtons()
    #returnTestButton = Button(ViewScreen.WorldMap, 500, 0, 100, 50, "Return To Screen", pygame.font.Font(size=20), lambda: changeScreen(ViewScreen.Test))

    #Tutorial screen stuff
    Image(ViewScreen.Tutorial, 0, 0, screen_width, screen_height, "assets\\tutorialbg.png")
    #returnTutorialButton = Button(ViewScreen.WorldMap, 0, 400, 100, 50, "Go to Tutorial", pygame.font.Font(size=20), lambda: changeScreen(ViewScreen.Tutorial))
    returnWorldMapButton = Button(ViewScreen.Tutorial, 700, 650, 250, 50, "Go to World Map", pygame.font.Font(size=35), lambda: changeScreen(ViewScreen.WorldMap)) 
    tutorialText1 = Text(ViewScreen.Tutorial, 300, 100, Font.medium, None, "Uh oh! Your beloved bunny breached dimensions, and was sent to this world! Since this ")
    tutorialText1.color = (0,0,0)
    tutorialText2 = Text(ViewScreen.Tutorial, 300, 125, Font.medium, None, "strange occurrence, the Evil Wizard Court (an established society) has been more active, ")
    tutorialText2.color = (0,0,0)
    tutorialText3 = Text(ViewScreen.Tutorial, 300, 150, Font.medium, None, "and has been casting terrible spells! You, a groundhog from this world, embark on a journey ")
    tutorialText3.color = (0,0,0)
    tutorialText4 = Text(ViewScreen.Tutorial, 300, 175, Font.medium, None, "through the cemetery, woods, and meadow to reach the Court. Before taking on enemies, ")
    tutorialText4.color = (0,0,0)  
    tutorialText5 = Text(ViewScreen.Tutorial, 300, 200, Font.medium, None, "you can gain buffs through the gacha, where it seems your odds in this universe have ")
    tutorialText5.color = (0,0,0)
    tutorialText6 = Text(ViewScreen.Tutorial, 300, 225, Font.medium, None, "turned for the better. Some things you may expect to be rare may easily fall into your hands.")
    tutorialText6.color = (0,0,0) 
    tutorialText7 = Text(ViewScreen.Tutorial, 300, 250, Font.medium, None, "Good luck on your travels!  You may also want to practice honing your skills in earlier levels.")
    tutorialText7.color = (0,0,0)
    tutorialText8 = Text(ViewScreen.Tutorial, 300, 275, Font.medium, None, "Be careful not to die! You will lose half your dabloons if you do!!!")
    tutorialText8.color = (0,0,0)
    
    BattleCompletionText = DynamicText(ViewScreen.Battle, 1200, 775, Font.medium, lambda x: f"Enemies Defeated: {stateVars.enemiesDefeated[stateVars.selectLevel.value]}/3")

    def beginBattle():
        player.mana = 0
        stateVars.oponent.delete()
        spawnEnemy()
        changeScreen(ViewScreen.Battle)


    worldMapButton = Button(ViewScreen.Test, 500, 100, 100, 50, "To Battle", pygame.font.Font(size=20), lambda: changeScreen(ViewScreen.Battle))
    worldMapButton = Button(ViewScreen.WorldMap, 1425, 65, 150, 50, "To Battle", pygame.font.Font(size=32), beginBattle)
    #returnTestButton = Button(ViewScreen.Battle, 500, 100, 100, 50, "Return To Screen", pygame.font.Font(size=20), lambda: changeScreen(ViewScreen.Test))

    level0 = LevelButton(ViewScreen.WorldMap, 300, 300, Levels.Cemetery)
    level1 = LevelButton(ViewScreen.WorldMap, 700, 525, Levels.Woods)
    levelLine01 = Line(ViewScreen.WorldMap, 300, 300, 700, 525)
    level2 = LevelButton(ViewScreen.WorldMap, 1150, 700, Levels.Meadows)
    levelLine12 = Line(ViewScreen.WorldMap, 700, 525, 1150, 700)
    boss = LevelButton(ViewScreen.WorldMap, 1300, 800, Levels.Boss)
    levelLine2b = Line(ViewScreen.WorldMap, 1150, 700, 1300, 800)

    playerWorldMap = PlayerWorldMap(ViewScreen.WorldMap, 300-75*0.5, 300-150)

    worldMapButton = Button(ViewScreen.Test, 0, 300, 100, 50, "Play Gacha", pygame.font.Font(size=20), lambda: changeScreen(ViewScreen.GachaScreen))

    GoToGachaButton(ViewScreen.WorldMap, 1400, 650, 200, 400, "assets\\dabloon.png", lambda: changeScreen(ViewScreen.GachaScreen))

    levelNames = {Levels.Cemetery : "Cemetery", Levels.Woods : "Woods", Levels.Meadows : "Meadows", Levels.Boss: "Bunny's Lair"}
    DynamicText(ViewScreen.WorldMap, 1300, 15, Font.large, lambda x: levelNames[stateVars.selectLevel])
    
    punchAttackAnimation = MoveAnimation(playerImage, 1025, 275, 0.4, 400, 275, 0.8, None)
    addAnimationToAttack(punchAttack, punchAttackAnimation)

    stateVars.manaText = FadingText(ViewScreen.Battle, 50, 150, "    + mana", Font.large, (100, 150, 255), Icon.Mana, 0.5)
    stateVars.manaText2 = FadingText(ViewScreen.Battle, 1050, 250, "    + mana", Font.large, (100, 150, 255), Icon.Mana, 0.5)
    stateVars.damageText = FadingText(ViewScreen.Battle, 1050, 250, "    - health", Font.large, (255, 200, 50), Icon.Health, 0.5)
    stateVars.damageText2 = FadingText(ViewScreen.Battle, 400, 275, "    - health", Font.large, (255, 200, 50), Icon.Health, 0.5)
    stateVars.healthText = FadingText(ViewScreen.Battle, 50, 150, "     + health", Font.large, (255, 50, 50), Icon.Health, 0.5)
    stateVars.moneyText = FadingText(ViewScreen.Battle, 1050, 350, "    + dabloons", Font.large, (150, 150, 150), Icon.Coin, 0.5)
    #Button(ViewScreen.WorldMap, 0, 0, 250, 50, "Test", pygame.font.Font(size=32), lambda: testText.start())

    # Button(ViewScreen.WorldMap, 0, 0, 150, 50, "Test Die", Font.medium, lambda: changeScreen(ViewScreen.DiedScreen))
    # Button(ViewScreen.WorldMap, 0, 50, 150, 50, "Test Clear", Font.medium, lambda: changeScreen(ViewScreen.BattleClear))
    # Button(ViewScreen.WorldMap, 0, 100, 150, 50, "Test Win", Font.medium, lambda: changeScreen(ViewScreen.YouWin))

    Text(ViewScreen.DiedScreen, 650, 200, Font.large, None, "You Died")
    Text(ViewScreen.BattleClear, 650, 200, Font.large, None, "Battle Cleared")
    Text(ViewScreen.YouWin, 650, 200, Font.large, None, "You Win")

    Button(ViewScreen.DiedScreen, 575, 400, 350, 50, "Continue to World Map", Font.medium, lambda: changeScreen(ViewScreen.WorldMap))
    Button(ViewScreen.BattleClear, 600, 400, 350, 50, "Continue to World Map", Font.medium, lambda: changeScreen(ViewScreen.WorldMap))
    Button(ViewScreen.YouWin, 550, 400, 350, 50, "Continue to World Map", Font.medium, lambda: changeScreen(ViewScreen.WorldMap))

    DynamicText(ViewScreen.CharacterCustomization, 600, 100, Font.large, lambda x: f"Health: {BossStats.health}")
    DynamicText(ViewScreen.CharacterCustomization, 600, 150, Font.large, lambda x: f"Damage: {BossStats.damage}")
    DynamicText(ViewScreen.CharacterCustomization, 600, 200, Font.large, lambda x: f"Width: {BossStats.width}")
    DynamicText(ViewScreen.CharacterCustomization, 600, 250, Font.large, lambda x: f"Height: {BossStats.height}")
    DynamicText(ViewScreen.CharacterCustomization, 600, 300, Font.large, lambda x: f"Upgrade Points: {BossStats.upgradePoints}")

    def decreaseHealth():
        BossStats.health -= 50
        BossStats.upgradePoints += 1
    def increaseHealth():
        BossStats.health += 50
        BossStats.upgradePoints -= 1
    def decreaseDamage():
        BossStats.damage -= 5
        BossStats.upgradePoints += 1
    def increaseDamage():
        BossStats.damage += 5
        BossStats.upgradePoints -= 1
    def decreaseWidth():
        BossStats.width -= 25
    def increaseWidth():
        BossStats.width += 25
    def decreaseHeight():
        BossStats.height -= 25
    def increaseHeight():
        BossStats.height += 25


    DisableButton(ViewScreen.CharacterCustomization, 450, 100, 135, 40, "Decrease", Font.medium, decreaseHealth, lambda: BossStats.health <= 100)
    DisableButton(ViewScreen.CharacterCustomization, 1000, 100, 135, 40, "Increase", Font.medium, increaseHealth, lambda: BossStats.upgradePoints <= 0)
    DisableButton(ViewScreen.CharacterCustomization, 450, 150, 135, 40, "Decrease", Font.medium, decreaseDamage, lambda: BossStats.damage <= 10)
    DisableButton(ViewScreen.CharacterCustomization, 1000, 150, 135, 40, "Increase", Font.medium, increaseDamage, lambda: BossStats.upgradePoints <= 0)
    DisableButton(ViewScreen.CharacterCustomization, 450, 200, 135, 40, "Decrease", Font.medium, decreaseWidth, lambda: BossStats.width <= 125)
    DisableButton(ViewScreen.CharacterCustomization, 1000, 200, 135, 40, "Increase", Font.medium, increaseWidth, lambda: BossStats.width >= 325)
    DisableButton(ViewScreen.CharacterCustomization, 450, 250, 135, 40, "Decrease", Font.medium, decreaseHeight, lambda: BossStats.height <= 300)
    DisableButton(ViewScreen.CharacterCustomization, 1000, 250, 135, 40, "Increase", Font.medium, increaseHeight, lambda: BossStats.height >= 600)

    DisableButton(ViewScreen.CharacterCustomization, 700, 350, 175, 40, "Begin Game", Font.medium, lambda: changeScreen(ViewScreen.Tutorial), lambda: BossStats.upgradePoints > 0)

    charcterCustomImage = pygame.image.load("assets\\bnuuy.png")

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

        if stateVars.viewScreen == ViewScreen.CharacterCustomization:
            charcterCustomImageTemp = pygame.transform.scale(charcterCustomImage, (BossStats.width, BossStats.height))
            charcterCustomImageRect = charcterCustomImageTemp.get_rect()
            charcterCustomImageRect = charcterCustomImageRect.move(500, 400)
            screen.blit(charcterCustomImageTemp, charcterCustomImageRect)

        pygame.display.flip()


if __name__ == "__main__":
    main()