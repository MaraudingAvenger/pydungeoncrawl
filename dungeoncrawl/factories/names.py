import string
import re
import random

import faker


class NameFactory:
    def __init__(self) -> None:
        self.fake = faker.Faker()
        self._vowels = "aeiouy"
        self._consonants = re.sub(
            f"[{self._vowels}]", "", string.ascii_lowercase)

        self._next_letters = {
            l: ""
            for l in string.ascii_lowercase
        }
        for l in self._vowels:
            self._next_letters[l] += self._consonants + \
                re.sub(l, "", self._vowels)
        for l in self._consonants:
            self._next_letters[l] += self._vowels
            if l not in 'chjkvwx':
                self._next_letters[l] += l
        self._next_letters['c'] += 'hr'
        self._next_letters['t'] += 'hr'
        self._next_letters['q'] = 'u'

    def get_true_random_name(self, length: int = 5, starting_letters: str | None = None) -> str:
        '''
        Get truly random name with no real analog. Follows some pronounciation rules.
        Optionally, specify a `length` (default 5) and/or a string `starting_letters` you would like
        the resulting name to begin with.
        '''
        name = ""
        letter = starting_letters.lower() if starting_letters else random.choice(
            string.ascii_lowercase)
        while len(name)+len(starting_letters or "") < length:
            name += letter
            if random.random() > 0.92:
                name += "'"
            letter = random.choice(self._next_letters[letter[-1]])
        name += letter
        return name.capitalize()

    def get_name(self, name: str = ""):
        """
        Get a name that begins with a random 'real' name.
        Optionally, provide a `name` string to be used as the base 'real' name.
        """
        name = name.lower() if not name else self.fake.last_name().lower()

        v = list(self._vowels)
        for vowel in v:
            name = name.replace(vowel, v.pop(v.index(random.choice(v))))

        mapper = {
            'b': 'byd',
            'g': 'gal',
            'r': 'lleyn',
            'z': 'xor',
            'y': "'yth",
            'p': "lleth",
            'ph': 'dd',
            'k': 'ek',
            'l': 'ol',
            'j': 'ye'
        }

        m = list(mapper.items())

        # adjust the range to do more replaces on the name string
        for letter, repl in [m.pop(m.index(random.choice(m))) for _ in range(4)]:
            name = name.replace(letter, repl)

        # This makes the name more pronouncable; it replaces doubled letters.
        for letter in 'iuyxpb':
            name = re.sub(f'{letter}+', letter, name)
        return name.title()
