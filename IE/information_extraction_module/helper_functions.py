import dateparser


def is_good_character(character):
    character_order = ord(character)

    if character_order >= 97 and character_order <= 122:
        return True

    if character_order >= 48 and character_order <= 57:
        return True

    if character_order >= 65 and character_order <= 90:
        return True

    if character_order == 32:
        return True

    return False


def data_concatenator(json_object):
    row_data = ""
    for key, value in json_object.items():
        row_data = row_data + value + " "
    return row_data


def text_filtering(string):
    cleaned_text = ""
    for character in string:
        if is_good_character(character):
            cleaned_text += character
    return cleaned_text


def process_row_data(json_object):
    return text_filtering(data_concatenator(json_object))


def clean_date(date_string):
    date_string = date_string.lower()
    date_string = date_string.replace('posted', '')
    return date_string.strip()


def clean_url(url):
    cleaned_url = url.split("?")[0]
    return cleaned_url
