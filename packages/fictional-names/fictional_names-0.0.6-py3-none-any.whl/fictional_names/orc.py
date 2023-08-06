from random import choice
from .supportive_functions import generate_female_name, generate_male_name


female_prefix = [
    "az", "barg", "bruz", "dolg", "drak", "gash", "ghor", "grish", "groth", "gul", "haz", "karg",
    "krash", "morg", "narg", "naz", "raz", "shag", "shar", "skar", "snag", "snar", "snaz", "thrak",
    "ug", "uruk", "varg", "zarg",
]

female_suffix = [
    "a", "ba", "da", "ga", "gga", "gla", "gra", "gsha", "gza", "ka", "kra", "la", "lga", "lka",
    "lsha", "mga", "mka", "nga", "nka", "nsha", "ra", "rak", "rga", "rka", "rsha", "sa", "sha",
    "ska", "sla", "tka", "tra", "tsha", "uka", "urka", "zga", "zka", "zsha",
]

male_prefix = [
    "az", "bal", "bolg", "dorg", "drak", "grom", "gruk", "gul", "karg", "kru", "laz", "log", "mog", 
    "mok", "narg", "nok", "org", "rag", "rak", "shag", "shar", "skar", "skul", "snag", "snok", "thok",
    "thug", "thrak", "ug", "urk", "yaz", "yur",
]

male_suffix = [
    "dak", "dor", "gol", "grom", "gul", "karg", "krak", "kul", "lurk", "mok", "nak", "nok", "rag", 
    "rak", "shak", "shok", "skar", "skul", "snik", "snok", "thak", "thok", "thug", "urk", "warg", 
    "yak", "yuk", "zog",
]

surnames = [
    'the Annihilator', 'the Ashmaker', 'the Axe', 'the Bane', 'the Blackhand', 'the Blade', 'the Blight',
    'the Bloodbane', 'the Bloodfang', 'the Bloodscourge', 'the Bloodthirsty', 'the Bone', 'the Bonecrusher',
    'the Brutal', 'the Brute', 'the Butcher', 'the Conqueror', 'the Corpsemaker', 'the Crazed', 'the Crusher',
    'the Darkblade', 'the Darkheart', 'the Deathbringer', 'the Deathdealer', 'the Deathgaze', 'the Deathgrip',
    'the Deathmask', 'the Desecrator', 'the Desolation', 'the Despair', 'the Despoiler', 'the Destroyer',
    'the Devourer', 'the Dismemberer', 'the Doom', 'the Doombringer', 'the Doomclaw', 'the Doomgaze',
    'the Doomhammer', 'the Fearmonger', 'the Fierce', 'the Fleshrend', 'the Gloom', 'the Gloomfang', 'the Gorefist',
    'the Gorehowl', 'the Gravewalker', 'the Grim', 'the Grimdark', 'the Grimface', 'the Grimjaw', 'the Grimskull',
    'the Gruesome', 'the Gutslicer', 'the Harbinger', 'the Hellraiser', 'the Horned', 'the Howler', 'the Impaler',
    'the Inferno', 'the Ironfist', 'the Ironhide', 'the Marauder', 'the Maul', 'the Mauler', 'the Merciless',
    'the Mocker', 'the Nightstalker', 'the Pestilence', 'the Pitiless', 'the Plaguebringer', 'the Plunderer', 'the Rage',
    'the Rager', 'the Rampage', 'the Ravager', 'the Rend', 'the Ruin', 'the Ruiner', 'the Ruthless', 'the Savage',
    'the Scar', 'the Scarface', 'the Scourge', 'the Scrapper', 'the Shadow', 'the Shadowhand', 'the Shatterer',
    'the Sinister', 'the Skull', 'the Skullcrusher', 'the Skullsplitter', 'the Slasher', 'the Slaughterer', 'the Slayer',
    'the Sludge', 'the Smasher', 'the Snarler', 'the Spinebreaker', 'the Spite', 'the Stalker', 'the Swiftblade',
    'the Throatripper', 'the Tormentor', 'the Torturer', 'the Venom', 'the Venomfang', 'the Vex', 'the Vicious',
    'the Vile', 'the Warbringer', 'the Warcry', 'the Warg', 'the Warlord', 'the Wicked', 'the Wound', 'the Wrecking Ball'
]

female = generate_female_name(female_prefix, female_suffix, min=0, max=1)
male = generate_male_name(male_prefix, male_suffix, min=0, max=1)
surname = choice(surnames)
