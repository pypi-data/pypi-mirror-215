from .supportive_functions import generate_female_name, generate_male_name, generate_surname


female_prefix = [
    "ael", "al", "an", "ar", "cal", "dael", "el", "er", "fae", "fal", "fi", "gal", "gil", "glor",
    "hal", "ia", "id", "il", "im", "in", "laer", "lan", "leg", "li", "lind", "lith", "lor", "mae",
    "mel", "na", "nar", "nen", "ner", "or", "pe", "ran", "rhov", "sae", "saer", "se", "sil", "ta",
    "thal", "thar", "thing", "ti", "tir", "val", "ví", "yar", "zeph", "zim"
]

female_suffix = [
    "á", "ë", "í", "ír", "ís", "ith", "lá", "lé", "liël", "lís", "lith", "lyn", "má", "më", "mí",
    "ná", "në", "niël", "nis", "nith", "nyá", "rá", "ré", "riël", "ris", "rith", "ryá", "sä", "së",
    "siél", "sis", "sith", "stá", "thél", "theá", "thée", "thiël", "this", "thith", "vyl", "wén",
    "wiel", "wis", "withë", "yá", "yë", "yra", "ysë"
]

male_prefix = [
    "aeg", "aer", "am", "an", "ar", "bar", "ber", "cal", "cel", "cor", "dan", "dar", "den",
    "dor", "el", "em", "en", "er", "fal", "fer", "gal", "gar", "gil", "glor", "hal", "har",
    "hel", "her", "iath", "im", "in", "ir", "lam", "lar", "len", "lin", "lor", "mel", "men",
    "mir", "nem", "ner", "nim", "nor", "ol", "or", "rad", "ral", "ran", "rel", "rim", "ron",
    "sam", "san", "ser", "sil", "sin", "sor", "tan", "tar", "tel", "thor", "tom", "tor", "ul",
    "ur", "val", "var", "vén", "ver", "wil", "win", "wis", "yam", "yar", "ÿer", "yin", "yol"
]

male_suffix = [
    "ad", "aél", "an", "and", "ar", "ard", "as", "ath", "énd", "ër", "ern", "eth", "il", "in",
    "ind", "ion", "ir", "is", "ith", "lad", "läs", "lin", "lo", "lon", "or", "orn", "os", "rad",
    "rän", "ras", "rath", "rin", "ron", "ros", "rth", "th", "thir", "thor", "únd", "úr", "us",
    "win", "ynd", "yon", "ÿth"
]

surname_syllables = [
    "ael", "al", "an", "ar", "cal", "dael", "ël", "er", "fae", "fal", "fi", "gal", "gil", "glor",
    "hal", "ia", "id", "il", "im", "in", "laér", "lan", "leg", "li", "lind", "lith", "lor", "mae",
    "mel", "ne", "ner", "nén", "ner", "or", "pe", "ran", "rhöv", "sae", "sae", "se", "sil", "ta",
    "thal", "thar", "thing", "ti", "tir", "val", "vi", "yar", "zah", "zim"
]

female = generate_female_name(female_prefix, female_suffix, min=1, max=1)
male = generate_male_name(male_prefix, male_suffix, min=1, max=1)
surname = generate_surname(surname_syllables, min=2, max=3)
