from dataclasses import dataclass, field
from collections.abc import Callable
from VisualComponents import *
from standardClasses import *
from Animations import *
import random
#import VisualComponents

oponent = None
inAnimation = False
delayNextTurn = False
doEnemyAttack = True

textColor = (255,158,54) #orange
#textColor = (193, 39, 34) #dark red

@dataclass
class EnemyType():
    physicalStrength: float
    magicalStrength: float
    maxHealth: float
    maxMana: float
    name: str
    imageFile: str

    def spawn(self):
        stateVars.oponent = CombatActor(self.physicalStrength, self.magicalStrength, self.maxHealth, self.maxMana)
        stateVars.oponent.genText((1250, 0), ViewScreen.Battle)
        stateVars.enemyImage.image = pygame.image.load(self.imageFile)
        stateVars.enemyImage.width = 225
        stateVars.enemyImage.height = 450


levelEnemyTypes = {Levels.Cemetery : [EnemyType(5, 5, 50, 50, "Pumpkin", "assets\\pumpkin.png")], 
                    Levels.Woods : [EnemyType(10, 10, 75, 50, "Mushroom", "assets\\mysteryshroom.png")], 
                    Levels.Meadows : [EnemyType(15, 15, 100, 50, "Ranibow Sprimkle", "assets\\ranibowsprimkle.png")],
                    Levels.Boss : []}

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
        global visualComponents, delayNextTurn
        #print(self, " died")
        delayNextTurn = True
        ShrinkAnimation(stateVars.enemyImage, 0.25, self.doDeath).start()

    def delete(self):
        for text in self.texts:
            visualComponents.remove(text)

    def doDeath(self):
        global inAnimation, delayNextTurn, doEnemyAttack
        stateVars.enemyImage.reloadImage()
        self.delete()
        stateVars.player.mana += 10
        stateVars.player.money += 10
        stateVars.manaText2.text = "    +10 mana"
        stateVars.manaText2.start()
        stateVars.moneyText.text = "    +10 money"
        stateVars.moneyText.start()
        spawnEnemy()
        delayNextTurn = False
        doEnemyAttack = False
        nextTurn(stateVars.player)
        doEnemyAttack = True
        inAnimation = False
        stateVars.enemiesDefeated[stateVars.selectLevel.value] += 1
        if stateVars.playerProgression >= stateVars.selectLevel.value and stateVars.enemiesDefeated[stateVars.selectLevel.value] >= 3:
            stateVars.playerProgression += 1
            changeScreen(ViewScreen.BattleClear)

    def genText(self, position, viewScreen):
        self.texts = []
        healthText = DynamicText(viewScreen, position[0], position[1], Font.medium, lambda x: f"    Health: {self.health}/{self.maxHealth}")
        healthText.color = textColor
        self.texts.append(healthText)
        manaText = DynamicText(viewScreen, position[0], position[1]+Font.medium.get_linesize(), Font.medium, lambda x: f"    Mana: {self.mana}/{self.maxMana}")
        manaText.color = textColor
        self.texts.append(manaText)
        self.texts.append(createIcon(viewScreen, Icon.Health, position[0], position[1]+0*(Font.medium.get_linesize()), Font.medium))
        self.texts.append(createIcon(viewScreen, Icon.Mana, position[0], position[1]+1*(Font.medium.get_linesize()), Font.medium))

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
            stateVars.damageText.text = f"    -{source.magicalStrength+self.strength} damage"
        else:
            source.physicalAttack(target, self.strength)
            stateVars.damageText.text = f"    -{source.physicalStrength+self.strength} damage"
            
        stateVars.damageText.start()
        nextTurn(stateVars.player)

    def genText(self, position, useButton, viewScreen, elements):
        elements.append(HollowRect(viewScreen, position[0], position[1], 320, 150, 2.5))
        elements.append(DynamicText(viewScreen, position[0]+3, position[1]+3, pygame.font.Font(size=50), lambda x: self.name))
        elements.append(DynamicText(viewScreen, position[0]+3, position[1]+Font.large.get_linesize()+3, Font.medium, lambda x: f"    Strength: {self.strength}"))
        if self.isMagic:
            elements.append(DynamicText(viewScreen, position[0]+3, position[1]+Font.medium.get_linesize()+Font.large.get_linesize()+3, Font.medium, lambda x: f"    Mana cost: {self.manaCost}"))
        multiText = genMultilineText(self.description, viewScreen, position[0]+3, position[1]+(2 if self.isMagic else 1)*Font.medium.get_linesize()+Font.large.get_linesize()+3, Font.small)
        for text in multiText:
            elements.append(text)

            
        elements.append(createIcon(viewScreen, Icon.MagicalStrength if self.isMagic else Icon.PhysicalStrength,  position[0]+3, position[1]+Font.large.get_linesize()+3, Font.medium))
        if self.isMagic:
            elements.append(createIcon(viewScreen, Icon.Mana, position[0]+3, position[1]+Font.medium.get_linesize()+Font.large.get_linesize()+3, Font.medium))

        if useButton:
            #if self.isMagic:
            return DisableButton(viewScreen, position[0]+230, position[1]+10, 70, 40, "Use", pygame.font.Font(size=48), None, None)
            #return Button(ViewScreen.Battle, position[0]+225, position[1], 75, 45, "Use", Font.large, None)

def nextTurn(player):
    global inAnimation
    if not delayNextTurn:
        inAnimation = True
        if doEnemyAttack:
            stateVars.enemyAnimation.start()

        else:
            finishEnemyAnimate()

def finishEnemyAnimate():
    global inAnimation
    player = stateVars.player
    if doEnemyAttack:
        stateVars.oponent.physicalAttack(player, 10)
        stateVars.damageText2.text = f"    -{stateVars.oponent.physicalStrength+10} damage"
        stateVars.damageText2.start()
    player.mana += 10
    stateVars.oponent.mana += 10
    inAnimation = False

def spawnEnemy():
    random.choice(levelEnemyTypes[stateVars.selectLevel]).spawn()

def regenPlayerText():
    for element in stateVars.player.elements:
        visualComponents.remove(element)
    for button in stateVars.player.buttons:
        buttons.remove(button)
    stateVars.player.buttons = []
    stateVars.player.elements = []
    stateVars.player.genText((0, 0), None, ViewScreen.GachaScreen, False)
    stateVars.player.genText((0, 0), stateVars.oponent, ViewScreen.Battle, True)


@dataclass
class Player(CombatActor):
    attacks: list = field(default_factory=lambda: [])
    money: float = 10
    healPotions: int = 0
    manaPotions: int = 0

    def __post_init__(self):
        #super().__post_init__()
        self.attacks.append(UsePotion(0.0, False, "Health Potion", "Grants 25 health", player=self))
        self.attacks.append(UsePotion(0.0, False, "Mana Potion", "Grants 25 mana", isMana=True, player=self))
        self.elements = []
        self.buttons = []

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

    def genText(self, position, opponent, viewScreen, isUseButton):
        super().genText(position, viewScreen)
        physStrengthText = DynamicText(viewScreen, position[0], position[1]+2*(Font.medium.get_linesize()), Font.medium, lambda x: f"    Physical Strength: {self.physicalStrength}")
        physStrengthText.color = textColor
        self.elements.append(physStrengthText)
        magStrengthText = DynamicText(viewScreen, position[0], position[1]+3*(Font.medium.get_linesize()), Font.medium, lambda x: f"    Magical Strength: {self.magicalStrength}")
        magStrengthText.color = textColor
        self.elements.append(magStrengthText)
        healPotText = DynamicText(viewScreen, position[0], position[1]+4*(Font.medium.get_linesize()), Font.medium, lambda x: f"    Healing Potions: {self.healPotions}")
        healPotText.color = textColor
        self.elements.append(healPotText)
        manaPotText = DynamicText(viewScreen, position[0], position[1]+5*(Font.medium.get_linesize()), Font.medium, lambda x: f"    Mana Potions: {self.manaPotions}")
        manaPotText.color = textColor
        self.elements.append(manaPotText)
        dabloonText = DynamicText(viewScreen, position[0], position[1]+6*(Font.medium.get_linesize()), Font.medium, lambda x: f"    Dabloons: {self.money}")
        dabloonText.color = textColor
        self.elements.append(dabloonText)

        self.elements.append(createIcon(viewScreen, Icon.PhysicalStrength, position[0], position[1]+2*(Font.medium.get_linesize()), Font.medium))
        self.elements.append(createIcon(viewScreen, Icon.MagicalStrength, position[0], position[1]+3*(Font.medium.get_linesize()), Font.medium))
        self.elements.append(createIcon(viewScreen, Icon.HealPotion, position[0], position[1]+4*(Font.medium.get_linesize()), Font.medium))
        self.elements.append(createIcon(viewScreen, Icon.ManaPotion, position[0], position[1]+5*(Font.medium.get_linesize()), Font.medium))
        self.elements.append(createIcon(viewScreen, Icon.Coin, position[0], position[1]+6*(Font.medium.get_linesize()), Font.medium))

        if isUseButton:
            @dataclass
            class AttackButtonContainer:
                attack: Attack
                def _attack(iself):
                    global inAnimation
                    inAnimation = True
                    iself.attack.attack(self, stateVars.oponent)
                def canAttack(iself):
                    global oponent
                    return not iself.attack.canAttack(self, oponent) or inAnimation

        for i, attack in enumerate(self.attacks):
            useButton = attack.genText((position[0], position[1]+7*(Font.medium.get_linesize())+i*150), isUseButton, viewScreen, self.elements)
            if isUseButton:
                self.elements.append(useButton)
                self.buttons.append(useButton)
                myAttack = AttackButtonContainer(attack)
                useButton.action = myAttack._attack
                useButton.isDisabled = myAttack.canAttack
    
    def die(self):
        self.health = self.maxHealth
        self.money = 0
        changeScreen(ViewScreen.DiedScreen)
        self.mana = 0

@dataclass
class UsePotion(Attack):
    isMana: bool = False
    player: Player = None
    def __post_init__(self):
        super().__post_init__()
        self.canAttack = lambda x, y: self.player.canManaPotion() if self.isMana else self.player.canHealPotion()
    
    def _attack(self, player, y):
        if self.isMana:
            player.mana += 25
            player.manaPotions -= 1
            stateVars.manaText2.text = "    +25 mana"
            stateVars.manaText.start()
        else:
            player.health += 50
            player.healPotions -= 1
            stateVars.healthText.start()
        nextTurn(player)
