# Docs-Bot
Roblox API Server documentation Bot

Download: ``git clone https://github.com/RbxAPI/Docs-Bot.git``

# Purpose
This repo and it's contents serve to make development regarding the Roblox API
much easier and provides links to various streamlined libraries. This is done
by means of compilation of various resources into a single easy-to-use interface.

## Configuration
The `docstoken.py` has be deprecated in favor of enviromental variables. 

To launch your own instance of the bot, create `.env` in this directory (main directory) with the following:
   ```env
   # The token the bot will use to authenticate with Discord
   DISCORD_TOKEN=<DISCORD_TOKEN>
   
   # Various channels
   BOT_COMMANDS_CHANNEL=<CHANNEL_FOR_BOT_COMMANDS>
   MESSAGE_LOGS_CHANNEL=<CHANNEL_FOR_MESSAGE_LOGS>
   MODERATION_LOGS_CHANNEL=<CHANNEL_FOR_MOD_LOGS>
   JOIN_LOGS_CHANNEL=<CHANNEL_FOR_JOIN_LOGS>
   
   # Various categories
   LIBRARIES_CATEGORY=<LIBRARY_DEVELOPER_CATEGORY>
   FRAMEWORKS_CATEGORY=<FRAMEWORKS_DEVELOPER_CATEGORY>
   ```
   where `DISCORD_TOKEN` is your own [Bot's token](https://discordapp.com/developers/applications/).

**NOTE:** No one should push `docstoken.py` to upstream. This is treated as local configuration.
