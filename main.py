import discord
import random 
from discord.ext import commands
import json
from urllib.request import urlopen
import os
import pandas as pd

# bot token 
Token=''

# bot prefix
bot = commands.Bot(command_prefix = '?') 

spell_map = {'Q':0,
             'W':1,
             'E':2,
             'R':3,
             'P':4}

champion_display_name = ''
spell_name = ''  
spellKey = ''

Wrong_answers = [
                 "lol Noob :joy:",
                 "REPORT :clown:",
                 "Omg report! :exploding_head: ",
                 "Uninstall plz :man_facepalming:",
                 "Omg Ape :monkey: ",
                 "KURWA :face_with_symbols_over_mouth: ",
                 "OMG NOOB :sob:",
                 "GET A LIFE! :disguised_face: ",
                 "Boosted Animal :ox:"]
        
       
@bot.event
async def on_ready():
    print('Ready...')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.HTTPException):
        await ctx.send("You are ratelimited")

@bot.command()
async def s(ctx): 
  '''
  Ask for a spell
  '''
  url = "http://ddragon.leagueoflegends.com/cdn/12.6.1/data/en_US/champion.json"
  response = urlopen(url)
  global champion_display_name
  global spell_name
  global spellKey  

  champions = []
  data_json = json.loads(response.read())

  for champion in data_json["data"]:
      champions.append(champion)
  champion_name = random.choice(champions)
  champion_display_name = data_json["data"][champion_name]["name"]
  print(champion_display_name)

  url = "https://ddragon.leagueoflegends.com/cdn/12.6.1/data/en_US/champion/"+champion_name+".json"
  response = urlopen(url)

  data_json = json.loads(response.read())
  # print(json.dumps(data_json, indent=2))
  spells = []  

  for spell in data_json["data"][champion_name]["spells"]:
      spells.append(spell["name"])
  spells.append(data_json["data"][champion_name]["passive"]["name"])


  spellKey = random.choice(['Q','W','E','R','P'])
  print(spellKey)
  champion_spell = spell_map[spellKey]
  print(champion_spell)

  if champion_spell == 4:
      spell_icon_name = data_json["data"][champion_name]["passive"]["image"]["full"]
      spell_name = data_json["data"][champion_name]["passive"]["name"]
      icon_url = "https://ddragon.leagueoflegends.com/cdn/12.6.1/img/passive/"+spell_icon_name  
  else:
      spell_icon_name = data_json["data"][champion_name]["spells"][champion_spell]["image"]["full"]
      spell_name = data_json["data"][champion_name]["spells"][champion_spell]["name"]
      icon_url = "https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/"+spell_icon_name
  embed=discord.Embed(title=":camera:  Spell icon", description="**GUESS THE CHAMPION AND THE SPELL KEY**\nex. Aatrox Q", color=discord.Color.blue())
  embed.set_thumbnail(url=icon_url)
  # embed.set_image(url=icon_url)
  await ctx.send(embed=embed)
                
@bot.command()
async def g(ctx, *args):  
  '''
  Give an answer
  '''
  global champion_display_name
  global spell_name   
  global spellKey 
  
  if champion_display_name == '':
    embed = discord.Embed(title="No spell to guess :zzz:", description="**Use ?s command**", color=discord.Color.red())
    await ctx.send(embed=embed)
    return
  
  if not args:
    embed = discord.Embed(title="No answers given", description="**Use format ?g Champion [spell key]\nex. Aatrox Q**", color=discord.Color.red())
    await ctx.send(embed=embed)
  elif len(args)==3:
    champion = str(args[0]+" "+args[1]).lower()
    spell = str(args[2]).lower() 
  elif len(args)==2:
    champion = str(args[0]).lower()
    spell = str(args[1]).lower()   
  else:
    embed = discord.Embed(title="Wrong Syntax!", description="**Use format ?g Champion [spell key]\nex. Aatrox Q**", color=discord.Color.red())
    await ctx.send(embed=embed)  
    return
  print(champion, spell)
  if champion == champion_display_name.lower():
    if spell == spellKey.lower():
      print("Success!  ") 
      embed = discord.Embed(title=ctx.author.display_name+" HAS WON !", description="Champion: **"+champion_display_name+"**\nSpell name: **"+spell_name+"**\nKey: **"+spellKey+"**", color=discord.Color.green())
      await ctx.send(embed=embed)
      champion_display_name=''
      spell_name=''
      spellKey=''
    else:
      print("Correct champion but wrong ability")
      embed = discord.Embed(title="Almost~ :sparkles:", description="Correct champion but wrong ability", color=discord.Color.orange())
      await ctx.send(embed=embed)
  else:
    print("nope")
    nope = random.choice(Wrong_answers)
    embed = discord.Embed(title=nope, description="**Try again**", color=discord.Color.red())
    await ctx.send(embed=embed)
    
@bot.command()
async def ff(ctx): 
  '''
  Give up
  '''
  global champion_display_name
  global spell_name   
  global spellKey
  if champion_display_name == '':
    embed = discord.Embed(title="No spell to guess :zzz:", description="**Use ?s command**", color=discord.Color.red())
    await ctx.send(embed=embed)
    return
  nope = random.choice(Wrong_answers)  
  embed = discord.Embed(title=nope, description="Champion: **"+champion_display_name+"**\nSpell name: **"+spell_name+"**\nKey: **"+spellKey+"**", color=discord.Color.green())
  await ctx.send(embed=embed)
  champion_display_name=''
  spell_name=''
  spellKey=''

@bot.command()
async def q(ctx): 
  '''
  Ask a history question
  '''
  global answer  
  seed = random.randint(0,3)
  answer = seed+1
  print(answer)

  # CSV file to be made by Dave
  df = pd.read_csv('Questions_History.csv')

  idx = random.randint(0,len(df['questions'])-1)

  question = df['questions'][idx]

  answers = [str(df['answers'][idx]), str(df['choice 2'][idx]), str(df['choice 3'][idx]), str(df['choice 4'][idx])]
  answers = answers[-seed:]+answers[:-seed]    
  embed=discord.Embed(title="Question: ", description=
                      "**"+str(question)+
                      "\n\n:one:"+answers[0]+
                      "\n:two:"+answers[1]+
                      "\n:three:"+answers[2]+
                      "\n:four:"+answers[3]+"**", 
                      color=discord.Color.blue())
  # embed.set_thumbnail(url=icon_url)
  # embed.set_image(url=icon_url)
  print("sent")
  await ctx.send(embed=embed)

@bot.command()
async def a(ctx, *args):  
  '''
  Give an answer for history question
  '''
  global answer
  
  if answer == '':
    embed = discord.Embed(title="No question to answer :zzz:", description="**Use ?q command**", color=discord.Color.red())
    await ctx.send(embed=embed)
    return
  
  if not args:
    embed = discord.Embed(title="No answers given", description="**Use format ?a [answer #]**", color=discord.Color.red())
    await ctx.send(embed=embed)
  elif len(args)==1:
    user_answer = int(args[0])  
  else:
    embed = discord.Embed(title="Wrong Syntax!", description="**Use format ?a [answer #]**", color=discord.Color.red())
    await ctx.send(embed=embed)  
    return
    
  print(answer)
  if user_answer == answer:
    print("Success!  ") 
    embed = discord.Embed(title=ctx.author.display_name+" HAS WON !", description="**Answer: "+str(answer)+"**", color=discord.Color.green())
    await ctx.send(embed=embed)
    answer=''
  else:
    print("nope")
    nope = random.choice(Wrong_answers)
    embed = discord.Embed(title=nope, description="**Try again**", color=discord.Color.red())
    await ctx.send(embed=embed)

    
bot.run(Token)