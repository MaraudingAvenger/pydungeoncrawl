
import random
from dungeoncrawl.entities.effects import Effect
from dungeoncrawl.utilities.location import bresenham

#############################
# ~~ Training Dummy Debuff ~~#
#############################


class Embarassed(Effect):
    def __init__(self) -> None:
        super().__init__(
            name="Embarassed",
            duration=3,
            category={'embarassed', 'debuff', 'spirit', 'spiritual', 'mental', 'curable'},
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
                         category={'dot', 'poison', 'debuff', 'damage', 'damage over time', 'curable'}, symbol='🐍')
        
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
                         category={'stun', 'debuff', 'debilitating', 'physical', 'curable'}, symbol='💫')


class Root(Effect):
    def __init__(self, duration) -> None:
        super().__init__(name="Root", duration=duration,
                         category={'root', 'slow', 'debilitating', 'debuff', 'curable'}, symbol='🐌')


class Blind(Effect):
    def __init__(self, duration) -> None:
        super().__init__(name="Blind", duration=duration,
                         category={'blind', 'debilitating', 'debuff', 'curable'}, symbol='👀')


class Frailty(Effect):
    def __init__(self, duration) -> None:
        super().__init__(name="Frailty", duration=duration, deal_bonus_damage_percent=-.05,
                         category={'frailty', 'physical', 'debuff', 'damage reduction'}, symbol='🤏')


class ExposeWeakness(Effect):
    def __init__(self, duration) -> None:
        super().__init__(name="Expose Weakness", duration=duration, take_bonus_damage_percent=.05,
                         category={'expose weakness', 'physical', 'debuff', 'modifier'}, symbol='🥴')


class PoisonVulnerability(Effect):
    def __init__(self, duration) -> None:
        super().__init__(name="Poison Vulnerability", duration=duration,
                         category={'poison', 'vulnerable', 'debuff', 'curable'}, symbol='🤢')


class MagicVulnerability(Effect):
    def __init__(self) -> None:
        super().__init__(name="Magic Vulnerability", duration=10, category={
            'magic', 'magic vulnerability', 'debuff', 'vulnerable', 'curable'}, take_bonus_damage_percent=.10, symbol='🤩')


class DoT(Effect):
    def __init__(self, target, name: str, duration:int=3, dot_amount:int=3) -> None:
        self.target=target
        super().__init__(name=name, duration=duration, damage_over_time=dot_amount,
                         category={'dot', 'debuff', 'damage', 'damage over time', 'curable'}, symbol='🩸')


class Curse(Effect):
    def __init__(self, caster, target, duration, dot_amount) -> None:
        super().__init__(name="Curse", duration=duration, damage_over_time=dot_amount,
                         category={'dot', 'debuff', 'damage', 'damage over time', 'curable'}, symbol='🩸')
        self.target = target
        self.caster = caster

    def on_expire(self):
        self.target._take_damage(self.caster, 10000, 'curse', True, "Curse")

class Doom(Effect):
    def __init__(self, caster, target, damage: int) -> None:
        self.caster = caster
        self.base_damage = damage
        self.multiplier = 1
        self.triggered = 0
        super().__init__(name="Doom", description="Your doom is near", duration=15, category={'doom', 'curable'}, symbol='☠️')
        self.target=target
    
    def increase_doom(self):
        self.triggered += 1
        
        for _ in self.target.effects.get_any_category_name('debuff'):
            self.multiplier += 0.05
        self.target.effects.remove_category('debuff')

        self.base_damage *= self.multiplier
        self.duration = 15

        if self.triggered >= 6:
            self.duration = 0

    def on_expire(self):
        self.duration=0
        self.target._take_damage(self.caster, int(self.base_damage), 'spirit', True, "Doom")

class ShadeOfDeath(Effect):
    def __init__(self, caster, target, damage:int=0) -> None:
        self.position = caster.position
        self.damage_total = damage
        self.target = target
        self.caster = caster
        super().__init__( name='Shade of Death', category={'debuff', 'damage'}, symbol='👻')
        self.duration = len(list(bresenham(self.position, target.position)))

    @property
    def duration(self) -> int:
        return self._duration

    @duration.setter
    def duration(self, _) -> None:
        path = list(bresenham(self.position, self.target.position))
        self._duration = len(path)
        self.position = path[0] if path else self.position

    def on_expire(self):
        self.target._take_damage(self.caster, self.damage_total, 'spirit', True, "Shade of Death")
        self.target.effects.add_stacks(ExposeWeakness, stacks=10, duration=5)
        self.target.effects.add_stacks(MagicVulnerability, stacks=10)
        self.target.effects.add_stacks(Frailty, stacks=10, duration=5)

class FrostResistance(Effect):
    def __init__(self) -> None:
        super().__init__(name="Frost Resistance", duration=20, category={
            'resist', 'ice', 'frost', 'frost resistance'}, take_bonus_damage_percent=-.10, symbol='🥶')


class FireResistance(Effect):
    def __init__(self) -> None:
        super().__init__(name="Fire Resistance", duration=20, category={
            'resist', 'fire', 'fire resistance'}, take_bonus_damage_percent=-.10, symbol='🥵')

