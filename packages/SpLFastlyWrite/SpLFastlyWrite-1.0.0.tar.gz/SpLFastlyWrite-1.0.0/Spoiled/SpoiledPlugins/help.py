from alphagram import Alpha, filters
from config import OWNER_ID, SUPPORT_GROUP, SUPPORT_CHANNEL
from Spoiled import CODE_OWNER_ID
from . import capsify
from alphagram.types import IKM, IKB

@Alpha.on_message(filters.command('help') & filters.private)
async def help(_, m):
  txt = f'**{capsify("commands")}**\n\n'
  txt += f'`/leaderboard` - {capsify("to get the top players [only groups].")}\n'
  txt += f'`/coins` - {capsify("to display your coins [only groups].")}\n'
  txt += '\n'
  txt += f'**{capsify("bot owner contact")}**\n\n'
  group = capsify('group')
  channel = capsify('channel')
  txt += f'{group} : @{SUPPORT_GROUP}\n'
  txt += f'{channel} : @{SUPPORT_CHANNEL}\n'
  txt += '\n'
  txt += f'**{capsify("code owner contact")}**\n\n'
  txt += f'{group} : @Spoiled_Community\n'
  txt += f'{channel} : @SpLBots\n'
  markup = IKM(
      [
          [
              IKB(capsify('bot owner'), user_id=OWNER_ID)
          ],
          [
              IKB(capsify('code owner'), user_id=CODE_OWNER_ID)
          ]
      ]
  )
  await m.reply(txt, reply_markup=markup)
