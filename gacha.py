from dataclasses import dataclass
from collections.abc import Callable
from combat import *
from standardClasses import *
from VisualComponents import *
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

def addAnimationToAttack(attack, animation):
    def punchAttackAttack(x, y):
        global inAnimation
        animation.start()
        inAnimation = True
    def doPunchAttack():
        attack._attack(stateVars.player, stateVars.oponent)
    animation.onEnd = doPunchAttack
    attack.attack = punchAttackAttack

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
    #position[0]+235, position[1]+10, 65, 35, "Use", pygame.font.Font(size=48), 
    swapButons.append(Button(ViewScreen.GachaScreen, position[0]+210, position[1]+7*(Font.medium.get_linesize())+i*150+10, 95, 45, "Swap", pygame.font.Font(size=48), lambda: swap(player, attack, i)))

def genSwapButtons(player, attack):
    global swapping
    swapping = True
    for i in range(len(player.attacks)-2):
        _genSwapButton(player, attack, i)
    swapButons.append(Button(ViewScreen.GachaScreen, 750, 530, 100, 45, "Discard", Font.medium, lambda: clearButtons()))

@dataclass
class Reward():
    collect: Callable[[], None]
    draw: Callable[[pygame.Surface], None]

def genGacha(player):
    def getReward():
        rewardType = random.randint(0, 19)
        if rewardType % 4 == 0:
            if random.randint(0, 1) == 0:
                currency = random.choice([("physicalStrength", "Physical Strength", Icon.PhysicalStrength), 
                                            ("magicalStrength", "Magical Strength", Icon.MagicalStrength)])
                return genCurrencyReward(currency[0], currency[1], currency[2], random.randint(2, 6), player, stateVars.rareImage)
            currency = random.choice([("maxHealth", "Max Health", Icon.Health), 
                                        ("maxMana", "Max Mana", Icon.Mana)])
            return genCurrencyReward(currency[0], currency[1], currency[2], random.randint(15, 40), player, stateVars.rareImage)
        if rewardType == 1:
            return genCurrencyReward("money", "Dabloons", Icon.Coin, random.randint(5, 10), player, stateVars.commonImage)
        if rewardType == 18 or rewardType == 19:
            return genCurrencyReward("healPotions", "Healing Potions", Icon.HealPotion, random.randint(4, 8), player, stateVars.uncommonImage)
        if rewardType == 15 or rewardType == 17:
            return genCurrencyReward("manaPotions", "Mana Potions", Icon.ManaPotion, random.randint(4, 8), player, stateVars.uncommonImage)

        #return genAttackReward(random.choice([stateVars.plantShroudAttack]), player)
        return genAttackReward(random.choice([stateVars.punchAttack, stateVars.shredAttack, stateVars.bonkAttack, stateVars.waterBoltAttack, stateVars.plantShroudAttack, stateVars.enlightenmentAttack, stateVars.frostAttack, stateVars.shadowfallAttack, stateVars.fireBallAttack]), player)

    gachaAnimation = GachaAnimation(ViewScreen.GachaScreen, getReward, player)
    returnTestButton = DisableButton(ViewScreen.GachaScreen, 1300, 0, 250, 50, "Return To World Map", pygame.font.Font(size=32), lambda: changeScreen(ViewScreen.WorldMap), lambda: swapping or gachaAnimation.animationPlaying)

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
        myImage = pygame.transform.scale(stateVars.legendaryImage, (160, 40))
        myImageRect = myImage.get_rect()
        myImageRect = myImageRect.move(450-160, 0)
        surface.blit(myImage, myImageRect)
    return Reward(collect, draw)

def genCurrencyReward(currency, name, icon, amount, player, badge):
    def collect():
        player.__setattr__(currency, amount+player.__getattribute__(currency))
    def draw(surface):
        myText = Font.medium.render(f"+{amount} {name}", True, Color.white)
        myTextRect = myText.get_rect()
        myTextRect = myTextRect.move((450-myTextRect.width)/2.0, 30)
        surface.blit(myText, myTextRect)
        bigText = Font.large.render(f"+{amount}  ", True, Color.white)
        bigTextRect = bigText.get_rect()
        bigTextRect = bigTextRect.move((450-bigTextRect.width)/2.0, 120)
        surface.blit(bigText, bigTextRect)

        iconImg.x = bigTextRect.x+60
        iconImg.y = bigTextRect.y
        iconImg.draw(surface)

        myImage = pygame.transform.scale(badge, (160, 40))
        myImageRect = myImage.get_rect()
        myImageRect = myImageRect.move(450-160, 0)
        surface.blit(myImage, myImageRect)

    iconImg = createIcon(ViewScreen.Test, icon, 0, 0, Font.large)
    visualComponents.remove(iconImg)

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
        self.leftImage = pygame.image.load("assets/leftscroll.png").convert_alpha()
        self.leftImage = pygame.transform.scale(self.leftImage, (75, 300))
        self.rightImage = pygame.image.load("assets/rightscroll.png").convert_alpha()
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
        visualComponents.remove(self.rollCost)
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
        self.rollButton = DisableButton(self.viewScreen, self.center - 50, self.top+325, 100, 50, "Roll 5    ", Font.medium, self.roll, lambda: not self.player.canBuy(5) or swapping)
        self.rollCost = createIcon(self.viewScreen, Icon.Coin, self.center-50 + 6*12, self.top+325+15, Font.medium)

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

            
@dataclass
class GoToGachaButton(VisualComponent):
    x: float
    y: float
    width: float
    height: float
    imageFile: str
    action: Callable[[], None]

    def __post_init__(self):
        super().__post_init__()
        buttons.append(self)
        self.image = pygame.image.load(self.imageFile).convert_alpha()
        self.animating = False
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.completion = 0

    def triggerAnimation(self):
        self.animating = True
        self.startTime = time.time()

    def stopAnimation(self):
        self.animating = False

    def draw(self, surface):
        mouse = convertMousePos(pygame.mouse.get_pos())
        if self.x < mouse[0] < self.x+self.width and self.y < mouse[1] < self.y+self.height:
            if not self.animating and self.completion <= 0:
                self.triggerAnimation()
            if self.animating and self.completion > 1:
                self.stopAnimation()
        else:
            if not self.animating and self.completion >= 1:
                self.triggerAnimation()
            if self.animating and self.completion < 0:
                self.stopAnimation()
        if self.animating:
            if self.x < mouse[0] < self.x+self.width and self.y < mouse[1] < self.y+self.height:
                self.completion = (time.time()-self.startTime)/2.5
            else:
                self.completion = 1-(time.time()-self.startTime)/2.5

        imageRect = self.image.get_rect()
        imageRect = imageRect.move(self.x, self.y-self.completion*150)
        surface.blit(self.image, imageRect)




    def checkAction(self):
        mouse = convertMousePos(pygame.mouse.get_pos())
        if self.x < mouse[0] < self.x+self.width and self.y < mouse[1] < self.y+self.height:
            self.action()
            return True
        return False