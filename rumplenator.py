from twitchio.ext import commands
import os
import sys
from collections import defaultdict
from random import randint
import time

def readfile(fn):
    f = open(fn, "r")
    quotesdict = defaultdict(lambda:[])
    for line in f:
        line = line.split('#')[0].strip()
        if line =='': continue   
        instance = line.split()
        category = instance[0]
        quote = instance[1:]
        quotesdict[category].extend([quote])

    return quotesdict
        
dysontext = sys.argv[1]

quotes = readfile(dysontext)
params = list(quotes.keys())

def get_dyson_message(param=''):
    if param == '':
        param = params[randint (0,len(params)-1)]
    if param in params:
        return (' '.join(quotes[param][randint(0, len(quotes[param])-1)])).encode("utf-8").decode("utf-8")
    else:
        return 'We currently do not have that in stock. Please choose from our current range: hand, heat, dry, fan, style, and vac.'



class Bot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token=os.environ['TMI_TOKEN'], client_id=os.environ['CLIENT_ID'], nick=os.environ['BOT_NICK'], prefix=os.environ['BOT_PREFIX'], initial_channels=[os.environ['CHANNEL']])

     #Events don't need decorators when subclassed
    async def event_ready(self):
        print(f'Ready | {self.nick}')
        ws = bot._ws
        await ws.send_privmsg(os.environ['CHANNEL'], f"/me has landed!")

    async def event_message(self, message):
        print(message.content)
        await self.handle_commands(message)

    

    @commands.command(name='dyson')
    async def Dyson1(self, ctx):
        message = ''
        if len(ctx.content) > 6:
            param = ctx.content[7:]
            message = get_dyson_message(param)
        else:
            message = get_dyson_message()

        await ctx.send(message)

    @commands.command(name='onlyfans')
    async def Dyson2(self, ctx):
        message = get_dyson_message('fan')
        await ctx.send(f'FANS YOU SAY?')
        time.sleep(2)
        await ctx.send(message)


   # @commands.command(name='dyson')
    #async def undefined(self, ctx):
     #   if len(ctx.content) > 6:
      #      param = ctx.content[7:]
       #     if param in params:
        #        await ctx.send((' ').join(quotes[param][randint(0, len(quotes[param])-1)]).encode("utf-8").decode("utf-8"))
         #   else:
          #      await ctx.send(f' We currently do not have that in stock. Please choose from our current range: hand, heat, dry, fan, style, and vac.')
       # else:
        #    random_param = params[randint (0,len(params)-1)] 
         #   await ctx.send((' ').join(quotes[random_param][randint(0, len(quotes[random_param])-1)]).encode("utf-8").decode("utf-8"))    
  
    @commands.command(name='Hi')
    async def my_command(self, ctx):
        await ctx.send(f'Hello {ctx.author.name}!')


    @commands.command(name='kill')
    async def my_command2(self, ctx):
        await ctx.send(f'I cannot be killed™'.encode("utf-8").decode("utf-8"))

    @commands.command(name='flip')
    async def flipcommand(self, ctx):
        message = ctx.content
        if "!" not in message[1:]:
            await ctx.send(f'{ctx.content[:5:-1]}')
        else:
            await ctx.send(f'are you tryna do something sneaky..?')

    @commands.command(name='botlove')
    async def my_command3(self, ctx):
        await ctx.send(f'aaawh thank you {ctx.author.name} andrumHeart If I was sentient I would love you too! xxx')

    @commands.command(name='raid')
    async def my_command4 (self, ctx):
        await ctx.send(f' Rumple Raid! andrumHeart andrumHype Rumple Raid! andrumHeart andrumHype Rumple Raid! andrumHeart andrumHype Rumple Raid! andrumHeart andrumHype Rumple Raid! andrumHeart andrumHype Rumple Raid! andrumHeart andrumHype')

    @commands.command(name='ssimp')
    async def my_command5 (self, ctx):
        await ctx.send(f'does she speak? notice me. u r beetiful asian quenn. can i wife u? oh you have a bf? im out.')

    #async def event_message(message):
     # ctx = await bot.get_context(message=message)
      #if str(message.content).lower().startswith("hello"):
       #   await ctx.send(f'andrumHi {ctx.author.name}')

    @commands.command(name='simp')
    async def my_commandsimp(self, ctx):
        # Can be anywhere, or can set up a dedicated file import instead. Currently as a list.
        simp_quotes =["do you have onlyfans?", "do you talk?", "does she speak", "notice me senpai.", "u r beetiful asian quenn.", "can i wife u?", "oh you have a bf? im out.", "hiiiiooi can u be my girlfriend", "did it hurt when you fell from the vending machine cause you thicka then a snicka", "Burp for bits?"]
        await ctx.send(simp_quotes[randint(0, len(simp_quotes)-1)])

    @commands.command(name='wowie')
    async def wowie(self, ctx):
        await ctx.send(f'Thats awesome! But ur not just awesome, ur WOWIE! andrumHeart ')

    @commands.command(name='hype')
    async def hype(self, ctx):
        await ctx.send(f'andrumHype andrumHype andrumHype andrumHype andrumHype andrumHype andrumHype andrumHype andrumHype')

    @commands.command(name='MrSkwirl')
    async def Grantscommand(self, ctx):
        await ctx.send(f'Every Skwirl needs its NUT :peanuts:')

    @commands.command(name='mclovin')
    async def mclovinscommand(self, ctx):
        await ctx.send(f'According to Urban Dictionary Colored McLovin is the cutest E-girl known to man. His uwus have created peace in times of turmoil, and his gamer girl bath water quenched the thirst of people without clean water. McLovin truly is the queen of all.')

    @commands.command(name='tom2')
    async def undefined2(self, ctx):
        social_quotes = ["left your Raid Shadow Legend clan", "left your Minecraft server", "unfollowed your Goodreads", "downvoted your Allrecipes", 'unfollowed on twitch', "unsubbed on youtube", "unfriended on facebook", "un-starred on your github project", "rated 1 star on google maps", "downvoted on reddit"]
        BFlist = ['Tom is Rumple\'s boyfriend', 'Tom is Jay\'s better half', 'Tom is Rumple\'s bae']
        WTFlist = ['wtf boyfriend? ', 'ehw, a better half? ', 'urgh, bae? ']
        randnum = randint(0, len(BFlist)-1)
        await ctx.send(BFlist[randnum])
        time.sleep(3)
        await ctx.send(WTFlist[randnum] + social_quotes[randint(0, len(social_quotes)-1)])

    @commands.command(name='giveup')
    async def undefined3(self, ctx):
        await ctx.send(f'NEVER GIVE UP https://www.youtube.com/watch?v=tYzMYcUty6s&ab_channel=MetalGearFro')

    @commands.command(name='sleepy')
    async def mable(self, ctx):
        username = ctx.content[8:]
        await ctx.send(username+' is so so so sleeeepppyyyy!!!!')

    @commands.command(name='pat')   
    async def flawer(self, ctx):
        username = str(ctx.content[5:])
        await ctx.send(f'/me gentle pats on '+username+'\'s head. well done! you\'re doin great my friend (ｏ・・)ノ”(ᴗ ᴗ。) <3 ')

    @commands.command(name='dropkick')   
    async def Sky(self, ctx):
        username = str(ctx.content[10:])
        await ctx.send(f'/me '+username+f' has been dropkicked by {ctx.author.name} and sent into the abyss never to be loved again (•̀ᴗ•́ )و')

    @commands.command(name='dropkiss')   
    async def SKP(self, ctx):
        username = str(ctx.content[10:])
        await ctx.send(f'/me {ctx.author.name} has dropkissed '+username+' (on the cheeks cuz we are PG) and now '+username+ ' is not alone in this vast abyss  (ᵔᴥᵔ)')

    @commands.command(name='cointoss')   
    async def mabpl(self, ctx):
        flip = randint(0, 1)
        if (flip == 0):
            await ctx.send("Heads")
        else:
            await ctx.send("Tails")
        

bot = Bot()
bot.run()
