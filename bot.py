# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 00:18:49 2021

@author: cetyz
"""

import os
import ast
import asyncio
import random
import string
import numpy as np
import requests
from dotenv import load_dotenv
import discord
from discord.ext import commands

from wrapper import get_axie_market_list, get_breed_count
from breeding_functions import get_expected_revenue, get_breeding_cost

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = os.getenv('DISCORD_GUILD_ID')

# print(TOKEN)
# print(GUILD)
# print(GUILD_ID)

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    # for guild in bot.guilds:
    #     print(f'{guild.name} (id: {guild.id})')

# def is_in_guild():
#     def predicate(ctx):
#         return 'CETYZ scholarship' in ctx.guilds
#     return(commands.check(predicate))


@bot.command(name='breed', help='To be filled in')
async def breed(ctx, *, arg):
       
    
    ids = arg.split('|')
    axie1_id = int(ids[0])
    axie2_id = int(ids[1])
    expected_usd, expected_eth = get_expected_revenue(axie1_id, axie2_id, True)
    # expected_usd, expected_eth = 200, 0.05
    axie1_breed_count = get_breed_count(axie1_id)
    axie2_breed_count = get_breed_count(axie2_id)

    output_str = 'Breeds | Axie 1 Breeds | Axie 2 Breeds | USD Cost | USD Rev | ETH Cost | ETH Rev'
    
    breeds = 1
    axie1_breeds, axie2_breeds = axie1_breed_count, axie2_breed_count
    while (axie1_breeds < 7) and (axie2_breeds < 7):
        usd_cost, eth_cost = get_breeding_cost(axie1_breeds, axie2_breeds)
        usd_cost, eth_cost = np.round(usd_cost, 2), np.round(eth_cost, 4)
        usd_rev, eth_rev = np.round(expected_usd, 2), np.round(expected_eth, 4)
        
        built_str = '\n'+str(breeds)+' | '+str(axie1_breeds)+' | '+str(axie2_breeds)+' | '+str(usd_cost)+' | '+str(usd_rev)+' | '+str(eth_cost)+' | '+str(eth_rev)
    
        output_str += built_str
        
        axie1_breeds += 1
        axie2_breeds += 1
        breeds += 1


        
    embed = discord.Embed(
        title='Breeding Predictions',
        # description='Price: {}\nUSD: {}'.format(                    
            # np.round(float(axie['auction']['currentPrice'])/10e18, 4),
            # axie['auction']['currentPriceUSD']
        # ),
        # url='https://marketplace.axieinfinity.com/axie/'+axie['id']
    )
    # embed.set_image(url=axie['image'])
    # embed.image.height=200
    # embed.image.width=200
    # embed.set_thumbnail(url=axie['image'])
    
    
    
    embed.add_field(name='Results', value=output_str)
    
    # embed.add_field(name='Back', value=axie['parts'][2]['name'])
    # embed.add_field(name='Mouth', value=axie['parts'][3]['name'])
    # embed.add_field(name = chr(173), value = chr(173))
    # embed.add_field(name='Horn', value=axie['parts'][4]['name'])
    # embed.add_field(name='Tail', value=axie['parts'][5]['name'])
    # embed.add_field(name = chr(173), value = chr(173))
    
    await ctx.send(

        embed=embed
        )


@bot.command(name='quick_search', help='To be filled in')
async def quick_search(ctx, *, arg):
    
    classes = None
    parts = None
    pureness = None
    breed_count = None
    hp = None
    skill = None
    speed = None
    morale = None  
    
    eligible = [
        'classes',
        'parts',
        'pureness',
        'breed_count',
        'hp',
        'skill',
        'speed',
        'morale'
    ]
    
    criteria = arg.split('|')
    for criterion in criteria:
        
        key, value = criterion.split('=')
        
        if key not in eligible:
            return(await ctx.send(f'{key} is not a valid criteria'))
        
        try:
            list_val = ast.literal_eval(value)
        except ValueError:
            return(await ctx.send(f'Could not parse criterion value for {key}'))
        
        if key == 'classes':
            classes = list_val
        elif key == 'parts':
            parts = list_val
        elif key == 'pureness':
            pureness = list_val
        elif key == 'breed_count':
            breed_count = list_val
        elif key == 'hp':
            hp = list_val
        elif key == 'skill':
            skill = list_val
        elif key == 'speed':
            speed = list_val
        elif key == 'morale':
            morale = list_val
            
            
    axies = get_axie_market_list(
        size=5,
        classes=classes,
        parts=parts,
        pureness=pureness,
        breed_count=breed_count,
        hp=hp,
        skill=skill,
        speed=speed,
        morale=morale
    )
        
    
    # await ctx.send('Done')
    
    # for i in list_arg:
    #     await ctx.send(i)
        
    
    # axies = get_axie_market_list(args)
    
    for axie in axies:
        
        # raw_image = requests.get(axie['image']).content
        
        embed = discord.Embed(
            title='View in Marketplace',
            description='Price: {}\nUSD: {}'.format(                    
                np.round(float(axie['auction']['currentPrice'])/10e18, 4),
                axie['auction']['currentPriceUSD']
            ),
            url='https://marketplace.axieinfinity.com/axie/'+axie['id']
        )
        # embed.set_image(url=axie['image'])
        # embed.image.height=200
        # embed.image.width=200
        embed.set_thumbnail(url=axie['image'])
        
        embed.add_field(name='Back', value=axie['parts'][2]['name'])
        embed.add_field(name='Mouth', value=axie['parts'][3]['name'])
        embed.add_field(name = chr(173), value = chr(173))
        embed.add_field(name='Horn', value=axie['parts'][4]['name'])
        embed.add_field(name='Tail', value=axie['parts'][5]['name'])
        embed.add_field(name = chr(173), value = chr(173))
        
        await ctx.send(

            embed=embed
        )

@bot.command(name='set_alert')
async def set_alert(ctx, *, arg):
    
    alert_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
    
    classes = None
    parts = None
    pureness = None
    breed_count = None
    hp = None
    skill = None
    speed = None
    morale = None  
    
    eligible = [
        'classes',
        'parts',
        'pureness',
        'breed_count',
        'hp',
        'skill',
        'speed',
        'morale'
    ]
    
    criteria = arg.split('|')
    for criterion in criteria:
        
        key, value = criterion.split('=')
        
        if key not in eligible:
            return(await ctx.send(f'{key} is not a valid criteria'))
        
        try:
            list_val = ast.literal_eval(value)
        except ValueError:
            return(await ctx.send(f'Could not parse criterion value for {key}'))
        
        if key == 'classes':
            classes = list_val
        elif key == 'parts':
            parts = list_val
        elif key == 'pureness':
            pureness = list_val
        elif key == 'breed_count':
            breed_count = list_val
        elif key == 'hp':
            hp = list_val
        elif key == 'skill':
            skill = list_val
        elif key == 'speed':
            speed = list_val
        elif key == 'morale':
            morale = list_val
            
    _alert = True
    while _alert:
            
        axies = get_axie_market_list(
            size=5,
            classes=classes,
            parts=parts,
            pureness=pureness,
            breed_count=breed_count,
            hp=hp,
            skill=skill,
            speed=speed,
            morale=morale
        )
        
    
        for axie in axies:
            
            # raw_image = requests.get(axie['image']).content
            
            embed = discord.Embed(
                title='View in Marketplace',
                description='Price: {}\nUSD: {}'.format(                    
                    np.round(float(axie['auction']['currentPrice'])/10e18, 4),
                    axie['auction']['currentPriceUSD']
                ),
                url='https://marketplace.axieinfinity.com/axie/'+axie['id']
            )
            # embed.set_image(url=axie['image'])
            embed.set_thumbnail(url=axie['image'])
            
            embed.add_field(name='Back', value=axie['parts'][2]['name'])
            embed.add_field(name='Mouth', value=axie['parts'][3]['name'])
            embed.add_field(name = chr(173), value = chr(173))
            embed.add_field(name='Horn', value=axie['parts'][4]['name'])
            embed.add_field(name='Tail', value=axie['parts'][5]['name'])
            embed.add_field(name = chr(173), value = chr(173))
            
            
            await ctx.send(

                embed=embed
            )
        await ctx.send(
            'Alert ID: {}\nSend stop_alert_{} or stop_all_alerts to stop this alert\n'.format(
                alert_id,
                alert_id
            )
            
        )    

        def check(m):
            return not m.author.bot and \
                ((m.content == "stop_alert_"+alert_id) or (m.content.lower() == "stop_all_alerts"))
        
        try:
            if await bot.wait_for('message', check=check, timeout=1800):
                _alert = False
                await ctx.send("Stopping alert {}".format(alert_id))
        except asyncio.TimeoutError:
            pass
        



    
bot.run(TOKEN)

