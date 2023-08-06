from Spoiled.Database.user_chat_info import get_user_info, get_chat_info

def _sort(set):
    for y in set:
      set[y] = int(set[y])
    x = sorted(set.items(), key=lambda x:x[1])
    x.reverse()
    final = {}
    for y in x:
        final[y[0]] = y[1]
    return final

ALPHABETS = "abcdefghijklmnopqrstuvwxyz"
ALL_CAPS = "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"

def capsify(text):
  txt = ""
  for x in text.split():
    for y in x:
      if y.lower() in ALPHABETS:
        ind = ALPHABETS.index(y.lower())
        txt += ALL_CAPS[ind]
      else:
        txt += y
    txt += " "
  return txt

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time

async def mention(user_id: int) -> str:
    name = await get_user_info(user_id)
    name = name.get('first_name', 'Anonymous')
    st = f'[{name[:25]}](tg://user?id={user_id})'
    return st
    
async def title(chat_id: int) -> str:
    title = await get_chat_info(chat_id)
    title = title.get('title', 'Unknown')
    return title
