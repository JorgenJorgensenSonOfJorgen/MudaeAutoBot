#A discord bot requiring discord.py-self package. It will roll, claim, claim kak, and use daily. The kakera claiming feature on this bot is very limited, and daily can be improved
#bot should be reset every now and then as the timers will become out of sync after a while.
import discord
from functions import *
client = discord.Client(self_bot = True)

@client.event
async def on_ready():
    print('online')
    #set the timer now
    channel = await client.fetch_channel(982171971620053062) #we send to a particular channel
    while not g.initialize: #continue until we get the tu off
        await channel.send('$tu')
        await asyncio.sleep(5)

@client.event
async def on_message(message):
    if message.author.id == 432610292342587392 and message.guild.id == 777661139474710538: #if it appears to be a roll from mudae on proper server
        if message.content.startswith('**{}**, you __can__ claim right now!'.format(client.user.name)) or message.content.startswith('**{}**, you can\'t claim for another'.format(client.user.name)):
            await startTimers(message)

        elif message.embeds:
            emb = message.embeds[0]
            desc = emb.description.split('\n')
            if desc[len(desc)-1] == 'React with any emoji to claim!' and g.abilities['claim']:# we know this is a roll
                kakeraString = desc[len(desc)-2]
                val =int(re.search('\d+', kakeraString).group())
                if val >= 350 :# we want to claim this with any emoji
                    await asyncio.sleep(0.6)
                    await message.add_reaction('🥰')
                    print('we got a character')
                    g.abilities['claim'] = False
                    
            else: #might not even be a roll, we can check using regex
                kakeraString = desc[len(desc)-1]
                val = re.search('^\*\*\d+',kakeraString)
                if val != None: #the last thing is kakera in the correct form as well so we know this is a roll
                    if emb.footer.text != discord.Embed.Empty: 
                        if 'Belongs to' in emb.footer.text and g.abilities['kak']: #is already claimed roll, claim the kakera. We should eventually check to see if the kakera is of good enough quality too, but later.
                            for i in range(2): #try this twice in case of lag
                                await asyncio.sleep(0.3) #wait for the reactions to show up
                                for i in message.reactions:
                                    await message.add_reaction(i.emoji)
                            
                            print('kakeraaa')
                            g.abilities['kak'] = False
                            await asyncio.sleep(3600 * 5)
                            g.abilities['kak'] = True

                        else: #bs footer
                            
                            await noMessageClaim(message,val.group())

                    else: #could be either heart react or wish/perstogglereact 
                    
                        await noMessageClaim(message,val.group())


#tidyrice2 = Nzk2NDQwMjEyMzQzMzU3NDgw.YmMjKA.EDptsqQAQMNqK1eBUUqBHunjsSU
#neo = 
#johnwayne = OTYyODQxMjU1NTQzNDU1ODM0.YmOD4g.YefKx6-G6s7HNj37ZG1f92w1q_M
client.run('OTcxNDkxMTQzMzg2ODA0MzA1.Gsp_gM.ptJAx-OYKvDlL_gSaLGuOq-KQhPuW6tKKblvQA')