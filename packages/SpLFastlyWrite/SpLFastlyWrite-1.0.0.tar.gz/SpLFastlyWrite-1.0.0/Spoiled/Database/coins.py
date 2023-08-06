from . import database

db = database()

cdb = db.coins

async def add_coins(user_id: int, coins: int, chat_id: int):
  chat_id = str(chat_id)
  x = await cdb.find_one({"user_id": user_id})
  if x:
    dic = x['dic']
  else:
    dic = {}
  if chat_id in dic:
    dic[chat_id] += coins
  else:
    dic[chat_id] = coins
  dic = await _get()
  if str(user_id) in dic:
    dic[str(user_id)] += coins
  else:
    dic[str(user_id)] = coins
  await update(dic)
  dic = await _get_chat()
  if chat_id in dic:
    dic[chat_id] += coins
  else:
    dic[chat_id] = coins
  await update_chat(dic)
  await cdb.update_one({"user_id": user_id}, {"$set": {"dic": dic}}, upsert=True)

async def get_coins(user_id: int, chat_id: int = None):
  if chat_id:
    chat_id = str(chat_id)
  x = await cdb.find_one({"user_id": user_id})
  if x:
    dic = x['dic']
    if chat_id:
      re = dic.get(chat_id, 0)
      return re
    tot = 0
    for y in dic:
      tot += dic[y]
    return tot
  return 0
      

ddb = db.coins_dict

async def update(dic):
    await ddb.update_one({"_": "_"}, {"$set": {"coins": dic}}, upsert=True)

async def _get():
    x = await ddb.find_one({"_": "_"})
    if x:
        return x["coins"]
    return {}

idb = db.coins_dict_chat

async def update_chat(dic):
    await idb.update_one({"_": "_"}, {"$set": {"coins": dic}}, upsert=True)

async def _get_chat():
    x = await idb.find_one({"_": "_"})
    if x:
        return x["coins"]
    return {}
