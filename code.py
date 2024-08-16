import os

from pytimeparse import parse

import ptbot

TG_TOKEN = os.environ['TELEGRAM_TOKEN']
TG_CHAT_ID = os.environ['TG_CHAT_ID']
bot = ptbot.Bot(TG_TOKEN)


def wait(chat_id, question):
    message_id = bot.send_message(chat_id, "Запускаю таймер!")
    parser_time = parse(question)
    bot.create_countdown(parser_time,
                         notify_progress,
                         parser_time=parser_time,
                         chat_id=chat_id,
                         message_id=message_id)


def notify_progress(secs_left, chat_id, message_id, parser_time):
    progres_bar = render_progressbar(parser_time, parser_time - secs_left)
    bot.update_message(chat_id, message_id,
                       f"Осталось {secs_left} секунд! \n {progres_bar}")
    if secs_left == 0:
        bot.send_message(chat_id, "Время вышло")


def render_progressbar(total,
                       iteration,
                       prefix='',
                       suffix='',
                       length=30,
                       fill='█',
                       zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def main():
    bot.reply_on_message(wait)
    bot.run_bot()


if __name__ == '__main__':
    main()
