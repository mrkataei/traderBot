_lang = 'en'


def activate(lang):
    global _lang
    _lang = lang


TRANSLATIONS = {
    'C_please_start': {
        'en': 'Please /start bot again',
        'fa': 'لطفا دوباره بات را استارت کنید /start'
    },
    'C_full_watchlist': {
        'en': 'your watchlist is full!😓',
        'fa': 'واچلیست شما پر است! 😓'
    }
}


def trans(string):
    return TRANSLATIONS[string][_lang]
