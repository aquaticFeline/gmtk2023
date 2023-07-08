from dataclasses import dataclass
from collections.abc import Callable
from standardClasses import *
from VisualComponents import *
from combat import *
import random

# Gacha Rewards: 
# Common: Money (5%) (5-10)
# Uncommon: Health Potions & Mana Potions (10%, 10%) (3-7)
# Rare: Character Stat Buffs (25%) (1-3)
#  - Max Health
#  - Max Mana
#  - Physical Strength
#  - Magical Strength
#  - 
# Epic: ???
# Legendary: New Attacks (50%)
# 

swapButons = []
swapping = False

def swap(player, attack, position):
    player.attacks[position] = attack
    regenPlayerText()
    clearButtons()

def clearButtons():
    global swapping, swapButons
    swapping = False
    for button in swapButons:
        visualComponents.remove(button)
        buttons.remove(button)
    swapButons = []

def _genSwapButton(player, attack, i):
    position = (0, 0)
    swapButons.append(Button(ViewScreen.GachaScreen, position[0]+200, position[1]+6*(Font.medium.get_linesize())+i*150, 100, 45, "Swap", Font.large, lambda: swap(player, attack, i)))

def genSwapButtons(player, attack):
    global swapping
    swapping = True
    for i in range(len(player.attacks)-2):
        _genSwapButton(player, attack, i)
    swapButons.append(Button(ViewScreen.GachaScreen, 1300, 55, 250, 45, "Discard", Font.large, lambda: clearButtons()))

@dataclass
class Reward():
    collect: Callable[[], None]
    draw: Callable[[pygame.Surface], None]

def genGacha(player):
    def getReward():
        rewardType = random.randint(0, 19)
        if rewardType % 4 == 0:
            return genCurrencyReward(random.choice(["maxHealth", "maxMana", "physicalStrength", "magicalStrength"]), random.randint(1, 3), player)
        if rewardType == 1:
            return genCurrencyReward("money", random.randint(5, 10), player)
        if rewardType == 18 or rewardType == 19:
            return genCurrencyReward("healPotions", random.randint(3, 7), player)
        if rewardType == 15 or rewardType == 17:
            return genCurrencyReward("manaPotions", random.randint(3, 7), player)
        return genAttackReward(Attack(0, False, "None", "None"), player)

    gachaAnimation = GachaAnimation(ViewScreen.GachaScreen, getReward, player)

def genAttackReward(attack, player):
    attackElements = []
    attack.genText((60, 35), False, ViewScreen.Test, attackElements)
    for attackElement in attackElements:
        visualComponents.remove(attackElement)

    def collect():
        genSwapButtons(player, attack)
    def draw(surface):
        myText = Font.medium.render(f"New Attack", True, Color.white)
        myTextRect = myText.get_rect()
        surface.blit(myText, myTextRect)
        for attackElement in attackElements:
            attackElement.draw(surface)
    return Reward(collect, draw)

def genCurrencyReward(currency, amount, player):
    def collect():
        player.__setattr__(currency, amount+player.__getattribute__(currency))
    def draw(surface):
        myText = Font.medium.render(f"+{amount} {currency}", True, Color.white)
        myTextRect = myText.get_rect()
        surface.blit(myText, myTextRect)
    return Reward(collect, draw)

@dataclass
class GachaAnimation(VisualComponent):
    getReward: Callable[[], Reward]
    player: Player
    completion: float = 0.0
    reward: Reward = None
    animationStartTime: float = 0
    animationPlaying: bool = False
    
    def __post_init__(self):
        super().__post_init__()
        self.leftImage = pygame.image.load("assets/leftscroll.png")
        self.leftImage = pygame.transform.scale(self.leftImage, (75, 300))
        self.rightImage = pygame.image.load("assets/rightscroll.png")
        self.rightImage = pygame.transform.scale(self.rightImage, (75, 300))
        self.center = 800
        self.top = 150
        self.animationScale = 225
        self.createRollButton()

    def roll(self):
        global buttons
        self.animationStartTime = time.time()
        self.animationPlaying = True
        self.player.money -= 5
        buttons.remove(self.rollButton)
        visualComponents.remove(self.rollButton)
        self.reward = self.getReward()

    def animationComplete(self):
        self.completion = 1
        self.animationPlaying = False
        self.createCollectButton()

    def collectReward(self):
        global buttons
        self.completion = 0
        self.createRollButton()
        buttons.remove(self.collectButton)
        visualComponents.remove(self.collectButton)
        self.reward.collect()

    def createRollButton(self):
        self.rollButton = DisableButton(self.viewScreen, self.center - 50, self.top+325, 100, 50, "Roll $5", Font.medium, self.roll, lambda: not self.player.canBuy(5) or swapping)

    def createCollectButton(self):
        self.collectButton = Button(self.viewScreen, self.center - 50, self.top+225, 100, 50, "Collect", Font.medium, self.collectReward)
    
    def draw(self, surface):
        if self.animationPlaying:
            self.completion = (time.time() - self.animationStartTime)/3.0
            if self.completion > 1:
                self.animationComplete()


        leftRect = self.leftImage.get_rect()
        leftRect = leftRect.move(self.center-75-self.animationScale*self.completion, self.top)
        surface.blit(self.leftImage, leftRect)

        rightRect = self.rightImage.get_rect()
        rightRect = rightRect.move(self.center+self.animationScale*self.completion, self.top)
        surface.blit(self.rightImage, rightRect)

        centerRect = pygame.rect.Rect(self.center-self.animationScale*self.completion, self.top+12.5*1.5, 2*self.animationScale*self.completion+2, 262.5)
        #pygame.draw.rect(surface, (193, 190, 169), centerRect)

        if self.reward is not None:
            rewardSurface = pygame.Surface(centerRect.size)
            rewardSurface.fill((193, 190, 169))
            self.reward.draw(rewardSurface)
            surface.blit(rewardSurface, centerRect)