from alphagram import Alpha, filters
from ..Database.chat_words import get_top_chat_users
from alphagram.types import IKM, IKB
from . import capsify, mention, title

@Alpha.on_message(filters.command('leaderboard') & filters.group)
async def leaderboard(_, m):
  ok = await m.reply(capsify('getting leaderboard...'))
  chat_id = m.chat.id
  chat_title = m.chat.title
  x = await get_top_chat_users(chat_id)
  txt = capsify('top word completers in {}') + '\n\n'
  txt = txt.format(chat_title)
  a = 1
  for y in x:
    txt += f'`{a}.` {await mention(int(y))} [{x[y]}]\n'
    a += 1
    if a == 11:
      break
  markup = IKM(
    [
      [
        IKB(capsify('top by coins'), callback_data='topby_coins')
      ]
    ]
  )
  await ok.edit(txt, reply_markup=markup)
    
