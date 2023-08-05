import random
import datetime

card_data = {
    'American Express': {
        'iinRanges': ['34', '37'],
        'lengths': [15]
    },
    'Bankcard': {
        'iinRanges': ['5610', '560221-560225'],
        'lengths': [16]
    },
    'China T-Union': {
        'iinRanges': ['31'],
        'lengths': [19]
    },
    'China UnionPay': {
        'iinRanges': ['62'],
        'lengths': [16, 17, 18, 19]
    },
    'Diners Club enRoute': {
        'iinRanges': ['2014', '2149'],
        'lengths': [15]
    },
    'Diners Club International': {
        'iinRanges': ['36', '300-305', '3095', '38-39'],
        'lengths': [14, 15, 16, 17, 18, 19]
    },
    'Diners Club United States & Canada': {
        'iinRanges': ['54', '55'],
        'lengths': [16]
    },
    'Discover Card': {
        'iinRanges': ['6011', '644-649', '65', '622126-622925'],
        'lengths': [16, 17, 18, 19]
    },
    'UkrCard': {
        'iinRanges': ['60400100-60420099'],
        'lengths': [16, 17, 18, 19]
    },
    'RuPay': {
        'iinRanges': ['60', '65', '81', '82', '508', '353', '356'],
        'lengths': [16]
    },
    'InterPayment': {
        'iinRanges': ['636'],
        'lengths': [16, 17, 18, 19]
    },
    'InstaPayment': {
        'iinRanges': ['637-639'],
        'lengths': [16]
    },
    'JCB': {
        'iinRanges': ['3528-3589'],
        'lengths': [16, 17, 18, 19]
    },
    'Mastercard': {
        'iinRanges': ['2221-2720', '51-55'],
        'lengths': [16]
    },

    'Laser': {
        'iinRanges': ['6304', '6706', '6771', '6709'],
        'lengths': [16, 17, 18, 19]
    },
    'Maestro (UK)': {
        'iinRanges': ['6759', '676770', '676774'],
        'lengths': [12, 13, 14, 15, 16, 17, 18, 19]
    },
    'Maestro': {
        'iinRanges': ['5018', '5020', '5038', '5893', '6304', '6759', '6761', '6762', '6763'],
        'lengths': [12, 13, 14, 15, 16, 17, 18, 19]
    },
    'Dankort': {
        'iinRanges': ['5019', '4571'],
        'lengths': [16]
    },
    'Mir': {
        'iinRanges': ['2200', '2201', '2202', '2203', '2204'],
        'lengths': [16, 17, 18, 19]
    },
    'BORICA': {
        'iinRanges': ['2205'],
        'lengths': [16]
    },
    'NPS Pridnestrovie': {
        'iinRanges': ['6054740', '6054741', '6054742', '6054743', '6054744'],
        'lengths': [16]
    },
    'Solo': {
        'iinRanges': ['6334', '6767'],
        'lengths': [16, 18, 19]
    },
    'Switch': {
        'iinRanges': ['4903', '4905', '4911', '4936', '564182', '633110', '6333', '6759'],
        'lengths': [16, 18, 19]
    },
    'Troy': {
        'iinRanges': ['65', '9792'],
        'lengths': [16]
    },
    'Visa': {
        'iinRanges': ['4'],
        'lengths': [13, 16]
    },
    'Visa Electron': {
        'iinRanges': ['4026', '417500', '4508', '4844', '4913', '4917'],
        'lengths': [16]
    },
    'UATP': {
        'iinRanges': ['1'],
        'lengths': [15]
    },
    'Verve': {
        'iinRanges': ['506099-506198', '650002-650027', '507865-507964'],
        'lengths': [16, 18, 19]
    },
    'LankaPay': {
        'iinRanges': ['357111'],
        'lengths': [16]
    },
    'UzCard': {
        'iinRanges': ['8600'],
        'lengths': [16]
    },
    'Humo': {
        'iinRanges': ['9860'],
        'lengths': [16]
    },
    'GPN': {
        'iinRanges': ['1', '2', '6', '7', '8', '9'],
        'lengths': [16]
    }
};


def luhn_check(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]

    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits + [sum(divmod(d * 2, 10)) for d in even_digits])
    return checksum % 10 == 0


def generate_credit_card(card_name, attempt=1):
    max_attempts = 100
    if attempt > max_attempts:
        raise ValueError(f"Unable to generate a valid card number after {max_attempts} attempts.")

    card_info = card_data.get(card_name)
    if not card_info:
        raise ValueError(f"Invalid card name: {card_name}")

    iin_range = random.choice(card_info['iinRanges'])
    length = random.choice(card_info['lengths'])
    card_number = generate_card_number(iin_range, length)

    if luhn_check(card_number):
        cvv = generate_cvv(card_name)
        expiry_date = generate_expiry_date()
        return {'card_number': card_number, 'cvv': cvv, 'expiry_date': expiry_date}
    else:
        return generate_credit_card(card_name, attempt + 1)


def generate_card_number(iin_range, length):
    card_number = iin_range
    remaining_length = length - len(iin_range)
    for _ in range(remaining_length):
        card_number += str(random.randint(0, 9))
    return card_number


def generate_cvv(card_name):
    cvv_length = 4 if card_name == 'American Express' else 3
    cvv = ''
    for _ in range(cvv_length):
        cvv += str(random.randint(0, 9))
    return cvv


def generate_expiry_date():
    current_year = datetime.datetime.now().year
    year = current_year + random.randint(1, 5)
    month = str(random.randint(1, 12)).zfill(2)
    return f'{month}/{year}'


