import requests
import os
from dotenv import load_dotenv

load_dotenv()

#Getting access to API
FACEIT_KEY = os.getenv('FACEIT')
headers = {
  'Authorization': 'Bearer ' + FACEIT_KEY,
  'accept': 'application/json'
}


#Getting player data
def getData(nickname : str):
  url = "https://open.faceit.com/data/v4/players?nickname="+nickname
  response = requests.request("GET", url, headers=headers)
  data = response.json()
  player_id = data['player_id']
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

  return player_id, player_avatar, player_nickname, lastMatches, player_csgo_elo, player_csgo_level, csgo_lastMatch_id, lastMatchesStats