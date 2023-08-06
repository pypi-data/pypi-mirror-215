from supportive_functions import generate_female_name, generate_male_name, generate_surname_less


female_prefix = [
    "cer", "cy", "dan", "el", "es", "fi", "gwen", "is", "jil", "ka", "la", "me", "nes", "phi", "que",
    "ri", "sha", "tri", "va", "wen", "xi", "ya", "zel"
]


female_suffix = [
    "a", "anna", "ara", "delle", "ena", "eth", "felle", "ia", "in", "is", "la", "mina", "na", "nara",
    "ne", "neth", "ra", "re", "ri", "selle", "sha", "thel", "tri", "va", "vera", "wyn", "ya", "zara"
]

male_prefix = [
    "al", "ar", "ber", "cor", "dan", "ed", "fer", "gar", "hal", "ian", "jar", "kar", "luc",
    "mar", "nor", "or", "per", "quil", "rad", "ser", "ter", "ul", "val", "wal", "xan", "yar",
    "zan"
]

male_suffix = [
    "an", "ard", "en", "er", "ian", "ion", "is", "ix", "le", "lin", "mir", "on", "or", "rick",
    "ton", "us", "ven", "ver", "wick", "win", "xander", "yen", "yson", "zeb", "zen"
]


surname_prefix = [
    "ber", "car", "dor", "ev", "fal", "ger", "han", "iar", "jor", "kal", "lin", "mor", "nar",
    "oer", "per", "qar", "ran", "sar", "tor", "ud", "var", "wer", "xan", "yor", "zar"
]

# Harry Potter-based surname suffixes
surname_suffix = [
    "dith", "elle", "fain", "gwen", "hild", "is", "jenn", "kath", "lith", "min", "na", "orin",
    "phine", "quil", "rin", "sael", "thel", "uin", "veth", "wyn", "xel", "yra", "zire"
]

female = generate_female_name(female_prefix, female_suffix, min=1, max=1)
male = generate_male_name(male_prefix, male_suffix, min=1, max=1)
surname = generate_surname_less(surname_prefix, surname_suffix)
