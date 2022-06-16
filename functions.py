import asyncio
import re
import g
from discord.ext import tasks

@tasks.loop()
async def claimTimer():
    if claimTimer.current_loop == 0: #we dont want it to actually activate on first loop
        pass

    elif claimTimer.current_loop == 1: #after the first, we set to regular schedule
        g.abilities['claim'] = True
        claimTimer.change_interval(seconds =  3 * 3600)
    else:
        g.abilities['claim'] = True

@tasks.loop(count = 2)
async def dailyTimer():
    if dailyTimer.current_loop == 0:
        pass

    else:
        g.abilities['daily'] = True

@tasks.loop(count = 2)
async def kakTimer():
    if kakTimer.current_loop == 0:
        pass
    
    else:
        g.abilities['kak'] = True

@tasks.loop()
async def rollTimer( message):
    if rollTimer.current_loop == 0:
        pass
    
    else: 
        time = await roll(8, message)
        rollTimer.change_interval(seconds = 3600 - time)
        

async def roll(numRolls, message):
    time = 0
    for i in range(numRolls):
        if g.abilities['claim']:
            await asyncio.sleep(3)
            await message.channel.send('$wa')
            time += 3

        else:
            break

    if g.abilities['claim'] and g.abilities['daily']: #we could get a daily off
        await asyncio.sleep(2.5)
        dailyTimer.change_interval(seconds = 20 * 3600)
        dailyTimer.start()
        g.abilities['daily'] = False
        await message.channel.send('$daily')
        await asyncio.sleep(2.5)
        time += 5
        await message.channel.send('$rolls')
        for i in range(8):
            if g.abilities['claim']:
                await asyncio.sleep(3)
                await message.channel.send('$wa')
                time += 3

            else:
                break
    return time

def parseCooldown(cooldown):
    if len(cooldown) == 2:
        cooldown[0] = int(cooldown[0][0]) * 3600
        cooldown[1] = int(cooldown[1]) * 60
        cooldown = cooldown[0] + cooldown[1]

    else:
        cooldown = int(cooldown[0]) * 60

    return cooldown

async def noMessageClaim(message,valString):
    val = int(valString[2:len(valString)])
    if val >= 350 and g.abilities['claim']: #this does not have claim to react message btw
        for i in range(2): #try this twice in case of lag
            await asyncio.sleep(0.3) #wait for the reactions to show up (if any)
            if len(message.reactions) != 0:
                for i in message.reactions:
                    await message.add_reaction(i.emoji)
            
            else:
                await message.add_reaction('🥰')
        
        print('we got a character')
        g.abilities['claim'] =  False

async def startTimers(message): #from this content, derive all the timings
    if g.initialize:
        pass
    
    else:
        g.initialize = True
        content = message.content

        #check claimtimer

        claimCheck= re.search('you __can__ claim right now\!',content)
        if claimCheck:
            g.abilities['claim'] = True
            cooldown = re.search('The next claim reset is in \*\*(.+)\*\* min', content).group(1).split(' ')
            cooldown = parseCooldown(cooldown)
            claimTimer.change_interval(seconds = cooldown)
            claimTimer.start()

        else:
            cooldown = re.search('you can\'t claim for another \*\*(.+)\*\* min\.', content).group(1).split(' ')
            cooldown = parseCooldown(cooldown)
            claimTimer.change_interval(seconds = cooldown)
            claimTimer.start()

        #check daily timer

        dailyCheck = re.search('\$daily is available\!', content)
        if dailyCheck:
            g.abilities['daily'] = True
        else:
            cooldown = re.search('Next \$daily reset in \*\*(.+)\*\* min', content).group(1).split(' ')
            cooldown = parseCooldown(cooldown)
            dailyTimer.change_interval(seconds = cooldown)
            dailyTimer.start()

        #check kak timer

        kakCheck = re.search('You __can__ react to kakera right now\!', content)
        if kakCheck:
            g.abilities['kak'] = True

        else:
            cooldown = re.search('You can\'t react to kakera for \*\*(.+)\*\* min', content).group(1).split(' ')
            cooldown = parseCooldown(cooldown)
            kakTimer.change_interval(seconds = cooldown)
            kakTimer.start()


        #check roll timer

        numRolls = int(re.search('You have \*\*(\d+)\*\* roll.? left', content).group(1)) 
        await roll(numRolls, message)
        cooldown = re.search('Next rolls reset in \*\*(.+)\*\* min', content).group(1).split(' ')
        cooldown = parseCooldown(cooldown)
        rollTimer.change_interval(seconds = cooldown + 500) #we dont want to start rolling right on the dot
        rollTimer.start(message)
