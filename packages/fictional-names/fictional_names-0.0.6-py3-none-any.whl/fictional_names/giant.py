from .supportive_functions import generate_female_name, generate_male_name, generate_surname_less


female_prefix = [
    "ar", "bal", "bar", "bran", "dar", "dran", "feth", "gras", "har", "jaf", "kar", "krul",
    "mar", "nar", "par", "rak", "ras", "sar", "tar", "thas", "thul", "war", "yas", "zar"
]


female_suffix = [
    "a", "ah", "al", "an", "ar", "ara", "as", "ath", "aun", "aya", "az", "da", "dal", "dan",
    "dar", "de", "del", "din", "dra", "du", "dul", "e", "eh", "el", "en", "er", "eth", "i",
    "ia", "il", "in", "ir", "is", "ish", "ith", "l", "la", "le", "lin", "ma", "mal", "man",
    "mar", "na", "nah", "nal", "nan", "ne", "neh", "nir", "ra", "rah", "ral", "ran", "re",
    "reh", "ri", "rin", "sa", "sal", "san", "se", "sel", "sha", "shal", "shan", "she", "shen",
    "si", "sin", "ta", "tal", "tan", "te", "tel", "ti", "tin", "va", "val", "van", "ve", "vel",
    "vi", "vin", "ya", "yah", "yal", "yan", "ye", "yel", "yi", "yin", "za", "zal", "zan", "ze",
    "zel", "zi", "zin"
]

male_prefix = [
    "ba", "bal", "bek", "bo", "bor", "bro", "dar", "del", "dra", "en", "er", "far", "fel", "gol",
    "gra", "ha", "har", "ho", "hor", "kar", "kel", "kor", "ku", "kur", "lar", "lek", "lok", "ma",
    "mar", "mo", "mor", "nar", "nel", "nor", "o", "or", "ra", "ran", "ro", "ron", "sa", "sar",
    "so", "sor", "ta", "tar", "to", "tor", "ur", "us", "va", "var", "vo", "vor"
]

male_suffix = [
    "ak", "ar", "ek", "el", "en", "er", "ik", "ir", "is", "ith", "ok", "or", "os", "oth", "uk",
    "ul", "un", "ur", "us", "uth", "yk", "yr", "ys"
]


surname_prefix = [
    "an", "bak", "blak", "bol", "bran", "bruk", "dar", "del", "dor", "erik", "fel", "gol", "grak",
    "gul", "har", "hel", "hor", "jor", "kar", "kel", "kha", "kol", "kor", "krul", "kul", "lar",
    "lek", "mor", "mur", "nal", "nul", "phel", "por", "rak", "ruk", "sar", "sel", "sol", "tar",
    "tel", "thel", "tol", "tor", "ul", "vak", "val", "var", "ver", "vol", "vor", "wol", "yor", "zol"
]

# Harry Potter-based surname suffixes
surname_suffix = [
    "aak", "ak", "an", "ar", "ek", "en", "er", "ik", "in", "ir", "ok", "on", "ong", "or", "uk", "un", "ur"
]

female = generate_female_name(female_prefix, female_suffix, min=0, max=1)
male = generate_male_name(male_prefix, male_suffix, min=0, max=1)
surname = generate_surname_less(surname_prefix, surname_suffix)
