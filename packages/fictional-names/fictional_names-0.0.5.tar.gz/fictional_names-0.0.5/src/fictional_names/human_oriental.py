from .supportive_functions import generate_female_name, generate_male_name, generate_surname_less


female_prefix = [
    "ai", "an", "bo", "chi", "da", "en", "fu", "go", "ha", "hi", "i", "ka", "ko", "mi", "na",
    "no", "ra", "ri", "sa", "shi", "ta", "to", "tsu", "u", "ya", "yo", "zu"
]

female_suffix = [
    "a", "aki", "ami", "aya", "chi", "e", "emi", "hana", "i", "iko", "ka", "kami", "ko", "mi",
    "miko", "na", "nami", "no", "omi", "ra", "ri", "saki", "shi", "ta", "to", "tsuki", "u", "ya",
    "yo"
]

male_prefix = [
    "ai", "ben", "chan", "da", "en", "fu", "gen", "hai", "ich", "ji", "ken", "li", "ming",
    "nao", "ori", "po", "qing", "ren", "shen", "tai", "ui", "vui", "wen", "xi", "ya", "zen"
]

male_suffix = [
    "bo", "chi", "do", "en", "fu", "gi", "hiro", "i", "ji", "ko", "lei", "ming", "no", "ou",
    "po", "quan", "rong", "shi", "to", "ui", "vui", "wen", "xi", "yo", "zen"
]

surname_prefix =  [
    "chin", "da", "fu", "guan", "han", "jing", "li", "mei", "ning", "qian", "rong", "shen", "ting",
    "wan", "xi", "yan", "zhi"
]

surname_suffix = [
    "bai", "chun", "feng", "hua", "ji", "lan", "mei", "nan", "ping", "qi", "rong", "shu", "ting",
    "wen", "xi", "yan", "ying", "zhi"
]
female = generate_female_name(female_prefix, female_suffix, min=1, max=2)
male = generate_male_name(male_prefix, male_suffix, min=1, max=1)
surname = generate_surname_less(surname_prefix, surname_suffix)