from ..Database.coins import get_coins
from . import capsify, get_readable_time, title
from Spoiled.Database.completed import get_top_chat, get_completed_words
from Spoiled.Database.record import get_record
from alphagram import Alpha, filters
from alphagram.types import InlineQueryResultArticle as IQRA, InputTextMessageContent as ITMC, IKM, IKB


@Alpha.on_inline_query()
async def inline(_, i):
  query = i.query
  if query == 'share':
    user_id = i.from_user.id
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
        ]
      ]
    )
    res = [IQRA(title=capsify("profile"), description=capsify('share your profile !'), input_message_content=ITMC(txt), reply_markup=markup)]
    await _.answer_inline_query(i.id, results=res, cache_time=0)
