
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, DispatcherHandlerStop
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
import Functions.PokemonDatabaseFunctions as Poke
import Functions.LoggingFunctions as Logger
import Functions.SearcherFunctions as Searcher
import Functions.TelegramMessageFunctions as Tele
import Handlers.CommandHandlers as Command
import Settings.AuthorizedUsers as Auth
import datetime
import time

def hello(update, context, *args):
    Tele.SendMessageFromUpdate(update.message, 
        'Hello {}{}'.format(update.message.from_user.first_name, *args))

update_id = None

def main():
    """Run the bot."""
    
    # Telegram Bot Authorization Token
    updater = Updater("", use_context=True)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    dp = updater.dispatcher

    # Get commands
    dp = receiveCommands(dp)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

def receiveCommands(dp):

    def check_allowed(update, context):
        if update.message.from_user.id not in Auth.allowedUsers:
            raise DispatcherHandlerStop

    # Check if the user is authorized or not.
    dp.add_handler(MessageHandler(Filters.all, check_allowed), -1)
    
    # Just to start.
    dp.add_handler(CommandHandler("start", Command.BotStart, filters = ~Filters.update.edited_message))

    # Actual command handlers. Add available commands to the dispatcher (dp).
    dp.add_handler(CommandHandler("scan", Command.ScanPokemons, filters = Filters.reply & ~Filters.update.edited_message))
    dp.add_handler(CommandHandler("add", Command.AddPokemons, filters = Filters.reply & ~Filters.update.edited_message))
    dp.add_handler(CommandHandler("authorizebyreply", Command.AuthorizeUserByReply, filters = Filters.reply & ~Filters.update.edited_message))
    dp.add_handler(CommandHandler("unauthorizebyreply", Command.UnauthorizeUserByReply, filters = Filters.reply & ~Filters.update.edited_message))
    dp.add_handler(CommandHandler("countdatabase", Command.CountPokemonsInDatabase, filters = ~Filters.update.edited_message))
    dp.add_handler(CommandHandler("printexamples", Command.Print10FirstPokemonsInDatabase, filters = ~Filters.update.edited_message))
    dp.add_handler(CommandHandler("getcontributors", Command.GetContributors, filters = ~Filters.update.edited_message))
    dp.add_handler(CommandHandler("getrecentcontributions", Command.GetRecentContributions, filters = ~Filters.update.edited_message))
    dp.add_handler(CommandHandler("sort", Command.SortPokemonsDatabase, filters = ~Filters.update.edited_message))
    dp.add_handler(CommandHandler("test", Command.ReplyToTest, filters = ~Filters.update.edited_message))

    return dp
            
if __name__ == '__main__':
    main()
