from .supportive_functions import generate_female_name, generate_male_name, generate_surname_less


female_prefix = [
    "ber", "bri", "cla", "cor", "dal", "dor", "el", "fro", "gol", "har", "hil", "lav", "lil", "lo",
    "mar", "mel", "nar", "nor", "ol", "per", "pip", "ro", "sam", "san", "syl", "tas", "wil",
]

female_suffix = [
    "a", "adoc", "ald", "bella", "belle", "dora", "ella", "elle", "freda", "gwen", "la", "lea",
    "lina", "lla", "lotta", "ma", "mia", "mina", "mira", "na", "nelle", "nna", "ra", "ri", "ria",
    "rie", "rina", "sa", "sella", "sie", "sy", "ta", "tina", "wyn",
]

male_prefix = [
    "albo", "bal", "bil", "bran", "con", "dodo", "ever", "fal", "fer", "fin", "gaf", "gim", "gol",
    "ham", "hob", "las", "leo", "lim", "lobo", "mar", "milo", "mung", "nico", "odo", "olbo", "pal",
    "per", "pim", "pip", "rolo", "ruf", "sam", "silbo", "tob", "ugo", "vigo", "wigo", "wim", "wise",
    "wolbo",
]

male_suffix = [
    "bo", "bri", "do", "dro", "fast", "fer", "gar", "go", "grin", "hard", "lo", "man", "mo", "nac",
    "nard", "nibo", "no", "per", "pin", "po", "ric", "rim", "ro", "san", "sim", "to", "wise",
]

surname_prefix =  [
    "bagg", "bran", "bur", "cra", "cud", "good", "green", "hard", "hay", "hill", "le", "long",
    "merry", "oak", "old", "pere", "pip", "proud", "sack", "small", "tall", "took", "toss",
    "under", "whit",
]

surname_suffix = [
    "bottom", "buckle", "burr", "by", "digger", "foot", "girdle", "hair", "hobb", "ins",
    "kins", "leaf", "man", "over", "pint", "root", "shire", "thistle", "top", "wag", "ward",
    "wheat", "wort", "worthy",
]

female = generate_female_name(female_prefix, female_suffix, min=1, max=1)
male = generate_male_name(male_prefix, male_suffix, min=1, max=1)
surname = generate_surname_less(surname_prefix, surname_suffix)