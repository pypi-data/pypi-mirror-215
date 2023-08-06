from alphagram import Alpha, filters
from alphagram.types import IKM, IKB
from config import SUPPORT_GROUP, SUPPORT_CHANNEL, OWNER_ID
from Spoiled.Database.users import add_served_user
from Spoiled.Database.coins import get_coins
from Spoiled.Database.completed import get_top_chat, get_completed_words
from Spoiled.Database.record import get_record
from . import capsify, get_readable_time, title

@Alpha.on_message(filters.command('start') & filters.private)
async def start(_, m):
  await add_served_user(m.from_user.id)
  txt = "Hello {}, Am {}, I sends an Image containing word in which one who completes that word quickly, will be rewarded coins.\n\nCheck info for source code and other Information."
  id = _.me.id
  un = _.me.username
  fn = _.me.first_name
  user_first_name = m.from_user.first_name
  markup = IKM(
      [
          [
              IKB(capsify("➕ Add me to your group ➕"), url=f't.me/{un}?startgroup=True')
          ],
          [
              IKB(capsify("Help 📘"), url=f't.me/{un}?start=help'),
              IKB(capsify("Hoster ☁️"), user_id=OWNER_ID)
          ],
          [
              IKB(capsify("Profile 👤"), callback_data='profile'),
              IKB(capsify("Leaderboard 🏆"), callback_data='leaderboard')
          ],
          [
              IKB(capsify("Info ℹ️"), callback_data='info'),
              IKB(capsify("Settings ⚙️"), callback_data='settings')
          ]
      ]
  )
  await m.reply(txt.format(user_first_name, fn), reply_markup=markup)

@Alpha.on_callback_query(filters.regex('backtostart'))
async def backtostart(_, q):
  txt = "Hello {}, Am {}, I sends an Image containing word in which one who completes that word quickly, will be rewarded coins.\n\nCheck info for source code and other Information."
  id = _.me.id
  un = _.me.username
  fn = _.me.first_name
  user_first_name = q.from_user.first_name
  markup = IKM(
      [
          [
              IKB(capsify("➕ Add me to your group ➕"), url=f't.me/{un}?startgroup=True')
          ],
          [
              IKB(capsify("Help 📘"), url=f't.me/{un}?start=help'),
              IKB(capsify("Hoster ☁️"), user_id=OWNER_ID)
          ],
          [
              IKB(capsify("Profile 👤"), callback_data='profile'),
              IKB(capsify("Leaderboard 🏆"), callback_data='leaderboard')
          ],
          [
              IKB(capsify("Info ℹ️"), callback_data='info'),
              IKB(capsify("Settings ⚙️"), callback_data='settings')
          ]
      ]
  )
  await q.answer()
  await q.edit_message_text(txt.format(user_first_name, fn), reply_markup=markup)

@Alpha.on_callback_query(filters.regex('profile'))
async def profile_cbq(_, q):
  await q.answer()
  await q.edit_message_text(capsify('getting your profile, please wait...'))
  user_id = q.from_user.id
  cns = await get_coins(user_id)
  txt = capsify('👤 User Profile')
  txt += '\n\n'
  words = await get_completed_words(user_id)
  txt += capsify('words completed :') + f' `{words}`.'
  txt += '\n'
  txt += capsify('coins :') + f' `{cns}`.'
  top_chat = await get_top_chat(user_id)
  if top_chat:
    top_chat = await title(int(top_chat))
  txt += '\n'
  txt += capsify('top chat :') + f' {top_chat}.'
  txt += '\n'
  txt += capsify('record :') + f' `{get_readable_time(int(await get_record(user_id)))}.`'
  markup = IKM(
    [
      [
        IKB(capsify("share profile"), switch_inline_query='share')
      ],
      [
        IKB(capsify('back'), callback_data='backtostart')
      ]
    ]
  )
  await q.edit_message_text(txt, reply_markup=markup)
  
  
