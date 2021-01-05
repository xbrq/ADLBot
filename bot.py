# reference file; this is what bot.me should turn into after the Boner++ interpreter is done with it
# see the repo Boner++ for more information

import discord
import asyncio
import logging
from discord.ext import commands
from discord.ext.commands import Bot
import traceback
import sys

import os
import discord
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

import csv

with open("wordlist.csv", "r") as f:
    file = csv.reader(f)
    wordlist = list(file)[0]

description = """ADLBot"""

inline_bot = discord.Client()

@inline_bot.event
async def on_ready():
    print('logged in as: ')
    print(inline_bot.user.name)
    print(inline_bot.user.id)
    print('-----')
    activity = discord.Activity(name='Watching for hate speech', type=4)
    await inline_bot.change_presence(activity=activity)

# function to generate all the sub lists 
def sub_lists(l): 
    subsequences = []
    for i in range(len(l)):
      for j in range(1,len(l)+1):
        if l[i:j] != []:
            subsequences.append(l[i:j])
    return subsequences

@inline_bot.event
async def on_message(message):
    if message.author.bot or message.channel.id != 300377971234177024:
        return
    content = message.content
    words = sub_lists(content.split(' '))
    for i in range(len(words)):
        phrase = words[i]
        if len(phrase) == 1:
            words[i] = str(phrase[0])
        else:
            words[i] = ' '.join(phrase)
    reply = ""
    for word in words:
        if word in wordlist:
            if word.count(' ') != 0:
                reply += "<@" + str(message.author.id) + ">, the phrase `" + str(word) + "` is recognized by the ADL as a hate symbol. Israeli drone strikes will soon reach your location. :flag_il::rocket::fire:\n"
            else:
                reply += "<@" + str(message.author.id) + ">, the word `" + str(word) + "` is recognized by the ADL as a hate symbol. Israeli drone strikes will soon reach your location. :flag_il::rocket::fire:\n"
    if reply != '':
        await message.channel.send(reply)

inline_bot.run(TOKEN)

