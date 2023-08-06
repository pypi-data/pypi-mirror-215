from .supportive_functions import generate_female_name, generate_male_name, generate_surname_less


female_prefix = [
    "aisha", "amal", "asra", "bahia", "dalila", "esma", "fadia", "ghada", "hala", "jalila",
    "kamila", "laila", "maha", "nadia", "omaira", "rabia", "sabah", "tamara", "yasmin", "zahra"
]

female_suffix = [
    "a", "ah", "at", "aya", "een", "ela", "ena", "era", "eya", "ia", "ida", "ina", "ira", "iya",
    "iyya", "iya", "iya", "iza", "ra", "ya"
]

male_prefix = [
    "ab", "ad", "ah", "al", "am", "an", "ar", "as", "az", "bah", "dal", "fah", "gha", "hab", "hak",
    "han", "has", "hay", "ibn", "id", "is", "ja", "kal", "kar", "kas", "lab", "mal", "mar", "nas",
    "rab", "rah", "sal", "sam", "sar", "sha", "tab", "tal", "tar", "yah", "yas", "zah", "zay"
]

male_suffix = [
    "ad", "ah", "al", "am", "an", "ar", "as", "at", "ay", "az", "dil", "din", "eem", "el", "en",
    "es", "ey", "id", "il", "im", "in", "ir", "is", "it", "iy", "iz", "lil", "mal", "mil", "min",
    "mir", "nir", "or", "os", "ur", "us", "ut", "uz"
]

surname_prefix =  [
    "abd", "al", "am", "an", "ar", "ash", "asim", "az", "bah", "dal", "fah", "ghal", "ham", "has", 
    "ibn", "jah", "kal", "kas", "mah", "naj", "qas", "ram", "saf", "sal", "sam", "tah", "zar"
]

surname_suffix = [
    "a", "ah", "at", "ay", "een", "i", "ia", "id", "il", "im", "ir", "is", "iy", "iyah", "ullah", 
    "ulah", "ur", "us", "ush", "yah", "yid", "yim", "yin"
]

female = generate_female_name(female_prefix, female_suffix, min=0, max=1)
male = generate_male_name(male_prefix, male_suffix, min=0, max=1)
surname = generate_surname_less(surname_prefix, surname_suffix)