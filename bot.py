from telegram.ext import Updater, MessageHandler, Filters
import configparser

config = configparser.ConfigParser()
config.read('bot.cfg')


def get_banlist():
    banlist = config.get('Main', 'banlist')
    return [int(i) for i in banlist.split(',') if i]


def ban_fwd(bot, update):
    msg = update.message
    chat_id = msg.chat.id

    if msg.forward_from_chat.id in get_banlist():
        try:
            bot.kickChatMember(chat_id, msg.from_user.id)
            bot.sendMessage(chat_id=chat_id,
                            text='%s отправлен в Вальхаллу [🔥SPAM]' % msg.from_user.name)
        except Exception as e:
            print(e)
            bot.sendMessage(chat_id=chat_id,
                            text='%s спамит, но забанить не могу 😭' % msg.from_user.name)


if __name__ == '__main__':
    updater = Updater(str(config.get('Main', 'token')))

    updater.dispatcher.add_handler(MessageHandler(Filters.forwarded, ban_fwd))

    updater.start_polling()
    updater.idle()