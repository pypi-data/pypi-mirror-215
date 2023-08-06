from supportive_functions import generate_female_name, generate_male_name, generate_surname_less


female_prefix = [
    "aer", "ash", "bri", "cer", "daen", "ela", "for", "gwe", "hel", "iri", "jen", "kal", "lyn",
    "mel", "ny", "oth", "pae", "qua", "rin", "san", "the", "uil", "val", "wyr", "xan", "yen", "zoe"
]

female_suffix = [
    "a", "ah", "ara", "beth", "cia", "dra", "elle", "fira", "ga", "hanna", "ia", "jara", "kara",
    "lyn", "ma", "na", "ora", "phine", "qua", "ra", "selle", "thya", "ura", "vira", "wyn", "ya", "zara"
]

male_prefix = [
    "aeg", "bar", "ben", "bran", "daen", "dav", "edd", "gar", "jaq", "jon", "khal", "lor", "mor", "ned",
    "qua", "rob", "sam", "theon", "tor", "tyr", "vis"
]

male_suffix = [
    "ard", "as", "dor", "en", "erion", "frey", "gar", "gold", "gon", "hard", "is", "jen", "lan", "len",
    "man", "mar", "men", "mond", "nard", "on", "or", "red", "rick", "ros", "sen", "son", "ton", "ton",
    "ver", "win"
]

surname_prefix = [
    "bar", "bel", "black", "bran", "bron", "cor", "dor", "grey", "har", "kar", "lan", "lor", "mor",
    "nor", "red", "rey", "sta", "star", "tar", "thor", "tyr", "var", "vel", "west", "win",
    "ar", "ber", "cad", "con", "dorn", "dur", "fay", "gar", "hol", "jor", "karl", "ly", "mal", "nar",
    "ran", "ren", "san", "sel", "thorn", "ven", "ver", "war", "wil", "ya", "yor", "zor"
]

surname_suffix = [
    "borne", "croft", "dale", "field", "ford", "gate", "helm", "hold", "horn", "keep", "lock",
    "ridge", "rock", "run", "shaw", "stead", "stone", "wall", "water", "well", "wood",
    "ark", "crest", "don", "ford", "glen", "ham", "hart", "holt", "land", "mont", "more", "port",
    "rick", "sage", "shire", "son", "ton", "ville", "ward", "wick", "wood", "worth", "wyn", "yard",
    "zell"
]

female = generate_female_name(female_prefix, female_suffix, min=0, max=2)
male = generate_male_name(male_prefix, male_suffix, min=0, max=2)
surname = generate_surname_less(surname_prefix, surname_suffix)
