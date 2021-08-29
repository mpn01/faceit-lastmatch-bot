import discord
import os
import requests
import faceit
from random import randint
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

bot = commands.Bot(command_prefix="!")
DISCORD_KEY = os.getenv('DISCORD')


FACEIT_KEY = os.getenv('FACEIT')
headers = {
  'Authorization': 'Bearer ' + FACEIT_KEY,
  'accept': 'application/json'
}

@bot.event
async def on_ready():
  print("I'm ready")

@bot.command()
async def lastmatch(ctx, nickname : str):

  #Getting player data
  data = faceit.getData(nickname)
  player_id = data[0]
  player_avatar = data[1]
  player_nickname = data[2]
  lastMatches = data[3]
  player_csgo_elo = data[4]
  player_csgo_level = data[5]
  csgo_lastMatch_id = data[6]
  lastMatchesStats = data[7]

  #Checking if player won or lost the match
  for x in range(0, 5):
    if lastMatches['items'][0]['teams']['faction1']['players'][x]['player_id'] != player_id:
      if lastMatches['items'][0]['teams']['faction2']['players'][x]['player_id'] == player_id:
        csgo_lastMatch_player_faction = "faction2"
    else:
      csgo_lastMatch_player_faction = "faction1"

  if lastMatches['items'][0]['results']['winner'] == csgo_lastMatch_player_faction:
    csgo_lastMatch_player_score = True
  else:
    csgo_lastMatch_player_score = False


  mapPlayed = lastMatchesStats['rounds'][0]['round_stats']['Map']
  score = lastMatchesStats['rounds'][0]['round_stats']['Score']
  #Finding certain player between all players
  for x in range(0, 2):
    for y in range (0, 5):
      if lastMatchesStats['rounds'][0]['teams'][x]['players'][y]['nickname'] == nickname:
        kills = lastMatchesStats['rounds'][0]['teams'][x]['players'][y]['player_stats']['Kills']
        kdratio = lastMatchesStats['rounds'][0]['teams'][x]['players'][y]['player_stats']['K/D Ratio']
        hspr = lastMatchesStats['rounds'][0]['teams'][x]['players'][y]['player_stats']['Headshots %']

  #channel = bot.get_channel(847137189133025321)
  if csgo_lastMatch_player_score == True:
    embed = discord.Embed(
      title = player_nickname,
      description = mapPlayed + " | " + score,
      colour = discord.Colour.green()
    )

    embed.set_thumbnail(url=str(player_avatar))
    embed.add_field(name = "Level", value=player_csgo_level, inline = True)
    embed.add_field(name = "ELO", value=player_csgo_elo, inline = True)
    embed.add_field(name = chr(173), value = chr(173))
    embed.add_field(name = "Kills", value=kills, inline = True)
    embed.add_field(name = "K/D ratio", value=kdratio, inline = True)
    embed.add_field(name = "HS %", value=hspr, inline = True)
    embed.add_field(name = "Match link", value="[CHECK IT ON FACEIT](https://www.faceit.com/pl/csgo/room/"+csgo_lastMatch_id+")", inline = False)

    await ctx.send(embed=embed)

  if csgo_lastMatch_player_score == False:
    embed = discord.Embed(
      title = player_nickname,
      description = mapPlayed + " | " + score,
      colour = discord.Colour.red()
    )

    embed.set_thumbnail(url=str(player_avatar))
    embed.add_field(name = "Kills", value=kills, inline = True)
    embed.add_field(name = "K/D ratio", value=kdratio, inline = True)
    embed.add_field(name = "HS %", value=hspr, inline = True)
    embed.add_field(name = "Level", value=player_csgo_level, inline = True)
    embed.add_field(name = "ELO", value=player_csgo_elo, inline = True)
    embed.add_field(name = "Match link", value="[CHECK IT ON FACEIT](https://www.faceit.com/pl/csgo/room/"+csgo_lastMatch_id+")", inline = False)

    await ctx.send(embed=embed)

bot.run(DISCORD_KEY)
