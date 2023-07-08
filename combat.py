from dataclasses import dataclass, field
from collections.abc import Callable
from VisualComponents import *
from standardClasses import *
#import VisualComponents

oponent = None

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
        stateVars.player.mana += 10
        stateVars.player.money += 10
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
        DynamicText(ViewScreen.Battle, position[0], position[1], pygame.font.Font(size=50), lambda x: self.name)
        DynamicText(ViewScreen.Battle, position[0], position[1]+Font.large.get_linesize(), Font.medium, lambda x: f"Strength: {self.strength}")
        if self.isMagic:
            DynamicText(ViewScreen.Battle, position[0], position[1]+Font.medium.get_linesize()+Font.large.get_linesize(), Font.medium, lambda x: f"Mana cost: {self.manaCost}")
        genMultilineText(self.description, ViewScreen.Battle, position[0], position[1]+(2 if self.isMagic else 1)*Font.medium.get_linesize()+Font.large.get_linesize(), Font.small)
        
        if useButton:
            #if self.isMagic:
            return DisableButton(ViewScreen.Battle, position[0]+225, position[1], 75, 45, "Use", Font.large, None, None)
            #return Button(ViewScreen.Battle, position[0]+225, position[1], 75, 45, "Use", Font.large, None)

def nextTurn(player):
    stateVars.oponent.physicalAttack(player, 10)
    player.mana += 10
    stateVars.oponent.mana += 10

def spawnEnemy():
    stateVars.oponent = CombatActor(10, 10, 50, 50)
    stateVars.oponent.genText((1250, 0))




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
                iself.attack.attack(self, stateVars.oponent)
                nextTurn(self)
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
        else:
            player.health += 50
            player.healPotions -= 1