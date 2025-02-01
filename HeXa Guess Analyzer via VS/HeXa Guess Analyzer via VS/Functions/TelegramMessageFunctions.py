import telegram
from time import sleep
from telegram.error import NetworkError, Unauthorized, RetryAfter, TimedOut

def SendMessageFromUpdate(messageUpdate, msgToSend):
    
    try:
        attempts = 0
        max_attempts = 10
        retry_delay = 10

        while attempts < max_attempts:
            try:
                messageUpdate.reply_text(msgToSend)
            except (RetryAfter, TimedOut) as e:
                print("Timeout")
                time.sleep(retry_delay)
                attempts += 1
            else:
                break

    except Exception as e:
        print(e)
