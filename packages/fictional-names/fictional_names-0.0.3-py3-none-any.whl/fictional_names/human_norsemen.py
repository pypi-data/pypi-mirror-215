from supportive_functions import generate_female_name, generate_male_name, generate_surname_less


female_prefix = [
    "aða", "æl", "arn", "björn", "dís", "eið", "ey", "fríð", "gud", "gull", "gyð", "hild", "hjör",
    "ing", "líf", "run", "sif", "skjald", "skuld", "sól", "thor", "val", "víg", "ygg"
]

female_suffix = [
    "björg", "dóttir", "ey", "fey", "fríða", "gärd", "gyða", "hild", "hjör", "inga", "lína", "runa",
    "sigríð", "skjöld", "skuld", "sól", "thor", "vald", "ví", "vig", "ygg"
]

male_prefix = [
    "að", "al", "arn", "ask", "bað", "bjǫrn", "dǫrr", "eir", "ein", "fjǫr", "geir", "grim", "gunn",
    "hǫrð", "ing", "jarl", "kárr", "kol", "leifr", "mǫrk", "njal", "od", "ǫrn", "rauð", "skǫgr",
    "steinn", "tórr", "úlfr", "vald", "víð", "yng"
]

male_suffix = [
    "arr", "bjǫrn", "dall", "einarr", "fang", "geir", "grimr", "hǫrðr", "iarr", "jǫrn", "kell",
    "lárr", "mann", "njarð", "olfr", "ráð", "skell", "steinn", "thórr", "ulf", "valdr", "víðr",
    "yrn"
]

surname_prefix =  [
    "aeg", "aer", "arn", "as", "baer", "ber", "bjorn", "daeg", "dagr", "ein", "eir", "ey", "freyr",
    "gar", "geir", "grim", "haeg", "haer", "haf", "hald", "har", "hjor", "kjaer", "leifr", "mund",
    "raed", "raeg", "ran", "saer", "sig", "skjold", "staf", "stein", "svein", "thaeg", "thor", "tor",
    "ulfr", "vaeg", "vaer", "vald", "veig", "ver", "vid", "vigr", "vind", "yng"
]

surname_suffix = [
    "ard", "bjorn", "brand", "dal", "dottir", "drifa", "drot", "eidr", "fast", "fjord", "flod",
    "frej", "gard", "gils", "haugr", "heim", "hildr", "holt", "ing", "jord", "kjold", "lind", "magn",
    "nord", "rafn", "rak", "rik", "sif", "skar", "son", "stein", "stir", "thor", "tor", "ulf", "vald",
    "vang", "ve", "vig", "vin", "vir", "vor", "yng", "yv"
]

female = generate_female_name(female_prefix, female_suffix, min=0, max=1)
male = generate_male_name(male_prefix, male_suffix, min=0, max=1)
surname = generate_surname_less(surname_prefix, surname_suffix)