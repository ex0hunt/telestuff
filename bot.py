import telegram
import configparser

config = configparser.ConfigParser()
config.read('bot.cfg')


def get_banlist():
    banlist = config.get('Main', 'banlist')
    return [int(i) for i in banlist.split(',') if i]


class TeleBot:
    def __init__(self):
        self.token = str(config.get('Main', 'token'))
        self.bot = telegram.Bot(token=self.token)

    def main_func(self):
        for m in self.bot.getUpdates(timeout=10):
            is_forwarded = m.message.forward_from
            forward_date = m.message.forward_date
            chat_id = m.message.chat_id
            if is_forwarded or forward_date:
                if m.message.forward_from_chat.id in get_banlist():
                    self.bot.kickChatMember(chat_id, m.message.from_user.id)
                    self.bot.sendMessage(chat_id=chat_id, text='%s отправлен в Вальхаллу [SPAM]' % m.message.from_user.name)

            if m.message.document:
                botfile = self.bot.getFile(m.message.document.file_id)
                m.message.text = botfile.file_path

            update_id = m.update_id

            self.confirm_updates(update_id)

    def confirm_updates(self, update_id):
        self.bot.getUpdates(offset=update_id+1, timeout=20)


if __name__ == '__main__':
    while True:
        TeleBot().main_func()