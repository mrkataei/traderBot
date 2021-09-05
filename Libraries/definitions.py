_lang = 'en'


def activate(lang):
    global _lang
    _lang = lang


def get_lang():
    return _lang


TRANSLATIONS = {
    'C_please_start': {
        'en': 'Please /start bot again',
        'fa': 'لطفا دوباره بات را استارت کنید /start'
    },
    'C_please_login': {
        'en': 'Please login to bot /start',
        'fa': 'لطفا وارد شودید /start'
    },
    'C_full_watchlist': {
        'en': 'your watchlist is full!😓',
        'fa': 'واچلیست شما پر است! 😓'
    },
    'C_welcome': {
        'en': 'I am Aran , your trade assistance \n /help show commands',
        'fa': 'من آران هستم ، دستیار خرید و فروش شما \n  نمایش دستورات بات /help '
    },
    'C_hello': {
        'en': 'Hey!',
        'fa': 'سلام!'
    },
    'C_login': {
        'en': '🔑Login',
        'fa': '🔑ورود'
    },
    'C_register': {
        'en': '🤩Sign up',
        'fa': '🤩ثبت نام'
    },
    'C_forget_password': {
        'en': '🔏Forget password',
        'fa': '🔏فراموشی رمز عبور'
    },
    'C_any_account': {
        'en': 'Have not any account?\nSign up now!',
        'fa': 'حساب کاربری ندارید؟\n همین الان ثبت نام کنید!'
    },
    'C_enter_username': {
        'en': '🔑Enter your username',
        'fa': '🔑نام کاربری را وارد کنید'
    },
    'C_already_have_account': {
        'en': 'You already have an account :',
        'fa': 'شما قبلا حساب کاربری ساخته اید :'
    },
    'C_enter_answer': {
        'en': 'Enter your answer',
        'fa': 'جواب خود را وارد کنید'
    },
    'C_select_coin': {
        'en': 'Select your coin',
        'fa': 'رمز ارز خود را انتخاب کنید'
    },
    'C_coin_already_exist': {
        'en': 'Coin already in watchlist /add',
        'fa': 'رمزارز قبلا در واچلیست وارد شده است /add'
    },
    'C_show_watchlist': {
        'en': '/show to show your watchlist  For change /frame',
        'fa': 'نمایش واچلیست /show'
    },
    'C_done': {
        'en': 'Done!',
        'fa': 'انجام شد!'
    },
    'C_default_timeframe': {
        'en': 'Default time frame is 30min!',
        'fa': 'تایم فریم پیش فرض 30 دقیقه است!'
    },
    'C_change_timeframe': {
        'en': 'For change /frame',
        'fa': 'تغیر تایم فریم با /frame'
    },
    'C_timeframe_changed': {
        'en': 'timeframe change to',
        'fa': 'تایم فریم تغیر کرد به'
    },
    'C_now': {
        'en': 'Now',
        'fa': 'الان'
    },
    'C_working_for_you': {
        'en': 'is working for you',
        'fa': 'برای تو کار میکند'
    },
    'C_select_watchlist': {
        'en': 'Select your watchlist',
        'fa': 'واچلیست خود را انتخاب کنید'
    },
    'C_null_watchlist': {
        'en': 'You don\'t have any watchlist! /new',
        'fa': 'شما واچلیستی ندارید!ایجاد /new'
    },
    'C_create_watchlist': {
        'en': 'For create /new',
        'fa': 'برای ایجاد /new'
    },
    'C_null_coin': {
        'en': 'No coins in your watchlist!/add😓',
        'fa': 'رمزارزی در واچلیست شما نیست!😓 ایجاد/add'
    },
    'C_create_watchlist_first': {
        'en': 'Create watchlist first! /new',
        'fa': 'ابتدا واچلیست را بسازید! /new'
    },
    'C_add_coins': {
        'en': '/add coins now!',
        'fa': 'رمزارز خود را اضافه کنید /add'
    },
    'C_enter_password': {
        'en': '🔒Enter your password',
        'fa': '🔒رمز خود را وارد کنید'
    },
    'C_password_instruction': {
        'en': '\n\n🔹your password must be at least 8 characters\n'
              '🔹And a number and special character(@#$%^&+=)\n'
              '🔹and lower/upper case at least',
        'fa': '\n\nپسورد شما باید حداقل شامل 8 کارکتر باشد🔹\n'
              '🔹باید شامل عدد و کارکترهای خاص(@#$%^&+=)\n'
              '🔹باید حروف بزرگ و کوچک را نیز شامل شود'
    },
    'C_again': {
        'en': ' again',
        'fa': ' دوباره'
    },
    'C_select_security_question': {
        'en': 'Select your security question',
        'fa': 'سوال امنیتی خود را انتخاب کنید'
    },
    'C_username_exist': {
        'en': '😞Username not exists',
        'fa': '😞نام کاربری موجود نیست'
    },
    'C_new_password': {
        'en': '🔓Enter your new password',
        'fa': '🔓رمز عبور جدید خود را وارد کنید'
    },
    'C_enter_watchlist_name': {
        'en': 'Enter your watchlist name',
        'fa': 'نام واچلیست خود را وارد کنید'
    },
    'C_already_have_watchlist': {
        'en': '😅 You have already one watchlist /show',
        'fa': '😅 شما در حال حاضر یک واچلیست دارید /show'
    },
    'C_good': {
        'en': 'Good!👀',
        'fa': 'ایول!👀'
    },
    'C_logged_out': {
        'en': '😪You are logged out',
        'fa': '😪شما خارج شده اید'
    },
    'C_select_timeframe': {
        'en': 'Select your timeframe',
        'fa': 'تایم فریم خود را وارد کنید'
    },
    'C_select_analysis': {
        'en': '📊️Select your analysis',
        'fa': '📊️آنالیز خود را وارد کنید'
    },
    'C_already_have_analysis': {
        'en': '😏You already have analysis: ',
        'fa': '😏شما درحال حاضر آنالیز دارید'
    },
    'C_select_option_delete': {
        'en': 'select option you want to delete',
        'fa': 'موردی که میخواهید پاک کنید انتخاب کنید'
    },
    'C_watchlist': {
        'en': 'Watchlist',
        'fa': 'واچلیست'
    },
    'C_coin': {
        'en': 'Coins',
        'fa': 'رمزارزها'
    },
    'C_unsuccessful_logout': {
        'en': 'logout unsuccessful',
        'fa': 'خروج ناموفق'
    },
    'C_goodbye': {
        'en': '👋🏼Goodbye!',
        'fa': '👋🏼خدانگهدار'
    },
    'C_login_again': {
        'en': 'For login /start bot ',
        'fa': 'برای ورود بات را استارت کنید /start'
    },
    'C_unsuccessful_operation': {
        'en': 'Operation unsuccessful!',
        'fa': 'عملیات ناموفق'
    },
    'C_timeframe': {
        'en': 'Timeframe',
        'fa': 'تایم فریم'
    },
    'C_assets': {
        'en': 'Assets',
        'fa': 'دارایی ها'
    },
    'C_open_time': {
        'en': 'Open time : ',
        'fa': 'زمان بازگشایی : '
    },
    'C_open': {
        'en': 'Open : ',
        'fa': 'بازگشایی : '
    },
    'C_high': {
        'en': 'High : ',
        'fa': 'بالاترین : '
    },
    'C_low': {
        'en': 'Low : ',
        'fa': 'کمترین : '
    },
    'C_close': {
        'en': 'Close : ',
        'fa': 'پایانی : '
    },
    'C_volume': {
        'en': 'Volume : ',
        'fa': 'حجم : '
    },
    'C_number_trades': {
        'en': 'Number of trades : ',
        'fa': 'تعداد معاملات : '
    },
    'M_new_signal': {
        'en': 'New received from ',
        'fa': 'سیگنال جدیدی رسید از '
    },
    'M_in': {
        'en': ' in',
        'fa': ' در'
    },
    'M_position': {
        'en': 'position',
        'fa': 'موقعیت'
    },
    'M_current_price': {
        'en': 'Current price',
        'fa': 'قیمت حاضر'
    },
    'M_target_price': {
        'en': 'Target price',
        'fa': 'قیمت هدف'
    },
    'M_risk': {
        'en': 'Risk',
        'fa': 'ریسک'
    },
    'L_successful_login': {
        'en': 'You are logged in🤩',
        'fa': 'شما وارد شدید 🤩'
    },
    'L_invalid_login': {
        'en': 'Your username or password is incorrect🥵',
        'fa': 'نام کاربری یا رمزعبور شما صحیح نمیباشد'
    },
    'R_username_exist': {
        'en': 'username already exist',
        'fa': 'نام کابری موجود میباشد'
    },
    'R_welcome': {
        'en': 'welcome',
        'fa': 'خوش آمدید'
    },
    'R_wrong_answer': {
        'en': 'answer is wrong ',
        'fa': 'پاسخ غلط است'
    },
    'R_success': {
        'en': 'success',
        'fa': 'موفقیت آمیز'
    },
    'R_try_again': {
        'en': 'try again',
        'fa': 'دوباره تلاش کنید'
    },

}


def trans(string):
    return TRANSLATIONS[string][_lang]
