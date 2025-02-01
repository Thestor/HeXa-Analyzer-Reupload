import Functions.PokemonDatabaseFunctions as Poke
import Functions.LoggingFunctions as Logger
import Functions.SearcherFunctions as Searcher
import Functions.TelegramMessageFunctions as Tele
import datetime
import time

def BotStart(update, context):
    Tele.SendMessageFromUpdate(update.message, "Hi!")

def ScanPokemons(update, context):

    try:
        """FLAGS"""
        pokemonName = ""

        # Indicate the beginning of the download.
        countStart = time.time()

        reply_to_message = update.message.reply_to_message
        reply_to_photo = reply_to_message.photo[-1].get_file().download()

        #Indicate time necessary to complete download.
        countHalf = time.time()
        halfElapsed = round(countHalf - countStart, 3)

        RGBList = Poke.scanRGB(reply_to_photo)

        isSuccess, PokemonsList = Poke.GetPokemonsListFromDatabase()
        if isSuccess:
            searchSuccess, isFound, index = Searcher.InitiateBinarySearch(PokemonsList, RGBList, key_start = 0, key_end = 10)
            if isFound:
                getNameSuccess, pokemonName = Poke.GetPokemonByIndex(PokemonsList, index)
     
        if pokemonName != "":

            # Successful. Get and send the time necessary to complete all the process.
            countStop = time.time()
            finalElapsed = round(countStop - countStart, 3)
            Tele.SendMessageFromUpdate(update.message, pokemonName + f"\nTime elapsed = {finalElapsed} seconds\nTime elapsed until download "
                                        f"complete: {halfElapsed} seconds")

        elif not isSuccess:
            Tele.SendMessageFromUpdate(update.message, "Failed to extract data from the database.")

        elif not searchSuccess:
            Tele.SendMessageFromUpdate(update.message, "Failed to perform binary search.")

        else:
            Tele.SendMessageFromUpdate(update.message, "Data not found.")

    except Exception as e:
        print(e)
        Tele.SendMessageFromUpdate(update.message, "Failed.")

def AddPokemons(update, context):
    
    try:
        if update.message.reply_to_message.from_user.id == 572621020 and\
            update.message.reply_to_message.caption == "Who's that pokemon?":

            reply_to_message = update.message.reply_to_message
            reply_to_photo = reply_to_message.photo[-1].get_file().download()
            pokemonName = context.args[0].title()

            RGBList = Poke.scanRGB(reply_to_photo)
            isSuccess = Poke.AddToTxtDatabase(RGBList, pokemonName)
            isSuccess2 = Poke.SortDatabaseByNumber()
            if isSuccess and isSuccess2:
                Tele.SendMessageFromUpdate(update.message, "Data {} successfully recorded.".format(pokemonName))
                Logger.AddLog(update.message.from_user.id, pokemonName)
            else:
                Tele.SendMessageFromUpdate(update.message, "The picture already exists. No need to add.")
        else:
            Tele.SendMessageFromUpdate(update.message, "Bruh, that isn't a Pokemon picture, or it isn't from HeXa.")

    except Exception as e:
        print(e)
        Tele.SendMessageFromUpdate(update.message, "Failed to add a new record.")

def GetContributors(update, context):

    try:
        isSuccess, contributors = Logger.GetContributors()
        if isSuccess:
            Tele.SendMessageFromUpdate(update.message, "Here are the contributions per ID.\n\n"
                                        "None that this feature is implemented after some contributions. "
                                        "Hence, some may not be recorded in the log file.\n\n"
                                        "{}".format(contributors))

        else:
            Tele.SendMessageFromUpdate(update.message, "Failed to get the contributors dictionary.")

    except Exception as e:
        print(e)
        Tele.SendMessageFromUpdate(update.message, "Failed to get the contributors dictionary.")

def GetRecentContributions(update, context):

    try:
        if not context.args:
            howMany = 5
        else:
            howMany = eval(context.args[0])

        isSuccess, contributions = Logger.GetRecentContributions(howMany)  
  
        if isSuccess:
            Tele.SendMessageFromUpdate(update.message, "Here are the recent contributions.\n\n"
                                        "{}".format("".join(map(str, contributions)).replace("\n", "\n")))
        else:
            Tele.SendMessageFromUpdate(update.message, "Failed to get recent contributions list.")

    except Exception as e:
        print(e)
        Tele.SendMessageFromUpdate(update.message, "Failed to get the contributors list.")

def CountPokemonsInDatabase(update, context):

    try:
        isSuccess, count = Poke.ScanTxtDatabaseForMatches(onlyCount = True)
        if isSuccess:
            Tele.SendMessageFromUpdate(update.message, "The current number of records: " + str(count))
        else:
            Tele.SendMessageFromUpdate(update.message, "Failed to count the number of records.")

    except Exception as e:
        print(e)
        Tele.SendMessageFromUpdate(update.message, "Failed to count the number of records.")

def AuthorizeUserByReply(update, context):

    try:
        to_reply_id = update.message.reply_to_message.from_user.id
        if to_reply_id in allowedUsers:
            Tele.SendMessageFromUpdate(update.message, f"{to_reply_id} has already been authorized.")
        else:
            allowedUsers.append(to_reply_id)
            Tele.SendMessageFromUpdate(update.message, f"Authorization for {to_reply_id} successful!")

    except Exception as e:
        print(e)
        Tele.SendMessageFromUpdate(update.message, "Failed to authorize the specified user.")

def UnauthorizeUserByReply(update, context):

    try:
        to_reply_id = update.message.reply_to_message.from_user.id
        if to_reply_id not in allowedUsers:
            Tele.SendMessageFromUpdate(update.message, f"{to_reply_id} hasn't been authorized yet.")
        else:
            allowedUsers.remove(to_reply_id)
            Tele.SendMessageFromUpdate(update.message, f"Unauthorization for {to_reply_id} successful!")

    except Exception as e:
        print(e)
        Tele.SendMessageFromUpdate(update.message, "Failed to authorize the specified user.")

def Print10FirstPokemonsInDatabase(update, context):

    try:
        isSuccess, examples = Poke.ScanTxtDatabaseForMatches(onlyExamples = True)
        if isSuccess:
            Tele.SendMessageFromUpdate(update.message, "Here are the first ten records: \n\n" + "".join(map(str, examples)))
        else:
            Tele.SendMessageFromUpdate(update.message, "Failed to display examples.")

    except Exception as e:
        print(e)
        Tele.SendMessageFromUpdate(update.message, "Failed to display examples.")

def SortPokemonsDatabase(update, context):

    try:
        isSuccess = Poke.SortDatabaseByNumber()
        if isSuccess:
            Tele.SendMessageFromUpdate(update.message, "Sorting completed.")
        else:
            Tele.SendMessageFromUpdate(update.message, "Failed to sort.")

    except Exception as e:
        print(e)
        Tele.SendMessageFromUpdate(update.message, "Failed to sort.\nReason:", e)

def ReplyToTest(update, context):

    Tele.SendMessageFromUpdate(update.message, update.message.text)