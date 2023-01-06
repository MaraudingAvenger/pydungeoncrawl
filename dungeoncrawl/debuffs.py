
import random
from dungeoncrawl.entities.effects import Effect

#############################
# ~~ Training Dummy Debuff ~~#
#############################


class Embarassed(Effect):
    def __init__(self) -> None:
        super().__init__(
            name="Embarassed",
            duration=3,
            category={'embarassed', 'debuff', 'spirit', 'spiritual'},
            description=f'The training dummy shouted, "{self.get_random_insult()}"',
            symbol='✨')

    def get_random_insult(self) -> str:
        insults = [
            "What a pillock!",
            "You absolute berk!",
            "I would pity you if you weren't such a buffoon!",
            "Your nincompoopery knows no bounds!",
            "You absolute ninnyhammer!",
            "You absolute ninny!",
            "You milquetoast!",
            "You pettifogging hobbledehoy!",
            "If you weren't such a cow-handed fopdoodle, I might be scared!",
            "You fragrant man-swine!",
            "If I wanted a kiss I'd have called your mother!",
            "If laughter is the best medicine, your face is curing the world!",
            "If I had a face like yours I'd sue my parents!",
            "If I wanted to kill myself I'd climb your ego and jump to your IQ!",
            "I don't know what makes you so stupid, but it really works!",
            "Calling you an idiot would be an insult to all stupid people!",
            "When your mother dropped you off at the schoolhouse she was fined for littering!",
            "Some babies were dropped on their heads but you were clearly thrown at a wall!",
            "I would slap you, but that would be animal abuse!",
            "If being ugly is a crime, you should be locked up for life!",
            "I don't know what your problem is, but I'll bet it's hard to pronounce!",
            "You are the reason the gene pool needs a lifeguard!",
            "Unfortunately stupidity is not a crime, so you're free to go!",
            "How did you get here, did someone leave your cage open?",
            "Don't you have a terribly empty feeling... in your skull?",
            "Are you always this stupid, or is today a special occasion?",
            "I would agree with you if I wanted us both to be wrong!",
            "Some cause happiness wherever they go. You cause happiness *whenever* you go!",
            "I'm glad to see you're not letting education get in the way of your ignorance!",
            "Don't be ashamed of who you are, that's your parents' job!",
            "You've got two brain cells that are both fighting for third place!",
            "You couldn't pour water out of a boot if the instructions were on the heel!",
            "You are proof God makes mistakes!",
            "Calling you an imbecile is an insult to imbeciles everywhere!",
            "I love what you've done with your hair... how do you get it to come out of the nostrils like that?",
            "If you spend word for word with me, I shall make your wit bankrupt!",
            "You may look like an idiot and talk like an idiot, but don't let that fool you, you really are an idiot!",
            "You have no enemies, but you are intensely disliked by your friends!",
            "You are impossible to underestimate!",
            "As an outsider, what is your perspective on intelligence?",
            "The bar is so low it's practically a tripping hazard in hell, but here you are dancing the limbo with the devil!",
            "If my dog looked like you, I'd shave his backside and teach him to walk backwards!",
            "Some day you'll go far, and we all hope you stay there!",
            "Mirrors cannot talk. Luckily for you, they can't laugh, either!",
            "Your face makes onions cry!",
            "Your teeth are so bad you can eat an apple through a fence!"
            "I'll never forget the first time we met, although I'll keep trying!",
            "You have miles to go before you reach mediocre!",
            "I would prefer a battle of wits, but I see you are unarmed!"
        ]
        return random.choice(insults)


class Poison(Effect):
    def __init__(self, target, duration:int=3, dot_amount:int=3) -> None:
        self._dot_amount = dot_amount
        self.target = target
        super().__init__(name="Poison", duration=duration,
                         category={'dot', 'poison', 'debuff', 'damage', 'damage over time'}, symbol='🐍')
        
    @property
    def damage_over_time(self) -> int:
        if self.target.poisoned:
            return self._dot_amount * 2
        return self._dot_amount
    
    @damage_over_time.setter
    def damage_over_time(self, value) -> None:
        self._dot_amount = value


class Stun(Effect):
    def __init__(self, duration) -> None:
        super().__init__(name="Stun", duration=duration,
                         category={'stun', 'debuff', 'debilitating', 'physical'}, symbol='💫')


class Root(Effect):
    def __init__(self, duration) -> None:
        super().__init__(name="Root", duration=duration,
                         category={'root', 'slow', 'debilitating', 'debuff'}, symbol='🐌')


class Blind(Effect):
    def __init__(self, duration) -> None:
        super().__init__(name="Blind", duration=duration,
                         category={'blind', 'debilitating', 'debuff'}, symbol='👀')


class Frailty(Effect):
    def __init__(self, duration) -> None:
        super().__init__(name="Frailty", duration=duration, deal_bonus_damage_percent=-.05,
                         category={'frailty', 'physical', 'debuff', 'damage reduction'}, symbol='🤏')


class ExposeWeakness(Effect):
    def __init__(self, duration) -> None:
        super().__init__(name="Expose Weakness", duration=duration, take_bonus_damage_percent=.05,
                         category={'expose weakness', 'physical', 'debuff'}, symbol='🥴')


class PoisonVulnerability(Effect):
    def __init__(self, duration) -> None:
        super().__init__(name="Poison Vulnerability", duration=duration,
                         category={'poison', 'vulnerable', 'debuff'}, symbol='🤢')


class MagicVulnerability(Effect):
    def __init__(self) -> None:
        super().__init__(name="Magic Vulnerability", duration=10, category={
            'magic', 'magic vulnerability', 'debuff', 'vulnerable'}, take_bonus_damage_percent=.10, symbol='🤩')


class DoT(Effect):
    def __init__(self, target, name: str, duration:int=3, dot_amount:int=3) -> None:
        super().__init__(name=name, duration=duration, damage_over_time=dot_amount,
                         category={'dot', 'debuff', 'damage', 'damage over time'}, symbol='🩸')

class FrostResistance(Effect):
    def __init__(self) -> None:
        super().__init__(name="Frost Resistance", duration=20, category={
            'resist', 'frost', 'frost resistance'}, take_bonus_damage_percent=-.10, symbol='🥶')


class FireResistance(Effect):
    def __init__(self) -> None:
        super().__init__(name="Fire Resistance", duration=20, category={
            'resist', 'fire', 'fire resistance'}, take_bonus_damage_percent=-.10, symbol='🥵')

