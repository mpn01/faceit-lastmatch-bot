# FACEIT last match stats BOT

This BOT, written in Python, sends a discord message to certain channel with info about your last CS:GO match on FACEIT.

![Teaser](https://raw.githubusercontent.com/mpn01/faceit-lastmatch-bot/master/README/videos/teaser.gif)


### How to install it?

To use it, you'll need to have your own Discord server or be and admin on one.

Click [this link](https://discord.com/api/oauth2/authorize?client_id=847113509124309013&permissions=18432&scope=bot) to add this BOT to your server.

**If BOT isn't working it's probably server related issue**

### How it works?
To show your last match just simply type `!lastmatch %nicnkame%`. BOT will send:
* Score of the match
* Which level you have
* How many ELO points you have
* How many kills you did
* Your K/D Ratio
* Headshot %

### Current problems

* FACEIT API won't let you see your last match if you left it. BOT will only send error message.
* FACEIT API can't read old matches (1/2 months old).