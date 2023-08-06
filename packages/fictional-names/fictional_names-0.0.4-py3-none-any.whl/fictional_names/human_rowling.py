from .supportive_functions import generate_female_name, generate_male_name, generate_surname_less


female_prefix = [
    "ada", "al", "am", "an", "bel", "beth", "ca", "ce", "cha", "da", "de", "dra", "ela", "el", "ema",
    "en", "fa", "fay", "ga", "ge", "gi", "ha", "he", "hi", "ila", "il", "ima", "in", "ja", "je", "ka",
    "ke", "ki", "la", "le", "li", "ma", "me", "mi", "na", "ne", "ni", "ola", "ol", "oma", "pa", "pe",
    "pi", "qua", "ra", "re", "ri", "sa", "se", "sha", "ta", "te", "tha", "u", "va", "ve", "vi", "wa",
    "we", "wi", "ya", "ye", "yi", "za", "ze", "zi"
]

female_suffix = [
    "a", "ana", "ara", "beth", "ca", "cel", "cia", "da", "dora", "e", "ella", "fa", "fay", "ga", "gine",
    "ha", "hilda", "ia", "ina", "ira", "la", "lina", "lissa", "ma", "mia", "na", "ne", "nia", "nissa",
    "ola", "ona", "ora", "pa", "pia", "ra", "ria", "rina", "sa", "sina", "sta", "ta", "tia", "trina",
    "va", "via", "vina", "wa", "wena", "wilda", "ya", "yna", "yra", "za", "zia", "zina"
]

male_prefix = [
    "al", "ar", "ben", "cor", "dan", "el", "fin", "gar", "hir", "ian", "jam", "kil", "lin",
    "mor", "nix", "or", "per", "quin", "ron", "sam", "ter", "ul", "ver", "wes", "xan", "yor",
    "zach"
]

male_suffix = [
    "ald", "bert", "cor", "dard", "el", "finn", "gald", "hart", "ian", "jack", "kyle", "land",
    "mack", "nald", "orin", "paul", "quin", "rick", "sam", "tin", "ulph", "vald", "wick", "xander",
    "yor", "zeph"
]

surname_prefix = [
    'amber', 'ash', 'beech', 'birch', 'black', 'bramble', 'bright', 'cedar', 'cypress','dark', 'ebony',
    'ember', 'fern', 'fire', 'glen', 'gold', 'hallow', 'hazel', 'holly', 'ivy', 'juniper', 'larch',
    'maple', 'moon', 'noble', 'oak', 'pine', 'proud', 'raven', 'rowan', 'sequoia', 'shadow', 'silver',
    'snow', 'spruce', 'star', 'stone', 'storm', 'swift', 'thistle', 'thorn', 'violet', 'willow', 'yew'
]

# Harry Potter-based surname suffixes
surname_suffix = [
    'ash', 'blaze', 'blossom', 'branch', 'breeze', 'brook', 'dawn', 'dusk', 'fall', 'feather', 'flame',
    'forest', 'glade', 'glimmer', 'glimpse', 'gust', 'heart', 'leaf', 'light', 'mist', 'moon', 'petal',
    'quill', 'ray', 'rose', 'shade', 'shimmer', 'song', 'spell', 'star', 'sun', 'thorn', 'twilight',
    'vale', 'whisper', 'wind', 'wisp', 'wood', 'wraith', 'wren'
]

female = generate_female_name(female_prefix, female_suffix, min=0, max=1)
male = generate_male_name(male_prefix, male_suffix, min=0, max=1)
surname = generate_surname_less(surname_prefix, surname_suffix)
