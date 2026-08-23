from telegram.ext import ( Application, 
                          CommandHandler, 
                          MessageHandler, 
                          CallbackQueryHandler,
                            ConversationHandler, filters)
from database import create_table
from commands import (start, 
                       help,
                       open_app,
                       get_name,
                       get_learning_language, 
                       get_interface_language,
                       settings, 
                       settings_change_name, 
                       save_new_name,
                       settings_change_interface,
                       save_new_interface,
                       settings_change_learning, 
                       save_new_learning,
                       continue_settings,
    
                     NAME, LEARNING_LANGUAGE, 
                     INTERFACE_LANGUAGE, SETTINGS, CHANGE_NAME,
                     CHANGE_INTERFACE, CHANGE_LEARNING)


from config import TOKEN 

app = Application.builder().token(TOKEN).build()
create_table()

onboarding = ConversationHandler(
    entry_points=[
        CommandHandler("start", start) ],

     states={
        NAME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                get_name
            ) ],

        INTERFACE_LANGUAGE: [
            CallbackQueryHandler(
                get_interface_language,
                pattern=r"^interface_(en|ru|ja|zh|de)$"
            ) ],

        LEARNING_LANGUAGE: [
            CallbackQueryHandler(
                get_learning_language,
                pattern=r"^learning_(en|ru|ja|zh|de)$"
            ) ],   },

    fallbacks=[]
)

settings_conversation = ConversationHandler(
    entry_points=[
        CommandHandler("settings", settings)
    ],

    states={

        SETTINGS: [
            CallbackQueryHandler(
                settings_change_name,
                pattern=r"^settings_name$" ),

            CallbackQueryHandler(
                settings_change_interface,
                pattern=r"^settings_interface$" ),

            CallbackQueryHandler(
                settings_change_learning,
                pattern=r"^settings_learning$" ),

            CallbackQueryHandler(
                continue_settings,
                pattern=r"^continue_settings$" ), ],

        CHANGE_NAME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                save_new_name ) ],

        CHANGE_INTERFACE: [
            CallbackQueryHandler(
                save_new_interface,
                pattern=r"^change_interface_(en|ru|ja|zh|de)$" ) ],

        CHANGE_LEARNING: [
            CallbackQueryHandler(
                save_new_learning,
                pattern=r"^change_learning_(en|ru|ja|zh|de)$" )
        ],
    },

    fallbacks=[],
    allow_reentry=True
)

app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("app", open_app))

app.add_handler(settings_conversation)
app.add_handler(onboarding)

print("Bot is working...")
app.run_polling()




