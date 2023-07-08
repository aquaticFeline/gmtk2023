import pygame, sys, math, time, random, copy
from dataclasses import dataclass, field
from collections.abc import Callable
from standardClasses import *
from VisualComponents import *
import stateVars

player, oponent = None, None

@dataclass
class CombatActor:
    physicalStrength: float
    magicalStrength: float
    _health: float
    maxHealth: float
    _mana: float = 0
    maxMana: float = 50

    @property 
    def health(self):
        return self._health

    @health.setter
    def health(self, val):
        self._health = min(self.maxHealth, val)
        if val <= 0:
            self.die()

    @property 
    def mana(self):
        return self._mana

    @mana.setter
    def mana(self, val):
        self._mana = min(self.maxMana, val)

    def physicalAttack(self, target, strength):
        target.health -= self.physicalStrength + strength

    def magicalAttack(self, target, strength, cost):
        target.health -= self.magicalStrength + strength
        self.mana -= cost

    def canCast(self, cost):
        return cost <= self.mana

    def die(self):
        global visualComponents
        #print(self, " died")
        for text in self.texts:
            visualComponents.remove(text)
        player.mana += 10
        player.money += 10
        spawnEnemy()

    def genText(self, position):
        self.texts = []
        self.texts.append(DynamicText(ViewScreen.Battle, position[0], position[1], Font.medium, lambda x: f"Health: {self.health}/{self.maxHealth}"))
        self.texts.append(DynamicText(ViewScreen.Battle, position[0], position[1]+Font.medium.get_linesize(), Font.medium, lambda x: f"Mana: {self.mana}/{self.maxMana}"))

@dataclass
class Attack:
    strength: float
    isMagic: bool
    name: str
    description: str
    manaCost: float = 0
    attack: Callable[[CombatActor, CombatActor], None] = None
    canAttack: Callable[[CombatActor, CombatActor], bool] = None

    def __post_init__(self):
        self.attack = lambda x, y: self._attack(x, y)
        self.canAttack = lambda x, y: (not self.isMagic) or self.manaCost <= x.mana

    def _attack(self, source, target):
        if self.isMagic:
            source.magicalAttack(target, self.strength, self.manaCost)
        else:
            source.physicalAttack(target, self.strength)

    def genText(self, position, useButton):
        HollowRect(ViewScreen.Battle, position[0], position[1], 300, 150, 2.5)
        DynamicText(ViewScreen.Battle, position[0], position[1], Font.large, lambda x: self.name)
        DynamicText(ViewScreen.Battle, position[0], position[1]+Font.large.get_linesize(), Font.medium, lambda x: f"Strength: {self.strength}")
        if self.isMagic:
            DynamicText(ViewScreen.Battle, position[0], position[1]+Font.medium.get_linesize()+Font.large.get_linesize(), Font.medium, lambda x: f"Mana cost: {self.manaCost}")
        genMultilineText(self.description, ViewScreen.Battle, position[0], position[1]+(2 if self.isMagic else 1)*Font.medium.get_linesize()+Font.large.get_linesize(), Font.small)
        
        if useButton:
            #if self.isMagic:
            return DisableButton(ViewScreen.Battle, position[0]+225, position[1], 75, 45, "Use", Font.large, None, None)
            #return Button(ViewScreen.Battle, position[0]+225, position[1], 75, 45, "Use", Font.large, None)

def nextTurn():
    oponent.physicalAttack(player, 10)
    player.mana += 10
    oponent.mana += 10

def spawnEnemy():
    global oponent
    oponent = CombatActor(10, 10, 50, 50)
    oponent.genText((1250, 0))

class UsePotion(Attack):
    pass


@dataclass
class Player(CombatActor):
    attacks: list = field(default_factory=lambda: [])
    money: float = 10
    healPotions: int = 0
    manaPotions: int = 0

    def canBuy(self, cost):
        return cost <= self.money

    def useHealPotion(self):
        self.healPotions -= 1
        health += 25

    def canHealPotion(self):
        return self.healPotions > 0

    def useManaPotion(self):
        self.manaPotions -= 1
        mana += 25

    def canManaPotion(self):
        return self.manaPotions > 0

    def genText(self, position, opponent):
        super().genText(position)
        DynamicText(ViewScreen.Battle, position[0], position[1]+2*(Font.medium.get_linesize()), Font.medium, lambda x: f"Physical Strength: {self.physicalStrength}")
        DynamicText(ViewScreen.Battle, position[0], position[1]+3*(Font.medium.get_linesize()), Font.medium, lambda x: f"Magical Strength: {self.magicalStrength}")
        DynamicText(ViewScreen.Battle, position[0], position[1]+4*(Font.medium.get_linesize()), Font.medium, lambda x: f"Healing Potions: {self.healPotions}")
        DynamicText(ViewScreen.Battle, position[0], position[1]+5*(Font.medium.get_linesize()), Font.medium, lambda x: f"Mana Potions: {self.manaPotions}")

        @dataclass
        class AttackButtonContainer:
            attack: Attack
            def _attack(iself):
                global oponent
                iself.attack.attack(self, oponent)
                nextTurn()
            def canAttack(iself):
                global oponent
                return not iself.attack.canAttack(self, oponent)

        for i, attack in enumerate(self.attacks):
            useButton = attack.genText((position[0], position[1]+6*(Font.medium.get_linesize())+i*150), True)
            myAttack = AttackButtonContainer(attack)
            useButton.action = myAttack._attack
            useButton.isDisabled = myAttack.canAttack
    
    def die(self):
        self.health = self.maxHealth
        self.money = 0
        changeScreen(ViewScreen.WorldMap)
        player.mana = 0





@dataclass
class Reward():
    collect: Callable[[], None]
    draw: Callable[[pygame.Surface], None]

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

def genReward(currency, amount, player):
    def collect():
        player.__setattr__(currency, amount+player.__getattribute__(currency))
    def draw(surface):
        myText = Font.medium.render(f"+{amount} {currency}", True, Color.white)
        myTextRect = myText.get_rect()
        surface.blit(myText, myTextRect)
    return Reward(collect, draw)


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
    spawnEnemy()

    player.attacks.append(Attack(10.0, False, "Punch", "punch 'em \nin the face"))
    player.attacks.append(Attack(10.0, True, "Fire Ball", "Shoots a \nfire ball", 20.0))

    quitButton = Button(ViewScreen.Test, 100, 0, 100, 40, "Quit", Font.large, myQuit)

    randomNumberText = Text(ViewScreen.Test, 0, 0, Font.large, None, f"{randomNumber}")
    playerHealthText = DynamicText(ViewScreen.Test, 0, 50, Font.large, lambda self: f"{player.health}")
    oponentHealthText = DynamicText(ViewScreen.Test, 0, 100, Font.large, lambda self: f"{oponent.health}")
    
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

    def getReward():
        return genReward(random.choice(["health", "maxHealth", "mana", "maxMana", "physicalStrength", "magicalStrength", "healPotions", "manaPotions", "money"]), random.randint(1, 15), player)

    gachaAnimation = GachaAnimation(ViewScreen.GachaScreen, getReward, player)

    lastTime = time.time()

    viewSurfaces = {veiwScreen : pygame.Surface(screen_size) for veiwScreen in ViewScreen}

    while True:
        screen.fill(Color.black)
        for surface in viewSurfaces.values():
            surface.fill(Color.black)

        checkEvents(playerWorldMap)
            
        if pygame.key.get_pressed()[pygame.K_a] and lastTime - time.time() < -0.1:
            lastTime = time.time()
            player.attack(oponent)

        for visualComponent in visualComponents:
            visualComponent.draw(viewSurfaces[visualComponent.viewScreen])

        screen.blit(viewSurfaces[stateVars.viewScreen], screen_rect)

        pygame.display.flip()


if __name__ == "__main__":
    main()