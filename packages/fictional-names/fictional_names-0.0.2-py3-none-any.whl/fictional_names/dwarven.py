from supportive_functions import generate_female_name, generate_male_name, generate_surname


female_prefix = [
    "bal", "da", "din", "dur", "fal", "gim", "gin", "gor", "hel", "in", "kil", "li", "mha", "na",
    "nin", "ran", "sha", "thor", "tha", "zin"
]

female_suffix = [
    "ǎ", "dǎ", "del", "dûr", "fa", "ga", "gal", "gan", "gard", "hild", "in", "kil", "la", "lda",
    "lin", "ma", "mi", "na", "ra", "ri", "sa", "thi", "thra", "zǎ"
]


male_prefix = [
    "az", "bal", "bor", "da", "dor", "du", "fa", "gar", "gim", "glo", "gra", "grom", "han", "hur",
    "kaz", "kil", "knar", "kri", "lur", "mak", "mor", "nar", "nor", "ri", "rok", "run", "thor",
    "thra", "thu", "ul", "ur", "var", "vōr"
]

male_suffix = [
    "ain", "ǎk", "ar", "bar", "bor", "dain", "dal", "din", "dûr", "fin", "gǎrn", "gar", "gim",
    "gorn", "grim", "gûn", "gûr", "in", "kil", "korn", "li", "lin", "mar", "mir", "nar", "nûr",
    "rik", "rim", "rin", "ron", "rum", "thōr", "thrin", "thûr", "um", "ûr", "var", "zin"
]


surname_syllables = [
    'bar', 'bif', 'bin', 'bor', 'bǎl', 'dal', 'dar', 'dur', 'fal', 'fin', 'gar', 'gim', 'gin', 'gon',
    'gor', 'grim', 'gun', 'gur', 'har', 'kar', 'kaz', 'khaz', 'kil', 'kin', 'kram', 'kōr', 'lok',
    'lor', 'mag', 'mak', 'mar', 'mir', 'mur', 'nar', 'nim', 'nor', 'nûr', 'rag', 'rig', 'rik', 'rim',
    'ror', 'rum', 'tar', 'thar', 'thor', 'thrak', 'thran', 'thrur', 'tor', 'tur', 'ur', 'vol', 'vor'
]

female = generate_female_name(female_prefix, female_suffix, min=1, max=2)
male = generate_male_name(male_prefix, male_suffix, min=0, max=1)
surname = generate_surname(surname_syllables)
