import os
from pytimeparse import parse
import ptbot
from functools import partial

TG_TOKEN = os.environ['TELEGRAM_TOKEN']
TG_CHAT_ID = os.environ['TG_CHAT_ID']


def wait(chat_id, question, bot):
    message_id = bot.send_message(chat_id, "Запускаю таймер!")
    parser_time = parse(question)
    bot.create_countdown(parser_time, notify_progress, parser_time=parser_time, bot=bot, chat_id=chat_id, message_id=message_id)


def notify_progress(secs_left, chat_id, message_id, parser_time, bot):
    progress_bar = render_progressbar(parser_time, parser_time - secs_left)
    bot.update_message(chat_id, message_id, f"Осталось {secs_left} секунд! \n {progress_bar}")
    if secs_left == 0:
        bot.send_message(chat_id, "Время вышло")


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def main():
    bot = ptbot.Bot(TG_TOKEN)
    bot.reply_on_message(partial(wait, bot=bot))
    bot.run_bot()


if __name__ == '__main__':
    main()
