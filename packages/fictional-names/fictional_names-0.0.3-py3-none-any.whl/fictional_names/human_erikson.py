from supportive_functions import generate_female_name, generate_male_name, generate_surname


female_suffix = [
    "a", "bel", "cia", "da", "el", "fae", "gwyn", "hia", "i", "ja", "ka", "la", "ma", "na", "ora", "pa",
    "qua", "ra", "sa", "ta", "ula", "va", "wa", "xa", "ya", "za",
    "belle", "cey", "dine", "elle", "finn", "grace", "hira", "ira", "jade", "kara", "lynn", "mara", "nora",
    "opal", "phina", "quella", "rina", "sera", "tia", "una", "vella", "wren", "xina", "yara", "zara"
]

male_prefix = [
    "ach", "an", "ar", "bal", "be", "bel", "bran", "cal", "cor", "dar", "de", "del", "dra", "er",
    "fis", "gal", "gar", "ha", "he", "hir", "il", "ja", "kel", "kor", "lar", "le", "li", "ma", "mar",
    "na", "nor", "ol", "on", "pa", "pel", "per", "qua", "ra", "ran", "rel", "ro", "sa", "sar", "sel",
    "tar", "te", "ti", "to", "ur", "va", "var", "vel", "ver", "wa", "wal", "ya", "yar", "zel"
]

male_suffix = [
    "ad", "al", "an", "ar", "as", "av", "don", "dor", "el", "en", "er", "es", "gan", "har", "hor",
    "ian", "ic", "id", "il", "in", "is", "kan", "kar", "kas", "lak", "las", "lin", "lon", "mar", "mon",
    "nan", "nar", "nas", "non", "or", "rad", "ran", "ras", "rik", "ron", "sal", "san", "tas", "tar",
    "tin", "ton", "ur", "us", "van", "var", "ver", "von", "war", "won", "yas", "zan", "zen", "zon"
]

female_prefix = [
    "acht", "bry", "cali", "dara", "ell", "fay", "gwen", "hela", "is", "jen", "kala", "lara", "morga",
    "nala", "orla", "pae", "quen", "rae", "sab", "tara", "ulan", "vay", "wyn", "xan", "yara", "zara",
    "bel", "cara", "dela", "ella", "fin", "grace", "hira", "ira", "jenna", "kira", "luna", "maia", "nira",
    "opal", "pippa", "quela", "rona", "saffron", "tessa", "ula", "vanna", "willa", "xara", "yuna", "zella"
]

surname_syllables =  [
    'al', 'an', 'ar', 'ark', 'as', 'ash', 'ba', 'bar', 'be', 'bel', 'car', 'cas', 'cor','da', 'dal', 'dar',
    'de', 'del', 'di', 'don', 'dor', 'el', 'en', 'er', 'es', 'fal', 'far', 'fi', 'gal', 'gar', 'har', 'ho',
    'ian', 'ik', 'il', 'in', 'is', 'ja', 'jar', 'kal', 'kar', 'kas', 'ken', 'kor', 'lar', 'li', 'lon', 'ma',
    'mal', 'mar', 'mas', 'mon', 'na', 'nal', 'nar', 'ni', 'no', 'on', 'or', 'pa', 'par', 'per', 'qu', 'ra',
    'ral', 'ran', 'ri', 'ril', 'ro', 'ron', 'sa', 'sal', 'sha', 'si', 'st', 'ta', 'tar', 'th', 'thal', 'thar',
    'thon', 'ti', 'tin', 'tor', 'un', 'ur', 'va', 'val', 'var', 'ver', 'von', 'wan', 'war', 'wen', 'win', 'ya',
    'yar', 'yen', 'yin', 'yor', 'za', 'zan', 'zar'
]


female = generate_female_name(female_prefix, female_suffix, min=0, max=2)
male = generate_male_name(male_prefix, male_suffix, min=0, max=2)
surname = generate_surname(surname_syllables, min=2, max=3)