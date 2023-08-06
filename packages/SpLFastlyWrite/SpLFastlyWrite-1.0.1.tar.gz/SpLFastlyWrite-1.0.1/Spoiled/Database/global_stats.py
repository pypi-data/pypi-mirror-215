from . import database

db = database()

gdb = db.global_chats

async def incr_global_chat(chat_id: int):
  chat_id = str(chat_id)
  x = await gdb.find_one({"_": "_"})
  if x:
    dic = x['dic']
  else:
    dic = {}
  if chat_id in dic:
    dic[chat_id] += 1
  else:
    dic[chat_id] = 1
  await gdb.update_one({"_": "_"}, {"$set": {"dic": dic}}, upsert=True)

async def get_global_chat(chat_id: int):
  chat_id = str(chat_id)
  x = await gdb.find_one({"_": "_"})
  if x:
    dic = x['dic']
    if chat_id in dic:
      return dic[chat_id]
    return 0

async def get_chats_dic() -> dict:
  x = await gdb.find_one({"_": "_"})
  if x: 
    return x['dic']
  return {}

udb = db.global_users

async def incr_global_user(user_id: int):
  user_id = str(user_id)
  x = await udb.find_one({"_": "_"})
  if x:
    dic = x['dic']
  else:
    dic = {}
  if user_id in dic:
    dic[user_id] += 1
  else:
    dic[user_id] = 1
  await udb.update_one({"_": "_"}, {"$set": {"dic": dic}}, upsert=True)

async def get_global_user(user_id: int):
  user_id = str(user_id)
  x = await udb.find_one({"_": "_"})
  if x:
    dic = x['dic']
    if user_id in dic:
      return dic[user_id]
    return 0

async def get_users_dic() -> dict:
  x = await udb.find_one({"_": "_"})
  if x: 
    return x['dic']
  return {}
