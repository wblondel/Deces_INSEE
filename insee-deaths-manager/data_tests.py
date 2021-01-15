def dates_birth_is_before_death(row):
    return row[2] <= row[6]


def fullname_is_complete(row):
    if "*" in row[0] and row[0].endswith('/'):
        nom, prenoms = row[0].split("*")
        prenoms = prenoms[:-1]
        return nom and prenoms and not nom.isspace() and not prenoms.isspace()
    else:
        return False


def gender_value(row):
    return row[1] == "1" or row[1] == "2"


def postcodes_are_int(row):
    def test_postcode_is_int(postcode):
        if postcode.startswith('2A') or postcode.startswith('2B'):
            if postcode[2:].isnumeric():
                return True

        return postcode.isnumeric()

    return test_postcode_is_int(row[3]) and test_postcode_is_int(row[7])


def dates_are_int(row):
    return row[2].isnumeric() and row[6].isnumeric()


def city_empty_when_postcode_990(row):
    if row[3].endswith('990'):
        return not row[4]
    return True


def city_correctly_formated_when_arrondissement(row):
    import regex

    if row[3].startswith('751'):
        return regex.match(r'(^PARIS \d{1,2}$)', row[4])

    if row[3].startswith('6938'):
        if row[3] == '69389' and row[4] == "SAINT-RAMBERT-L'ILE-BARBE":
            return True
        return regex.match(r'(^LYON \d{1,2}$)', row[4])

    if row[3].startswith('132'):
        return regex.match(r'(^MARSEILLE \d{1,2}$)', row[4])

    return True


def city_not_known(row):
    terms = ['INCONNU', 'RENSEIGNEMENT', 'COMMUNIQUE', 'INFORMATION', '..']

    if any(x in row[4] for x in terms):
        return True
    return False
