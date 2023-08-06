from . import capsify

def info_template(chats: int, users: int) -> str:
  INFO = capsify('bot info 🤖') + '\n\n'
  INFO += capsify('stats') + '\n'
  INFO += capsify('served chats :') + ' ' + chats + '\n'
  INFO += capsify('served users :') + ' ' + users + '\n\n'
  INFO += capsify('owner and belongings') + '\n'
  INFO += capsify('coded by') + ' **@North_Yankton**.\n'
  INFO += capsify('regards') + ' **@SpLBots**.\n\n'
  INFO += capsify('create your own bot by getting source code from buttons below !')
  return INFO
