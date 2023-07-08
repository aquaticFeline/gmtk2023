from dataclasses import dataclass
from collections.abc import Callable
from VisualComponents import *
from combat import *
import random

@dataclass
class Reward():
    collect: Callable[[], None]
    draw: Callable[[pygame.Surface], None]

def genGacha(player):
    def getReward():
        return genReward(random.choice(["health", "maxHealth", "mana", "maxMana", "physicalStrength", "magicalStrength", "healPotions", "manaPotions", "money"]), random.randint(1, 15), player)

    gachaAnimation = GachaAnimation(ViewScreen.GachaScreen, getReward, player)

def genReward(currency, amount, player):
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
        self.leftImage = pygame.transform.scale(self.leftImage, (50, 200))
        self.rightImage = pygame.image.load("assets/rightscroll.png")
        self.rightImage = pygame.transform.scale(self.rightImage, (50, 200))
        self.center = 250
        self.top = 50
        self.animationScale = 150
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
        self.rollButton = DisableButton(self.viewScreen, self.center - 50, self.top+225, 100, 50, "Roll $5", Font.medium, self.roll, lambda: not self.player.canBuy(5))

    def createCollectButton(self):
        self.collectButton = Button(self.viewScreen, self.center - 50, self.top+125, 100, 50, "Collect", Font.medium, self.collectReward)
    
    def draw(self, surface):
        if self.animationPlaying:
            self.completion = (time.time() - self.animationStartTime)/3.0
            if self.completion > 1:
                self.animationComplete()


        leftRect = self.leftImage.get_rect()
        leftRect = leftRect.move(self.center-50-self.animationScale*self.completion, self.top)
        surface.blit(self.leftImage, leftRect)

        rightRect = self.rightImage.get_rect()
        rightRect = rightRect.move(self.center+self.animationScale*self.completion, self.top)
        surface.blit(self.rightImage, rightRect)

        centerRect = pygame.rect.Rect(self.center-self.animationScale*self.completion, self.top+12.5, 2*self.animationScale*self.completion+2, 175)
        #pygame.draw.rect(surface, (193, 190, 169), centerRect)

        if self.reward is not None:
            rewardSurface = pygame.Surface(centerRect.size)
            rewardSurface.fill((193, 190, 169))
            self.reward.draw(rewardSurface)
            surface.blit(rewardSurface, centerRect)