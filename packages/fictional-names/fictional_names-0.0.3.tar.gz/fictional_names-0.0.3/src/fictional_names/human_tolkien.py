from supportive_functions import generate_female_name, generate_male_name, generate_surname_less


male_prefix = [
    "aer", "ald", "an", "ar", "bar", "bor", "cal", "dal", "dan", "dur", "ed", "eld", "er", "fal",
    "fin", "gal", "gan", "gar", "had", "hal", "ian", "in", "kar", "kor", "lanc", "mar", "mer",
    "nor", "or", "rad", "ran", "ron", "sar", "sol", "tan", "thor", "tor", "ul", "val", "van",
    "vor", "wal", "war", "yor", "zar"
]

male_suffix = [
    "ald", "an", "ar", "ard", "bar", "dan", "dor", "dred", "dur", "fin", "gald", "gan", "gar",
    "hard", "horn", "ian", "ion", "lan", "mir", "nard", "or", "rad", "ran", "ric", "rin", "ron",
    "thor", "thorn", "und", "val", "var", "ward", "win", "wood", "wyn", "yar"
]

female_prefix = [
    "ad", "al", "an", "ar", "bel", "ca", "cel", "da", "di", "el", "en", "fa", "fay", "gal",
    "gi", "ha", "hel", "il", "in", "ja", "kel", "la", "le", "ma", "mi", "na", "ni", "ol",
    "pe", "qui", "ra", "re", "sa", "se", "ta", "thi", "va", "ve", "wil", "ya", "ze"
]

female_suffix = [
    "a", "ana", "ara", "beth", "cia", "da", "dea", "elle", "fa", "ga", "hilda", "ia", "iana",
    "ida", "ira", "la", "lia", "lina", "ma", "mia", "na", "nelle", "nia", "ra", "ria", "sa",
    "sia", "ta", "thea", "thia", "va", "via", "ya"
]

surname_prefix = [
    "ald", "arn", "bar", "ber", "brand", "carr", "cor", "dun", "eag", "eld", "fair", "gar", "gold",
    "han", "haw", "helm", "kings", "long", "oak", "rav", "red", "river", "rock", "silver", "stone",
    "thorn", "west", "white", "wind", "wynd", "yar", "zel", "al", "an", "ark", "ash", "ba",
    "bor", "be", "bel", "car", "cas", "cor", "dar", "de", "del", "di", "dor", "el", "er", "fal",
]

surname_suffix = [
    "bourne", "bridge", "brook", "castle", "field", "ford", "ham", "hurst", "lake", "ley", "mead",
    "mill", "shire", "stead", "stone", "ton", "view", "wall", "ward", "water", "well", "wick", "worth",
    "bay", "crest", "croft", "dale", "gate", "glen", "haven", "hill", "holme", "isle", "keep", "mere",
    "moor", "peak", "pool", "reach", "rise", "shade", "slope", "thorpe", "vale", "village", "weir", "wood",
    "yard", "zeal"
]

female = generate_female_name(female_prefix, female_suffix)
male = generate_male_name(male_prefix, male_suffix)
surname = generate_surname_less(surname_prefix, surname_suffix)
