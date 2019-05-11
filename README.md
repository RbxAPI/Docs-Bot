# Docs-Bot
Roblox API Server documentation Bot

# Purpose
This repo and it's contents serve to make development regarding the Roblox API
much easier and provides links to various streamlined libraries. This is done
by means of compilation of various resources into a single easy-to-use interface.

## docstoken
The `docstoken.py` contains the token required to login as a Discord Bot User.

To launch your own instance of the bot, create `docstoken.py` in this directory with at least one variable `discord`:
   ```python
   discord = "Token"
   ```
   where `Token` is your own [Bot's token](https://discordapp.com/developers/applications/).

**NOTE:** No one should push `docstoken.py` to upstream. This is treated as local configuration.