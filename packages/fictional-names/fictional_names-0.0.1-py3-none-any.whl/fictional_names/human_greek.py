from random import choice
from supportive_functions import generate_female_name, generate_male_name


female_prefix = [
    "agá", "aléx", "amphí", "aná", "arí", "athén", "démé", "élektr", "eurydí", "euthén", "galát",
    "harmón", "hébé", "hér", "kalí", "kleió", "kyprí", "lét", "méliss", "nér", "orestí", "pandór",
    "penél", "perí", "philómél", "pó", "thál", "théod", "xén"
]
female_suffix = [
    "a", "anthe", "dóra", "eia", "éne", "essa", "ia", "idóra", "ika", "inia", "ipé", "ithéa", "íne",
    "ita", "oé", "óra", "otea", "óti", "oula", "phén", "phíne", "phrón", "séa", "théa", "théne",
    "tía", "tra", "tía", "ydia"
]

male_prefix = [
    'aeg', 'aer', 'alex', 'amph', 'an', 'anat', 'and', 'ant', 'arch', 'arist', 'astr', 'calli', 'chr',
    'chrys', 'cle', 'cyr', 'dam', 'dem', 'dion', 'eir', 'eugen', 'euph', 'her', 'herm', 'hip', 'hipp',
    'kal', 'klei', 'leon', 'lys', 'megas', 'myr', 'neo', 'nik', 'olym', 'pan', 'per', 'phil', 'pho',
    'pol', 'pyth', 'soph', 'theo', 'theod', 'xan', 'xen', 'zen'
]

male_suffix = [
    'ades', 'ander', 'archos', 'as', 'asios', 'ax', 'axos', 'eides', 'enios', 'eochos', 'eokles', 'eon',
    'eris', 'es', 'ias', 'ides', 'ikles', 'ion', 'ios', 'is', 'kleis', 'kles', 'kriti', 'lon', 'lykos',
    'medes', 'mon', 'mos', 'on', 'or', 'oris', 'os', 'otes', 'otis', 'ox', 'oxenos', 'oxis', 'pheles',
    'phoros', 'ptolemeos', 'rakles', 'ros', 'ruthios', 'sthenes', 'stratos', 'teles', 'tides', 'tor',
    'us', 'xander', 'xandros', 'xenos', 'xion', 'xiphos', 'ylos', 'zenos'
]

surnames = [
    "the Wise", "the Philosopher", "the Brave", "the Just", "the Noble", "the Bold", "the Merciful",
    "the Pious", "the Virtuous", "the Fierce", "the Strong", "the Loyal", "the Courageous", "the Valiant",
    "the Resolute", "the Magnificent", "the Majestic", "the Tranquil", "the Radiant", "the Serene",
    "the Wise", "the Enlightened", "the Gifted", "the Brilliant", "the Learned", "the Scholar",
    "the Thoughtful", "the Humble", "the Modest", "the Generous", "the Gracious", "the Benevolent",
    "the Compassionate", "the Kind", "the Gentle", "the Peaceful", "the Serene", "the Harmonious",
    "the Charismatic", "the Charming", "the Enigmatic", "the Joyful", "the Optimistic", "the Cheerful",
    "the Melancholy", "the Mysterious", "the Witty", "the Clever", "the Skilled", "the Agile",
    "the Swift", "the Resilient", "the Tenacious", "the Wise", "the Visionary", "the Inventive",
    "the Curious", "the Diligent", "the Persevering", "the Resourceful", "the Ambitious", "the Daring",
    "the Fearless", "the Audacious", "the Intrepid", "the Majestic", "the Regal", "the Commanding",
    "the Supreme", "the Exalted", "the Sovereign", "the Mighty", "the Unyielding", "the Victorious",
    "the Glorious", "the Triumphant", "the Magnanimous", "the Golden", "the Divine", "the Eternal",
    "the Everlasting", "the Radiant", "the Splendid", "the Enchanting", "the Eloquent", "the Graceful",
    "the Elegant", "the Stalwart", "the Sturdy", "the Honorable", "the Devoted", "the Revered",
    "the Heroic", "the Legendary", "the Illustrious", "the Renowned", "the Celebrated", "the Great",
    "the Grand", "the Mighty", "the Colossal", "the Monumental", "the Monumentous", "the Illustrious",
    "the Eminent", "the Venerable",
]

female = generate_female_name(female_prefix, female_suffix, min=1, max=1)
male = generate_male_name(male_prefix, male_suffix, min=1, max=1)
surname = choice(surnames)
