# FACEIT last match stats BOT

This BOT, written in Python, sends a discord message to certain channel with info about your last CS:GO match on FACEIT.

![Teaser](https://raw.githubusercontent.com/mpn01/faceit-lastmatch-bot/master/README/videos/teaser.gif)


### How to install it?

At this moment to use it, you need to have an account on [FACEIT for Developers](https://developers.faceit.com) and your own Discord server.

Create your Discord BOT on [Discord for Developers site](https://discord.com/developers) and add it to your server.
Then, download files from `/src` folder from this repo, create `.env` file and paste this:

```env
FACEIT='%faceit_token%'
DISCORD='%discord_token%'
```

Then run in terminal `python3 main.py`, this will turn on the bot.

### How it works?
To show your last match just simply type `!lastmatch %nicnkame%`. BOT will send:
* Score of the match
* Which level you have
* How many ELO points you have
* How many kills you did
* Your K/D Ratio
* Headshot %
