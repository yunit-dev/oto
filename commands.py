from telegram import (Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo)
from telegram.ext import ContextTypes, ConversationHandler 
from database import (save_user, 
                      add_learning_language, 
                      get_user, update_name,
                      update_interface_language)
from translations import t 

NAME = 1
INTERFACE_LANGUAGE = 2 
LEARNING_LANGUAGE = 3 

SETTINGS = 4
CHANGE_NAME = 5
CHANGE_INTERFACE = 6
CHANGE_LEARNING = 7

LANGUAGES = {
    "en": "🇬🇧 English",
    "ru": "🇷🇺 Russian",
    "ja": "🇯🇵 Japanese",
    "zh": "🇨🇳 Chinese",
    "de": "🇩🇪 German",
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id 
    user = get_user(user_id)

    if user: 
        user_id, name, interface_language = user 
        await update.message.reply_text(
            t("welcome_back", interface_language).format(name=name),
                                        parse_mode="HTML",
                                        reply_markup=mini_app_keyboard()
                                        )
        return ConversationHandler.END

    
    await update.message.reply_text(
        f"<b>{t('welcome', 'en')}</b>\n\n"
        f"<i>{t('ask_name', 'en')}</i>",
    parse_mode="HTML"
    )
    return NAME 

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text
    context.user_data["name"] = name 

    keyboard = [
        [InlineKeyboardButton("🇬🇧 English", callback_data="interface_en")],
        [InlineKeyboardButton("🇷🇺 Russian", callback_data="interface_ru")],
        [InlineKeyboardButton("🇯🇵 Japanese", callback_data="interface_ja")],
        [InlineKeyboardButton("🇨🇳 Chinese", callback_data="interface_zh")],
        [InlineKeyboardButton("🇩🇪 German", callback_data="interface_de")]
    ]
    await update.message.reply_text(
        f"<b>{t('nice_to_meet', 'en').format(name=name)}</b>\n\n"
        f"<i>{t('choose_interface', 'en')}</i>",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML",
    )
    return INTERFACE_LANGUAGE

async def get_interface_language(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    language_code = query.data.replace("interface_", "")

    context.user_data["interface_language"] = language_code

    name = context.user_data["name"]

    keyboard = [
        [InlineKeyboardButton("🇬🇧 English", callback_data="learning_en")],
        [InlineKeyboardButton("🇷🇺 Russian", callback_data="learning_ru")],
        [InlineKeyboardButton("🇯🇵 Japanese", callback_data="learning_ja")],
        [InlineKeyboardButton("🇨🇳 Chinese", callback_data="learning_zh")],
        [InlineKeyboardButton("🇩🇪 German", callback_data="learning_de")]
    ]

    await query.message.reply_text(
        f"<b>{t('interface_selected', language_code).format(name=name)}</b>\n\n"
        f"<i>{t('choose_learning', language_code)}</i>",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )

    return LEARNING_LANGUAGE

async def get_learning_language(
        update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    language_code = query.data.replace("learning_", "")
    learning_language = LANGUAGES[language_code]
    context.user_data["learning_language"] = learning_language

    user_id = update.effective_user.id
    name = context.user_data["name"]
    interface_language = context.user_data["interface_language"]
    save_user(user_id=user_id, name=name, interface_language=interface_language)
    add_learning_language(user_id=user_id,
                          language=language_code)
    await query.message.reply_text(
       f"<b>{t('perfect', interface_language).format(name=name)}</b>\n\n"
       f"{t('learning', interface_language).format(language=learning_language)}\n\n"
       f"<i>{t('journey', interface_language)}</i>",
       parse_mode="HTML")
    
    await query.message.reply_text(
        "🍋 Oto is ready!", 
        reply_markup=mini_app_keyboard()
    )
    return ConversationHandler.END

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
   user_id = update.effective_user.id 
   user = get_user(user_id)

   if user:
     _, _, interface_language = user 
   else:
     interface_language = "en"
   await update.message.reply_text(
       t("help", interface_language)
   )

async def settings(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    user_id = update.effective_user.id
    user = get_user(user_id)

    if not user:
        await update.message.reply_text(
            "🍋 Please use /start first."
        )
        return ConversationHandler.END

    _, name, interface_language = user

    keyboard = [
        [
            InlineKeyboardButton(
                t("settings_change_name", interface_language),
                callback_data="settings_name"
            )
        ],
        [
            InlineKeyboardButton(
                t("settings_change_interface", interface_language),
                callback_data="settings_interface"
            )
        ],
        [
            InlineKeyboardButton(
                t("settings_change_learning", interface_language),
                callback_data="settings_learning"
            )
        ],
    ]

    await update.message.reply_text(
        t("settings_title", interface_language),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    return SETTINGS

async def save_new_name(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    new_name = update.message.text
    user_id = update.effective_user.id

    update_name(user_id, new_name)

    user = get_user(user_id)

    if user:
        _, _, interface_language = user
    else:
        interface_language = "en"

    context.user_data["name"] = new_name

    await update.message.reply_text(
        t("settings_name_changed", interface_language).format(
            name=new_name
        ),
        reply_markup=settings_after_change_keyboard(interface_language)
    )

    return SETTINGS

async def settings_change_interface(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    user = get_user(user_id)

    if user:
        _, _, interface_language = user
    else:
        interface_language = "en"

    keyboard = [
        [
            InlineKeyboardButton(
                "🇬🇧 English",
                callback_data="change_interface_en"
            )
        ],
        [
            InlineKeyboardButton(
                "🇷🇺 Русский",
                callback_data="change_interface_ru"
            )
        ],
        [
            InlineKeyboardButton(
                "🇯🇵 日本語",
                callback_data="change_interface_ja"
            )
        ],
        [
            InlineKeyboardButton(
                "🇨🇳 中文",
                callback_data="change_interface_zh"
            )
        ],
        [
            InlineKeyboardButton(
                "🇩🇪 Deutsch",
                callback_data="change_interface_de"
            )
        ]
    ]

    await query.message.reply_text(
        t("choose_new_interface", interface_language),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    return CHANGE_INTERFACE

async def save_new_interface(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    language = query.data.replace(
        "change_interface_",
        ""
    )

    user_id = update.effective_user.id

    update_interface_language(
        user_id,
        language
    )

    context.user_data["interface_language"] = language

    await query.message.reply_text(
        t("settings_language_changed", language),
    
      reply_markup=settings_after_change_keyboard(language)
    )

    return SETTINGS

async def settings_change_name(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    user = get_user(user_id)

    if user:
        _, _, language = user
    else:
        language = "en"

    await query.message.reply_text(
        t("settings_ask_name", language)
    )

    return CHANGE_NAME

async def settings_change_learning(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    user = get_user(user_id)

    if not user:
        return ConversationHandler.END
    
    _, _, interface_language = user

    keyboard = [
        [
            InlineKeyboardButton(
                "🇬🇧 English",
                callback_data="change_learning_en"
            )
        ],
        [
            InlineKeyboardButton(
                "🇷🇺 Русский",
                callback_data="change_learning_ru"
            )
        ],
        [
            InlineKeyboardButton(
                "🇯🇵 日本語",
                callback_data="change_learning_ja"
            )
        ],
        [
            InlineKeyboardButton(
                "🇨🇳 中文",
                callback_data="change_learning_zh"
            )
        ],
        [
            InlineKeyboardButton(
                "🇩🇪 Deutsch",
                callback_data="change_learning_de"
            )
        ],
    ]

    await query.message.reply_text(
        t("choose_learning", interface_language),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    return CHANGE_LEARNING

async def save_new_learning(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    language_code = query.data.replace(
        "change_learning_",
        ""
    )

    user_id = update.effective_user.id

    add_learning_language(
        user_id=user_id,
        language=language_code
    )

    user = get_user(user_id)

    if not user:
        return ConversationHandler.END
    _, _, interface_language = user

    learning_language = LANGUAGES[language_code]

    await query.message.reply_text(
        t("learning_changed", interface_language).format(
            language=learning_language
        ), 
          reply_markup=settings_after_change_keyboard(interface_language)
    )

    return SETTINGS

def mini_app_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🍋 Open Oto",
                web_app=WebAppInfo(url="https://example.com")
            )
        ]
    ])

def settings_after_change_keyboard(interface_language):
    return InlineKeyboardMarkup([
        [ InlineKeyboardButton("Open Oto🍋",
                               web_app=WebAppInfo(url="https://example.com")
                               )],
                               [InlineKeyboardButton(
                                   t("continue_settings", interface_language),
                                   callback_data="continue_settings"
                               )]
    ])

async def continue_settings(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    user = get_user(user_id)

    if not user:
        return ConversationHandler.END

    _, _, interface_language = user

    keyboard = [
        [
            InlineKeyboardButton(
                t("settings_change_name", interface_language),
                callback_data="settings_name"
            )
        ],
        [
            InlineKeyboardButton(
                t("settings_change_interface", interface_language),
                callback_data="settings_interface"
            )
        ],
        [
            InlineKeyboardButton(
                t("settings_change_learning", interface_language),
                callback_data="settings_learning"
            )
        ],
    ]

    await query.message.reply_text(
        t("settings_title", interface_language),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    return SETTINGS
    
async def open_app(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)

    if not user:
        return await start(update, context)
    
    _, _, interface_language = user
    
    keyboard = [
        [
        InlineKeyboardButton(
    "🍋 Open Oto",
    web_app=WebAppInfo(
        url="https://example.com"
    )
)
        ]
    ]
    await update.message.reply_text(
        t("oto_start", interface_language),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

