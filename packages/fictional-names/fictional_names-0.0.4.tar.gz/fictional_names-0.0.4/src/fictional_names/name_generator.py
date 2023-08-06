from . import dwarven, elven, giant, halfling, orc, human_steampunk, human_modern, human_medieval, human_greek, human_norsemen, human_arab, human_oriental, human_tolkien, human_jordan, human_erikson, human_rowling, human_sapkowski


def generate_name(gender='male', style='modern'):
    if gender.lower() == 'male':
        match style:
            case 'elven':
                name = elven.male
            case 'dwarven':
                name = dwarven.male
            case 'giant':
                name = giant.male
            case 'halfling':
                name = halfling.male
            case 'orc':
                name = orc.male
            case 'modern':
                name = human_modern.male
            case 'greek':
                name = human_greek.male
            case 'norsemen':
                name = human_norsemen.male
            case 'arab':
                name = human_arab.male
            case 'oriental':
                name = human_oriental.male
            case 'steampunk':
                name = human_steampunk.male
            case 'medieval':
                name = human_medieval.male
            case 'tolkien':
                name = human_tolkien.male
            case 'jordan':
                name = human_jordan.male
            case 'erikson':
                name = human_erikson.male
            case 'rowling':
                name = human_rowling.male
            case 'sapkowski':
                name = human_sapkowski.male
    elif gender.lower() == 'female':
        match style:
            case 'elven':
                name = elven.female
            case 'dwarven':
                name = dwarven.female
            case 'giant':
                name = giant.female
            case 'halfling':
                name = halfling.female
            case 'orc':
                name = orc.female
            case 'modern':
                name = human_modern.female
            case 'greek':
                name = human_greek.female
            case 'norsemen':
                name = human_norsemen.female
            case 'arab':
                name = human_arab.female
            case 'oriental':
                name = human_oriental.female
            case 'steampunk':
                name = human_steampunk.female
            case 'medieval':
                name = human_medieval.female
            case 'tolkien':
                name = human_tolkien.female
            case 'jordan':
                name = human_jordan.female
            case 'erikson':
                name = human_erikson.female
            case 'rowling':
                name = human_rowling.female
            case 'sapkowski':
                name = human_sapkowski.female
            
    else:
        raise ValueError("Invalid gender specified. Please choose 'male' or 'female'.")
    
    if style.lower() == 'elven':
        surname = elven.surname
    elif style.lower() == 'dwarven':
        surname = dwarven.surname
    elif style.lower() == 'giant':
        surname = giant.surname
    elif style.lower() == 'halfling':
        surname = halfling.surname
    elif style.lower() == 'orc':
        surname = orc.surname
    elif style.lower() == 'modern':
        surname = human_modern.surname
    elif style.lower() == 'greek':
        surname = human_greek.surname
    elif style.lower() == 'norsemen':
        surname = human_norsemen.surname
    elif style.lower() == 'arab':
        surname = human_arab.surname
    elif style.lower() == 'oriental':
        surname = human_oriental.surname
    elif style.lower() == 'steampunk':
        surname = human_steampunk.surname
    elif style.lower() == 'medieval':
        surname = human_medieval.surname
    elif style.lower() == 'tolkien':
        surname = human_tolkien.surname
    elif style.lower() == 'jordan':
        surname = human_jordan.surname
    elif style.lower() == 'erikson':
        surname = human_erikson.surname
    elif style.lower() == 'rowling':
        surname = human_rowling.surname
    elif style.lower() == 'sapkowski':
        surname = human_sapkowski.surname
    
    return f"{name} {surname}"


if __name__ == '__main__':
    name = generate_name()
    print(name)
