from .watchers import served_watcher
from alphagram import Alpha, filters
from ..Database.chats import add_served_chat
from ..Database.users import add_served_user
from ..Database.user_chat_info import update_chat_info, update_user_info

@Alpha.on_message(group=served_watcher)
async def cwf(_, m):
  if m.from_user:
    await add_served_user(m.from_user.id)
    details = {}
    details["first_name"] = m.from_user.first_name
    details["last_name"] = m.from_user.last_name if m.from_user.last_name else None
    details["username"] = m.from_user.username if m.from_user.username else None
    await update_user_info(m.from_user.id, details)
  if m.chat.id < 0:
    await add_served_chat(m.chat.id)
    chat_details = {}
    chat_details["title"] = m.chat.title
    await update_chat_info(m.chat.id, chat_details)
