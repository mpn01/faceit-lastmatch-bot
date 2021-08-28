import discord
import os
import requests
#import faceit
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
  url = "https://open.faceit.com/data/v4/players?nickname="+nickname
  response = requests.request("GET", url, headers=headers)
  data = response.json()
  player_id = str(data['player_id'])
  player_avatar = data['avatar']
  player_nickname = data['nickname']

  #Getting last match of player
  csgo_lastMatches_url = "https://open.faceit.com/data/v4/players/" + player_id + "/history?game=csgo&offset=0&limit=0"
  response_lastMatches = requests.request("GET", csgo_lastMatches_url, headers=headers)
  lastMatches = response_lastMatches.json()

  #Getting player stats
  csgo_stats_url = "https://open.faceit.com/data/v4/players/" + player_id + "/stats/csgo"
  response_stats = requests.request("GET", csgo_stats_url, headers=headers)
  stats = response_stats.json()

  #Getting player ELO points and current level
  player_csgo_elo = data['games']['csgo']['faceit_elo']
  player_csgo_level = data['games']['csgo']['skill_level']

  #Getting player last match
  csgo_lastMatch_id = lastMatches['items'][0]['match_id']
  csgo_lastMatch_stats_url = "https://open.faceit.com/data/v4/matches/" + str(csgo_lastMatch_id) + "/stats"
  response_lastMatchesStats = requests.request("GET", csgo_lastMatch_stats_url, headers=headers)
  lastMatchesStats = response_lastMatchesStats.json()


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

  #Finding certain player between all players
  for x in range(0, 2):
    for y in range (0, 5):
      if lastMatchesStats['rounds'][0]['teams'][x]['players'][y]['nickname'] == nickname:
        kills = lastMatchesStats['rounds'][0]['teams'][x]['players'][y]['player_stats']['Kills']
        kdratio = lastMatchesStats['rounds'][0]['teams'][x]['players'][y]['player_stats']['K/D Ratio']
        hspr = lastMatchesStats['rounds'][0]['teams'][x]['players'][y]['player_stats']['Headshots %']
        mapPlayed = lastMatchesStats['rounds'][0]['round_stats']['Map']
        score = lastMatchesStats['rounds'][0]['round_stats']['Score']

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

#client.run(DISCORD_KEY)