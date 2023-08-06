from . import _sort, capsify, get_readable_time
from alphagram import Alpha, filters
from alphagram.types import IKM, IKB
from ..Database.chats import get_served_chats
from ..Database.completed import incr_word
from ..Database.chat_words import incr_chat_word
from ..Database.coins import add_coins
from ..Database.global_stats import *
from ..Database.record import update_record
from config import SUPPORT_GROUP, WORD_SPAWN_TIME
from .watchers import fw_watcher
import words
from shivi import alpha
from .image import make_image
import asyncio
import time

dic = {} # status dict
last_sent = {} # queue dict

support_markup = IKM(
  [
    [
      IKB(capsify("Support"), url=f't.me/{SUPPORT_GROUP}')
    ]
  ]
)

def get_reward(t: float) -> int:
  if t <= 5:
    return 10
  if t <= 10:
    return 8
  if t <= 60:
    return 5
  return 3

@Alpha.on_message(filters.group, group=fw_watcher)
async def cwf(_, m):
  global dic
  if not m.chat:
    return
  chat_id = m.chat.id
  if chat_id not in dic:
    return
  if not m.from_user:
    return
  user_id = m.from_user.id
  if not m.text:
    return
  text = m.text
  if len(text.split()) != 1:
    return
  if text.lower() != dic[chat_id][0]:
    return
  tim = dic[chat_id][1]
  dic.pop(chat_id)
  txt = capsify('{}, you got `{}` coins.') + '\n\n' + capsify('time taken : `{}`.')
  men = m.from_user.mention
  time_taken = time.time() - tim
  tt = time_taken
  rew = str(get_reward(time_taken))
  time_taken = get_readable_time(int(tt))
  await _.send_message(chat_id, txt.format(men, rew, time_taken))
  await incr_word(user_id, chat_id)
  await incr_chat_word(chat_id, user_id)
  await incr_global_chat(chat_id)
  await incr_global_user(user_id)
  await update_record(user_id, tt)
  await add_coins(user_id, int(rew), chat_id)

async def send():
  global last_sent, dic
  _ = alpha
  while True:
    un = _.me.username
    chats = await get_served_chats()
    for x in chats:
      if x in last_sent:
        diff = int(time.time() - last_sent[x])
        if diff >= WORD_SPAWN_TIME:
          w = words.Word()
          im = make_image(w, un)
          try:
            await _.send_photo(x, im, caption=capsify('write the word above !'), reply_markup=support_markup)
            last_sent[x] = time.time()
            dic[x] = [w.lower(), time.time()]
          except:
            pass
      else:
        w = words.Word()
        im = make_image(w, un)
        try:
          await _.send_photo(x, im, caption=capsify('write the word above !'), reply_markup=support_markup)
          last_sent[x] = time.time()
          dic[x] = [w.lower(), time.time()]
        except:
          pass
    await asyncio.sleep(1)

asyncio.create_task(send())
