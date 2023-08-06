from . import capsify, _sort, mention, title
from alphagram.types import IKM, IKB
from alphagram import Alpha, filters
from ..Database.privacy import *
from ..Database.chats import get_served_chats
from ..Database.users import get_served_users
from ..Database.global_stats import get_users_dic, get_chats_dic
from ..Database.chat_words import get_top_chat_users
from ..Database.user_chat_info import get_user_info, get_chat_info
from ..Database.coins import _get, _get_chat
from .templates import info_template
from Spoiled import CODE_OWNER_ID

@Alpha.on_callback_query(filters.regex('leaderboard'))
async def leaderboard_cbq(_, q):
  markup = IKM(
    [
      [
        IKB(capsify('users'), callback_data='users'),
        IKB(capsify('chats'), callback_data='chats')
      ],
      [
        IKB(capsify("back"), callback_data="backtostart")
      ]
    ]
  )
  await q.answer()
  await q.edit_message_text(capsify('» private accounts will be hidden.') + '\n\n' + capsify('choose from below !'), reply_markup=markup)

@Alpha.on_callback_query(filters.regex('info'))
async def info_cbq(_, q):
  chats = str(len(await get_served_chats()))
  users = str(len(await get_served_users()))
  txt = info_template(chats, users)
  markup = IKM(
    [
      [
        IKB(capsify('owner'), user_id=CODE_OWNER_ID),
        IKB(capsify('channel'), url='t.me/SpLBots')
      ],
      [
        IKB(capsify('group'), url='t.me/Spoiled_Community'),
        IKB(capsify('source'), url='github.com/ShutupKeshav/SpLFastlyWrite')
      ],
      [
        IKB(capsify('back'), callback_data='backtostart')
      ]
    ]
  )
  await q.answer()
  await q.edit_message_text(txt, reply_markup=markup)

@Alpha.on_callback_query(filters.regex('settings'))
async def settings_cbq(_, q):
  user_id = q.from_user.id
  x = await get_private_users()
  priv = True if user_id in x else False
  enab = capsify("enabled 🔘") if priv else capsify("enabled")
  disab = capsify("disabled") if priv else capsify("disabled 🔘")
  markup = IKM(
    [
      [
        IKB(capsify('privacy 🔒'), callback_data='privacy_answer')
      ],
      [
        IKB(enab, callback_data='enable'),
        IKB(disab, callback_data='disable')
      ],
      [
        IKB(capsify('back'), callback_data='backtostart')
      ]
    ]
  )
  txt = capsify('⚙️ settings') + '\n\n'
  txt += capsify('privacy enabled » your profile will be private.') + '\n'
  txt += capsify('privacy disabled » your profile will be public.') + '\n\n'
  txt += capsify('choose from below !')
  await q.answer()
  await q.edit_message_text(txt, reply_markup=markup)

@Alpha.on_callback_query(filters.regex('privacy_answer'))
async def privacy_answer_cbq(_, q):
  txt = 'use buttons below to toggle private mode !'
  await q.answer(capsify(txt), show_alert=True)

@Alpha.on_callback_query(filters.regex('users') | filters.regex('users_'))
async def users(_, q):
  if q.data == 'users':
    x = await get_private_users()
    dic = await get_users_dic()
    dic = _sort(dic)
    a = 1
    txt = capsify('top users by words') + "\n\n"
    for y in dic:
      y = int(y)
      if y in x:
        continue
      txt += f'`{a}.` {await mention(y)} [`{dic[str(y)]}`]\n'
      a += 1
      if a >= 11:
        break
    markup = IKM(
      [
        [
          IKB(capsify('by coins'), callback_data='bycoinsusers')
        ],
        [
          IKB(capsify('back'), callback_data='leaderboard')
        ]
      ]
    )
    await q.answer()
    await q.edit_message_text(txt, reply_markup=markup)
  else:
    x = await get_private_users()
    dic = await _get()
    dic = _sort(dic)
    a = 1
    txt = capsify('top users by coins') + '\n\n'
    for y in dic:
      y = int(y)
      if y in x:
        continue
      txt += f'`{a}.` {await mention(y)} [`{dic[str(y)]}`]\n'
      a += 1
      if a >= 11:
        break
    markup = IKM(
      [
        [
          IKB(capsify('by words'), callback_data='users')
        ],
        [
          IKB(capsify('back'), callback_data='leaderboard')
        ]
      ]
    )
    await q.answer()
    await q.edit_message_text(txt, reply_markup=markup)

@Alpha.on_callback_query(filters.regex('chats') | filters.regex('chats_'))
async def chats(_, q):
  if q.data == 'chats':
    dic = await get_chats_dic()
    dic = _sort(dic)
    a = 1
    txt = capsify('top chats by words') + "\n\n"
    for y in dic:
      y = int(y)
      txt += f'`{a}.` {(await title(y))[:25]} [`{dic[str(y)]}`]\n'
      a += 1
      if a >= 11:
        break
    markup = IKM(
      [
        [
          IKB(capsify('by coins'), callback_data='chats_')
        ],
        [
          IKB(capsify('back'), callback_data='leaderboard')
        ]
      ]
    )
    await q.answer()
    await q.edit_message_text(txt, reply_markup=markup)
  else:
    dic = await _get_chat()
    dic = _sort(dic)
    a = 1
    txt = capsify('top chats by coins') + '\n\n'
    for y in dic:
      y = int(y)
      txt += f'`{a}.` {(await title(y))[:25]} [`{dic[str(y)]}`]\n'
      a += 1
      if a >= 11:
        break
    markup = IKM(
      [
        [
          IKB(capsify('by words'), callback_data='chats')
        ],
        [
          IKB(capsify('back'), callback_data='leaderboard')
        ]
      ]
    )
    await q.answer()
    await q.edit_message_text(txt, reply_markup=markup)

@Alpha.on_callback_query(filters.regex('enable') | filters.regex('disable'))
async def enab_priv(_, q):
  user_id = q.from_user.id
  data = q.data
  x = await get_private_users()
  if q.data == 'enable':
    if user_id in x:
      return await q.answer(capsify('private mode is already enabled !'), show_alert=True)
    await enable_privacy(user_id)
    priv = True
  else:
    if not user_id in x:
      return await q.answer(capsify('private mode is already disabled !'), show_alert=True)
    await disable_privacy(user_id)
    priv = False
  enab = capsify("enabled 🔘") if priv else capsify("enabled")
  disab = capsify("disabled") if priv else capsify("disabled 🔘")
  markup = IKM(
    [
      [
        IKB(capsify('privacy 🔒'), callback_data='privacy_answer')
      ],
      [
        IKB(enab, callback_data='enable'),
        IKB(disab, callback_data='disable')
      ],
      [
        IKB(capsify('back'), callback_data='backtostart')
      ]
    ]
  )
  await q.answer()
  await q.edit_message_reply_markup(reply_markup=markup)

@Alpha.on_callback_query(filters.regex('topby_'))
async def topby(_, q):
  data = q.data.split('_')[1]
  await q.answer()
  if data == 'coins':
    await q.edit_message_text(capsify('sorting top by coins, please wait...'))
    get = await _get()
    sor = _sort(get)
    chat_mem = []
    async for x in _.get_chat_members(q.message.chat.id):
      if not x.user.is_bot and not x.user.is_deleted:
        chat_mem.append(x.user.id)
    txt = capsify('top coins holders in {}') + '\n\n'
    txt = txt.format(q.message.chat.title)
    a = 1
    for y in sor:
      y = int(y)
      if not y in chat_mem:
        continue
      txt += f'`{a}.` {await mention(y)} [{sor[str(y)]}]\n'
      a += 1
      if a == 11:
        break
    markup = IKM(
      [
        [
          IKB(capsify('top by words'), callback_data='topby_words')
        ]
      ]
    )
    await q.edit_message_text(txt, reply_markup=markup)
  else:
    await q.edit_message_text(capsify('sorting top by words, please wait...'))
    chat_id = q.message.chat.id
    chat_title = q.message.chat.title
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
    await q.edit_message_text(txt, reply_markup=markup)
    
  
    
