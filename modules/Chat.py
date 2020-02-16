import datetime
import discord
from discord.ext import commands
import os
import sys
sys.path.append('..')
from Lib import Logger, result_embed, pluralize

text = '        \                           /\n' \
       '         \                         /\n' \
       '          \ Видимо кого-то послали/\n' \
       '           ]   на 3 буквы ...    [    ,"|\n' \
       '           ]                     [   /  |\n' \
       '           ]___               ___[ ,"   |\n' \
       '           ]  ]\    нахуй    /[  [ |:   |\n' \
       '           ]  ] \     ||    / [  [ |:   |\n' \
       '           ]  ]  ]    ||   [  [  [ |:   |\n' \
       '           ]  ]  ]__  \/   __[  [  [ |:   |\n' \
       '           ]  ]  ] ]\ _ /[ [  [  [ |:   |\n' \
       '           ]  ]  ] ] (Ты)[ [  [  [ :===="\n' \
       '           ]  ]  ]_].nHn.[_[  [  [\n' \
       '           ]  ]  ]  HHHHH. [  [  [\n' \
       '           ]  ] /   `HH("N  \ [  [\n' \
       '           ]__]/     HHH  "  \[__[\n' \
       '           ]         NNN         [\n' \
       '           ]         N/"         [\n' \
       '           ]         N H         [\n' \
       '          /          N            \ \n' \
       '         /           q,            \ \n' \
       '        /                           \ \n'

PREFIX = os.environ.get('PREFIX')

class Chat(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    logger = Logger()

    @commands.command(aliases=['cl'],
                      description='This command allows you to delete messages '
                                  'from the channel in which the command was called.\n'
                                  '- Usual variant -\n'
                                  'This option allows to delete n messages. If a user is mentioned at the end,'
                                  'then ONLY messages of the specified user will be deleted.'
                                  f' Example: {PREFIX}clear <Messages to search. This is not the number of messages !>'
                                  '<(optional)@ User whose messages you want to delete>.\n'
                                  '- Delete by date and time - \n'
                                  'This option allows you to delete all messages from the channel starting '
                                  'from the specified date and time. If you specify a user at the end,'
                                  ' they will delete ONLY past posts of the user '
                                  f'Example: {PREFIX}clear <(UTC TIME!)[hour] [min] [sec] [day] [mount] [year]> '
                                  '<(Optional)@User whose posts you want to delete>.',
                      brief='Delete N- number of messages from the channel.')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, *args):
        chan = ctx.message.channel
        if len(args) == 7:
            def check(msg):
                return msg.author == ctx.message.mentions[0]

            deleted = await chan.purge(check=check,
                                       after=datetime.datetime(int(args[5]), int(args[4]), int(args[3]),
                                                               int(args[0]), int(args[1]), int(args[2])))
        elif len(args) == 6:
            deleted = await chan.purge(
                after=datetime.datetime(int(args[5]), int(args[4]), int(args[3]),
                                        int(args[0]), int(args[1]), int(args[2])))
        elif len(args) == 2:
            def check(msg):
                return msg.author == ctx.message.mentions[0]

            deleted = await chan.purge(limit=int(args[0]), check=check)
        else:
            deleted = await chan.purge(limit=int(args[0]))

        # await chan.send('Удалено %s {}'.format(pluralize(len(deleted),
        #                                                  'сообщение', 'сообщения', 'сообщений')) % len(deleted))
        await result_embed('Успешно!', 'Удалено %s {}'
                           .format(pluralize(len(deleted), 'сообщение', 'сообщения', 'сообщений')) % len(deleted), ctx)
        self.logger.comm(f'CLEAR. Author: {ctx.message.author}')

    # noinspection SpellCheckingInspection
    emoji_react = ['<:jnJ6kEPEBQU:619899647669960714>', '<:image0:641676982651715584>',
                   '<:emoji_6:615000140423626754>', '<:OREHUS_YES:666640633502498865>']

    @commands.Cog.listener()
    async def on_message(self, message):
        for emo in self.emoji_react:
            if emo.lower() in message.content.lower():
                emoji = emo
                await message.add_reaction(emoji)
        self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.lower() == 'пошел нахуй' or message.content.lower() == 'нахуй пошел':
            await message.channel.send(f'```{text}```')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, _):
        for emo in self.emoji_react:
            if emo.lower() in str(reaction).lower():
                emoji = emo
                await reaction.message.add_reaction(emoji)


def setup(bot):
    bot.add_cog(Chat(bot))
