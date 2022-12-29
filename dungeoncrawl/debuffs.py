
from dungeoncrawl.entities.effects import Effect


class Stun(Effect):
    def __init__(self, duration) -> None:
        super().__init__(name="Stun", duration = duration, category={'stun', 'debuff', 'physical'}, symbol='💫')

class Root(Effect):
    def __init__(self, duration) -> None:
        super().__init__(name="Root", duration = duration, category={'root', 'slow', 'debuff'}, symbol='🐌')

class Blind(Effect):
    def __init__(self, duration) -> None:
        super().__init__(name="Blind", duration = duration, category={'blind', 'debuff'}, symbol='👀')

class Frailty(Effect):
    def __init__(self, duration) -> None:
        super().__init__(name="Frailty", duration = duration, deal_bonus_damage_percent=-.05, category={'frailty', 'physical', 'debuff', 'damage reduction'}, symbol='')

class ExposeWeakness(Effect):
    def __init__(self, duration) -> None:
        super().__init__(name="Expose Weakness", duration = duration, take_bonus_damage_percent=.05, category={'vulnerable', 'expose weakness', 'physical', 'debuff'}, symbol='🥴')

class PoisonVulnerability(Effect):
    def __init__(self, duration) -> None:
        super().__init__(name="Poison Vulnerability", duration = duration, category={'poison', 'vulnerable', 'debuff'}, symbol='🤢')

class MagicVulnerability(Effect):
    def __init__(self) -> None:
        super().__init__(name="Magic Vulnerability", duration = 10, category={'magic', 'magic vulnerability', 'debuff', 'vulnerable', 'magic'}, take_bonus_damage_percent=.10, symbol='🤩')

class FrostResistance(Effect):
    def __init__(self) -> None:
        super().__init__(name="Frost Resistance", duration = 20, category={'resist','frost', 'frost resistance', 'debuff'}, take_bonus_damage_percent=-.10, symbol='🥶')

class FireResistance(Effect):
    def __init__(self) -> None:
        super().__init__(name="Fire Resistance", duration = 20, category={'resist','fire', 'fire resistance', 'debuff'}, take_bonus_damage_percent=-.10, symbol='🥵')