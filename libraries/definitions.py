"""
    Mr.Kataei 11/12/2021
    this is bot dictionary for added language you need just add your lang in bellow of 'fa' lang
            ex:     'C_please_start': {
                    'en': 'Please /start bot again',
                    'fa': 'لطفا دوباره بات را استارت کنید /start'
                    'la' : 'lka kdsa '  <------ new
                    },
"""
_lang = 'fa'


def activate(lang):
    global _lang
    _lang = lang


def get_lang():
    return _lang


"""
'': {
        'en': '',
        'fa': ''
    }
"""

TRANSLATIONS = {
    'C_please_start': {
        'en': 'Please /start bot again',
        'fa': 'لطفا بات را استارت کنید /start'
    },
    'C_exchanges': {
        'en': '🏛 exchanges',
        'fa': '🏛 صرافی ها'
    },
    'C_hello': {
        'en': 'Hey!',
        'fa': 'سلام!'
    },
    'M_new_signal': {
        'en': 'New received from ',
        'fa': 'سیگنال جدیدی رسید از '
    },
    'C_now': {
        'en': 'Now',
        'fa': 'الان'
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
    'M_risk': {
        'en': 'Risk',
        'fa': 'ریسک'
    },
    'C_timeframe': {
        'en': 'Timeframe',
        'fa': 'تایم فریم'
    },
    'C_sorry_signup': {
        'en': 'Sorry\n😥You should signup first',
        'fa': 'ببخشید\n 😥شما باید اول ثبت نام کنید'
    },
    'C_add_strategy': {
        'en': '📊 add strategy',
        'fa': '📊 استراتژی اضافه کن'
    },
    'C_add_exchange': {
        'en': '🏛 add exchange',
        'fa': '🏛 صرافی اضافه کن'
    },
    'C_tutorials': {
        'en': '📚 tutorials',
        'fa': '📚 آموزش ها'
    },
    'C_plans': {
        'en': '💳 plans',
        'fa': '💳 اشتراک ها'
    },
    'C_profile': {
        'en': '🙍🏻‍♂️profile',
        'fa': '🙍🏻‍♂️پروفایل'
    },
    'C_back_test': {
        'en': '🧭 back test',
        'fa': '🧭 بک تست'
    },
    'C_social_medias': {
        'en': '📬 social medias',
        'fa': '📬 شبکه های اجتماعی'
    },
    'C_help': {
        'en': '🤔 help me',
        'fa': '🤔 کمکم کن'
    },
    'C_lang': {
        'en': '🌏 change language',
        'fa': '🌏 تغییر زبان'
    },
    'C_coin': {
        'en': '🪙Coin',
        'fa': '🪙رمزارز'
    },
    'C_strategy': {
        'en': '📊Strategy',
        'fa': '📊استراتژی'
    },
    'C_percent_usd': {
        'en': '💰Percent usd',
        'fa': '💰درصد دلاری'
    },
    'C_exchange': {
        'en': '🏛Exchange',
        'fa': '🏛صرافی'
    },
    'C_expire_plan': {
        'en': 'Your plan is expire!😪\n Recharge your plan please.',
        'fa': 'اشتراکت تموم شده!😪 \n لطفا اشتراکتو را تمدید کن.'
    },
    'C_full_strategies': {
        'en': '❌ Your strategies is full\n 🤓 Upgrade your /plan or edit it in your /profile',
        'fa': '❌ استراتژی هات به سقفش رسیده. \n 🤓 اشتراکتو ارتقا بده یا اونو تو پروفایلت تغییر بده'
    },
    'C_full_exchanges': {
        'en': '❌ Your exchange accounts is full\n 🤓 Upgrade your /plan or edit it in your /profile',
        'fa': '❌ اکانتای صرافیت به سقفش رسیده. \n 🤓 اشتراکتو ارتقا بده یا اونو تو پروفایلت تغییر بده'
    },
    'C_edit': {
        'en': 'edit',
        'fa': 'ویرایش کن'
    },
    'C_delete': {
        'en': 'delete',
        'fa': 'پاک کن'
    },
    'C_assets': {
        'en': '💰Your assets',
        'fa': '💰دارایی هات'
    },
    'C_trade_history': {
        'en': '🔹Your last 10 trade history\n\n',
        'fa': '🔹10 معامله آخرت \n\n'
    },
    'C_date': {
        'en': 'Date',
        'fa': 'تاریخ'
    },
    'C_price': {
        'en': '💵Price',
        'fa': '💵قیمت'
    },
    'C_position': {
        'en': '🔑Position',
        'fa': '🔑موقعیت'
    },
    'C_order_status': {
        'en': '☢️Order status',
        'fa': '☢️وضیعت سفارش'
    },
    'C_status': {
        'en': '☢️Status',
        'fa': '☢️وضیعت'
    },
    'C_submit_order_time': {
        'en': '⏰Submit order time',
        'fa': '⏰زمان ارسال سفارش'
    },
    'C_receive_signal_time': {
        'en': '⏰Signal receive time',
        'fa': '⏰زمان رسیدن سیگنال'
    },
    'C_done': {
        'en': '✅ Done',
        'fa': '✅ انجام شد'
    },
    'C_hey': {
        'en': '🙋🏽‍♂️ Hey ',
        'fa': '🙋🏽‍♂️ سلام'
    },
    'C_welcome': {
        'en': 'I am AI Trader, your trade assistance\n /help to show what can i do for you😎',
        'fa': 'من AI Trader ام، دستیار هوشمند معامله گرت'
              '\n /help بهت نشون میدم چکارایی میتونم برات انجام بدم 😎'
    },
    'C_share_contact': {
        'en': '📞 Share your phone number',
        'fa': '📞 شمارتو برام بفرست'
    },
    'C_reg_with_phone': {
        'en': 'You should sign up with your phone number 🙄',
        'fa': 'باید شمارتو برای ثبت نام داشته باشم🙄'
    },
    'C_can_i_help': {
        'en': '🤓 How can i help you?',
        'fa': '🤓 چطور میتونم کمکت کنم؟'
    },
    'C_enter_username': {
        'en': '🙍🏻‍♂️ Please enter your username',
        'fa': '🙍🏻‍♂️ لطفا نام کاربری خودتو وارد کن'
    },
    'C_invalid_username': {
        'en': '⛔️ Invalid username!at least 4 english char\nTry again!',
        'fa': '⛔️ نام کاربریت اشتباهه!حداقل باید 4 حرف انگلیسی باشه و با عدد یا علایمی شروع نشده باشه'
              '\nدوباره سعی کن!'
    },
    'C_exist_username': {
        'en': '⛔️ Username already exist!\nTry again!',
        'fa': '⛔️ نام کاربریت قبلا ثبت شده!\n دوباره سعی کن!'
    },
    'C_try_again': {
        'en': '⛔️ Try again',
        'fa': '⛔️ دوباره سعی کن'
    },
    'C_account_created': {
        'en': '🥳 Welcome!\n Your account created!\n⚠️ Free plan is available for 30 day\n Enjoy!',
        'fa': '🥳 خوش اومدی!\n حساب کاربریتساخته شد! \n ⚠️ اشتراک رایگانت تا 30 روز دیگر معتبره\nلذت ببرید!'
    },
    'C_choose_exchange': {
        'en': '🏛  Please Select your exchange account',
        'fa': '🏛  لطفا صرافیتو انتخاب کن'
    },
    'C_error': {
        'en': '⛔️ Error',
        'fa': '⛔️ خطا'
    },
    'C_coming_soon': {
        'en': '🤓 Our tutorials coming soon!',
        'fa': '🤓 آموزش ها بزودی بارگذاری میشه!یکم صبر کن'
    },
    'C_demo_exist': {
        'en': '😥 You already have demo',
        'fa': '😥 اکانت دمو شما موجود است!'
    },
    'C_demo_created': {
        'en': '✅ your exchange demo account successfully updated/created\nand you can watch your assets in your profile',
        'fa': '✅ اکانت دمو شما با موفقعیت ایجاد/بروزرسانی شد'
    },
    'C_same_exchange': {
        'en': '😥 You cant have same exchange account! ',
        'fa': '😥  نمیتونی دو اکانت از یک صرافی داشته باشی'
    },
    'C_enter_public_key': {
        'en': '🔐 Enter your public API',
        'fa': '🔐 کلید عمومی خودتو وارد کن'
    },
    'C_wrong_exchange': {
        'en': '⛔️ wrong exchange',
        'fa': '⛔️ صرافیت معتبر نیست'
    },
    'C_enter_secret_key': {
        'en': '🔐 Enter your secret API',
        'fa': '🔐 کلید خصوصی خودتو وارد کن'
    },
    'C_wrong_API': {
        'en': '⛔️ wrong APIs/Token.\nTry again!',
        'fa': '⛔️ یکی از کلید ها/توکن اشتباهه.\n دوباره تلاش کن'
    },
    'C_something_wrong': {
        'en': '😥 Something is wrong\n Try again! ',
        'fa': '😥 اشتباهی پیش اومده.\n لطفا دوباره تلاش کن!'
    },
    'C_success': {
        'en': '✅ success',
        'fa': '✅ ایول'
    },
    'C_unsupported_exchange': {
        'en': '⛔️ unfortunately this exchange not supported for now',
        'fa': '⛔️ متاسفانه این صرافی درحال حاضر پشتبانی نمیشه!'
    },
    'C_choose_analysis': {
        'en': '📊 Please Select Strategy',
        'fa': '📊 استراتژی خودتو انتخاب کن'
    },
    'C_choose_coin': {
        'en': '🪙 Choose Coin',
        'fa': '🪙 رمزارز خودتو انتخاب کن'
    },
    'C_wrong_analysis': {
        'en': '⛔️ wrong Strategy',
        'fa': '⛔️ استراتژیت معتبر نیست'
    },
    'C_choose_timeframe': {
        'en': '⏱ Choose timeframe',
        'fa': '⏱ تایم فریم خودتو انتخاب کن'
    },
    'C_wrong_coin': {
        'en': '⛔️ wrong coin',
        'fa': '⛔️ رمزارزت معتبر نیست'
    },
    'C_initial_value_back_test': {
        'en': '💰 Please enter amount of founds initially available for the strategies for trade(⚠️ greater than 0)',
        'fa': '💰 با چند دلار میخوای معامله رو شروع کنی؟(⚠️ باید از 0 بزرگتر باشه)'
    },
    'C_wrong_timeframe': {
        'en': '⛔️ wrong timeframe',
        'fa': '⛔️ تایم فریمت معتبر نیست'
    },
    'C_warning_amount_back_test': {
        'en': '⚠️ Amount must be greater than 0',
        'fa': '⚠️ مقدار دلار باید بیشتر از 0 باشه '
    },
    'C_processing': {
        'en': 'Just a moment, processing ...',
        'fa': 'شکیبا باشید، در حال پردازش ...'
    },
    'C_wrong_setting_back_test': {
        'en': '⛔️This strategy doesnt work with this timeframe and coin\n',
        'fa': '⛔️این استراتژی با این تایم فریم یا این رمزارز کار نمیکنه.'
    },
    'C_start_time': {
        'en': '⏲Start time',
        'fa': '⏲تاریخ شروع'
    },
    'C_end_time': {
        'en': '⏲End time',
        'fa': '⏲تاریخ پایان'
    },
    'C_positive': {
        'en': '🟢Positive trades',
        'fa': '🟢معاملات موفق'
    },
    'C_total_trades': {
        'en': '🟢total trades',
        'fa': '🟢تعداد معاملات'
    },
    'C_total_trade_accuracy': {
        'en': '✅Total trade accuracy percent',
        'fa': '✅ درصد موفقیت تمامی معاملات'
    },
    'C_net_profit_percent': {
        'en': '✅Net profit percent',
        'fa': '✅درصد سود'
    },
    'C_average_trade_profit': {
        'en': '✅Average trade profit',
        'fa': '✅میانگین سود هر معامله'
    },
    'C_profit_per_coin': {
        'en': '✅Profit per coin percent',
        'fa': '✅درصد سود برحسب رمزارز'
    },
    'C_warning_set_exchange_first': {
        'en': '⛔️ Please set your exchange account first',
        'fa': '⛔️ اول صرافی خودتو وارد کن'
    },
    'C_enter_percent_usd': {
        'en': '💰 Please enter percent of USD \n You want to trade (⚠️ between 0 - 100)',
        'fa': '💰 چند درصد از حسابت وارد معامله بشه؟(⚠️ بین 0 تا 100 )'
    },
    'C_warning_percent_usd': {
        'en': '⚠️ Percent must be between 0 - 100',
        'fa': '⚠️ درصدت باید بین 0 تا 100 باشه'
    },
    'C_exist_strategy': {
        'en': '😥You already have this strategy with selected coin and strategy',
        'fa': '😥  قبلا این استراتژی رو با این مشخصات انتخاب کردی'
    },
    'C_strategies': {
        'en': '📊 strategies',
        'fa': '📊 استراتژی ها'
    },
    'C_trades_history': {
        'en': 'trade history',
        'fa': 'سوابق معاملات'
    },
    'C_plan': {
        'en': '💳 Plan',
        'fa': '💳 اشتراک'
    },
    'C_valid_date': {
        'en': '⏱ Valid date',
        'fa': '⏱ تاریخ اعتبار'
    },
    'C_follow_us': {
        'en': '📬 Follow us on social media',
        'fa': '📬 ما را در شبکه های اجتماعی دنبال کن'
    },
    'C_charge_plan': {
        'en': 'contact admin to upgrade your plan',
        'fa': 'برای تمدید یا ارتقا اشتراکت با ادمین تماس بگیر'
    },
    'C_choose_language': {
        'en': '🌏 select your language',
        'fa': '🌏 زبان خودتو انتخاب کن'
    },
    'C_was_selected': {
        'en': 'was selected.',
        'fa': 'انتخاب شد.'
    },
    'C_instagram': {
        'en': 'instagram',
        'fa': 'اینستاگرام'
    },
    'C_telegram': {
        'en': 'telegram',
        'fa': 'تلگرام'
    },
    'C_twitter': {
        'en': 'twitter',
        'fa': 'توییتر'
    },
    'C_dont_understand': {
        'en': 'sorry speak louder 😅, dont understand.'
              '\nre/start bot or change your /lang'
              '\nmore /help',
        'fa': 'ببخشید بلندتر صحبت کن 😅، نمیفهممت.\n'
              'ربات رو دوباره استارت کن./start یا زبونتو عوض کن./lang \n'
              'کمک بیشتر /help'
    },
    'C_help_message': {
        'en': '🤦🏻‍♂️Step 1 :\n you need *exchange* to use our strategies.\n'
              'so first (🏛 add /exchange)\n'
              '(if you just want use our signals choose *demo* in exchange category)\n'
              '\n'
              '🤨 Step 2 :\n'
              'after set exchange then (📊 add /strategy).\n'
              '🤓 *you can also run (🧭 back /test) before select strategy or exchange*\n'
              '\n'
              '🥵Ops! Did you make the wrong choice?\n Dont worry!'
              'you can edit/delete strategies or exchange on your profile '
              'with ( 🙍🏻‍♂️ /profile) also watch your plan, strategies and exchanges!\n\n'
              '⛔️Remember you can not delete your exchange !change it to demo!\n'
              '🥺 if you dont need me anymore , invoke your API key in your exchange!\n'
              '\n\n'
              'watch our all free (📚 tutorials) !\n'
              'Enjoy 🤠',
        'fa': '🤦🏻‍♂️گام اول :\n به یک اکانت *صرافی* برای استفاده از استراتژی ها نیاز داری.\n'
              'پس اول 🏛 صرافی اضافه کن یا از دستور /exchange استفاده کن\n'
              '(اگر فقط میخوای از سیگنالامون استفاده کنی تو اضافه کردن صرافی گزینه *demo* رو انتخاب کن.)\n'
              '\n'
              '🤨 گام دوم:\n'
              'بعد از تنظیم صرافی گزینه 📊استراتژی اضافه کن یا دستور /strategy رو انتخاب کن\n'
              '🤓 * میتونی برای بررسی عملکرد ربات درگذشته با گزینه 🧭 بک تست یا دستور'
              ' /test از عملکرد اون خروجی بگیری*\n'
              '\n'
              '🥵ای وای!اگه تو انتخاب استراتژی یا صرافی اشتباه کردی؟ اصلا نگران نباش!'
              'میتونی استراتژی یا صرافی در 🙍🏻‍♂ پروفایل ویرایش یا پاک کنی.\n\n'
              ' برای کمک بیشتر از 📚 آموزش ها کمک بگیر!\n'
              'حالشو ببر 🤠'
    },
    'C_any_strategies': {
        'en': 'Don have any strategies🙄',
        'fa': 'استراتژی نداری خب🙄'
    },
    'C_any_exchanges': {
        'en': 'Dont have any exchanges🙄',
        'fa': 'صرافی نداری خب🙄'
    },
    'C_any_trades': {
        'en': 'Dont have any trades🙄',
        'fa': 'معامله ای انجام نشده🙄'
    },
    'C_final_amount': {
        'en': '✅Your final amount',
        'fa': '✅دارایی نهایی شما'
    },
    'C_enter_token': {
        'en': '🔐 Enter your token',
        'fa': '🔐 توکن خودرا وارد کنید'
    },
    'C_assets_exchange': {
        'en': '💰 assets',
        'fa': '💰 دارایی ها'
    },
    'C_invoke': {
        'en': 'invoke',
        'fa': 'غیرفعال'
    },
    'C_active': {
        'en': '🥶 Your API/Token is invoked,please active it with edit',
        'fa': '🥶 توکن/API  شما غیرفعال شده است،لطفا اونو با ویرایش دوباره تنظیمش کن'
    },
    'C_watchlists':{
        'en': '👀 watchlists',
        'fa': '👀 واچلیست ها'
    },
    'c_created_at':{
        'en': '⏰ created at',
        'fa': '⏰ ایجاد شده در'
    },
    'C_edit_watchlists':{
        'en': '👀 edit watchlists',
        'fa': '👀 ویرایش واچلیست ها',
    }

}


def trans(string: str):
    return TRANSLATIONS[string][_lang]
