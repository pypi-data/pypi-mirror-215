from alphagram import Alpha, filters
from ..Database.coins import get_coins
from . import capsify

@Alpha.on_message(filters.command('coins') & filters.group)
async def coins(_, m):
  user_id = m.from_user.id
  chat_id = m.chat.id
  title = m.chat.title
  this_coins = await get_coins(user_id, chat_id=chat_id)
  global_coins = await get_coins(user_id)
  txt = capsify("coins in") + '\n\n'
  txt += f'{title} : `{this_coins}`\n'
  txt += f'{capsify("global")} : `{global_coins}`'
  await m.reply(txt)
                      
