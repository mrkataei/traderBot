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
    'C_help': {
        'en': '/start - login or Create account\n'
              '/new - Create new watchlist \n'
              '/add - Add coins in your selected watchlist \n'
              '/frame - Change your timeframe \n'
              '/analysis - Add analysis  candle \n'
              '/candle - show your coins details \n'
              '/recommendation - show you indicators recommendations \n'
              '/show - Show all details \n'
              '/remove - Remove coins ,watchlist or analysis \n'
              '/logout  - Logout from account\n',
        'fa': '/start - ورود یا ایجاد حساب کاربری'
              '\n/new - ایجاد واچلیست جدید '
              '\n/add - اضافه کردن رمزارز به واچلیست  '
              '\n/frame - عوض کردن تایم فریم  '
              '\n/candle - نمایش اطلاعات رمزارزها'
              '\n/recommendation - نمایش پیشنهادات خرید و فروش اندیکاتورها'
              '\n/analysis - اضافه کردن آنالیز'
              '\n/show - نمایش اطلاعات حساب'
              '\n/remove - حذف رمزارز ، واچلیست یا آنالیز '
              '\n/logout  - خروج از حساب کاربری',
    },
    'C_guide': {
        'en': '1-First you need an account sign up now!\n'
              '2-Create watchlist with /new\n'
              '3-/add your fav coins\n'
              '4-Select your /analysis to our signals sends to you\n'
              '5-change default timeframe(30min) /frame\n'
              '6-Enjoy 😃',
        'fa': '1-اول نیاز به یک حساب کاربری داری همین الان ثبتنام کن!'
              '\n2-واچلیست خودتو بساز /new '
              '\n3-رمزارزهای خودتو اضافه کن /add '
              '\n4-آنالیز خوتو انتخاب کند تا برات سیگنالهامون ارسال شن /analysis '
              '\n5-تایم فریم خودتو تغییر بده (تایم فریم پیشفرض 30 دقیقه) /frame '
              '\n6-حالشو ببر 😃 '
    },
    'C_add_keyboard': {
        'en': '➕ add coin',
        'fa': '➕ اضافه کردن رمزارز'
    },
    'C_new_keyboard': {
        'en': '🆕 new watchlist',
        'fa': '🆕 واچلیست جدید'
    },
    'C_analysis_keyboard': {
        'en': '📊 add analysis',
        'fa': '📊 اضافه کردن آنالیز'
    },
    'C_candle_keyboard': {
        'en': '🕯 show candle',
        'fa': '🕯 نمایش کندل'
    },
    'C_show_keyboard': {
        'en': '📺 show profile',
        'fa': '📺 نمایش حساب کاربری'
    },
    'C_recommendation_keyboard': {
        'en': '🧐 show recommendation',
        'fa': '🧐 نمایش پیشنهادات'
    },
    'C_remove_keyboard': {
        'en': '❌ delete option',
        'fa': '❌ حذف آپشن ها'
    },
    'C_logout_keyboard': {
        'en': '👋🏽 logout account',
        'fa': '👋🏽 خروج از حساب کاربری'
    },
    'C_frame_keyboard': {
        'en': '⏱ change timeframe',
        'fa': '⏱ عوض کردن تایم فریم'
    },
    'C_help_keyboard': {
        'en': '🙏🏽 help me',
        'fa': '🙏🏽 کمکم کن'
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
        'en': 'I am for Algowatch, your trade assistance \n /help show commands',
        'fa': 'من الگوواچ هستم ، دستیار خرید و فروش شما \n  نمایش دستورات بات /help '
    },
    'C_hello': {
        'en': 'Hey!',
        'fa': 'سلام!'
    },
    'C_login': {
        'en': '🔑Login',
        'fa': '🔑ورود'
    },
    'C_login_chat_id': {
        'en': '😈 Easy login',
        'fa': '😈 ورود آسان'
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
        'en': ' is working for you',
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
        'en': '\n\n🔹your password must be at least 8 characters',
        'fa': '\n\nپسورد شما باید حداقل شامل 8 کارکتر باشد🔹'
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
    'C_buy': {
        'en': 'Buy',
        'fa': 'خرید'
    },
    'C_sell': {
        'en': 'Sell',
        'fa': 'فروش'
    },
    'C_neutral': {
        'en': 'Neutral',
        'fa': 'خنثی'
    },
    'C_recommendation': {
        'en': 'Recommendation',
        'fa': 'پیشنهاد'
    },
    'C_Compute': {
        'en': 'Compute',
        'fa': 'محاسبه شده'
    },
    'C_moving_averages': {
        'en': 'Moving averages',
        'fa': 'میانگین متحرک ها'
    },
    'C_oscillators': {
        'en': 'Oscillators',
        'fa': 'اسیلاتورها'
    },
    'C_select_timeframe': {
        'en': 'Select your timeframe',
        'fa': 'تایم فریم خود را وارد کنید'
    },
    'C_select_analysis': {
        'en': '📊️Select your analysis',
        'fa': '📊️آنالیز خود را انتخاب کنید'
    },
    'C_already_have_analysis': {
        'en': '😏You already have analysis: ',
        'fa': '😏شما درحال حاضر آنالیز دارید'
    },
    'C_set_analysis_first': {
        'en': 'you dont have analysis\nSelect analysis first /analysis',
        'fa': 'شما آنالیزی ندارید\n لطفا ابتدا آنالیز خود را انتخاب کنید /analysis'
    },
    'C_analysis': {
        'en': 'analysis',
        'fa': 'آنالیز'
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
    'C_start': {
        'en': 'Please /start bot',
        'fa': 'لطفا بات را استارت کنید /start'
    },
    'C_what_can_i_do': {
        'en': 'What can i do for you?',
        'fa': 'چه کاری میتونم برات بکنم؟'
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
    'L_something_wrong': {
        'en': 'Something are going wrong!Try with simple login /start',
        'fa': 'مشکلی بجوود آمده ! لطفا، ورود با نام کاربری را امتحان کنید /start'
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
