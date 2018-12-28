let Discord = require("discord.js");
let bot = new Discord.Client();
let config = require("./config.json");

bot.on("ready", () => {
  console.log(`Bot started.`); 
  bot.user.setActivity(`Watching`, `noobs!`);
});

bot.on("message", async message => {
  if(message.author.bot) return;
  if(message.content.indexOf(config.prefix) !== 0) return;
  
  let args = message.content.slice(config.prefix.length).trim().split(/ +/g);
  let command = args.shift().toLowerCase();
  
  if(command === "ping") {
    let sentMessage = await message.channel.send("Ping?");
    sentMessage.edit(`The ping is currently ${sentMessage.createdTimestamp - message.createdTimestamp}ms.`);
  }

  if(command === "codeblocks" || command === "codeblock") {
    message.channel.send("Codeblocks are used to send your code in a message with a clean aesthetic, making it easier to read and format. \n```js\n print('Here is an example of a codeblock.')```\n Here is how to use a codeblock:", {code: false})
    message.channel.send("\```lua\n print('Here is an example of a codeblock.')\``` ", {code: true})
  }

  if(command === "api" || command === "apisites" || command === "robloxapi") {
    const codeBlock = new Discord.RichEmbed()
    .setColor(0xFFFFFF)
    .setTitle('Roblox API Site List')
    .setDescription("https://devforum.roblox.com/t/list-of-all-roblox-api-sites/154714/2")
    message.channel.send(codeBlock);
  }

  if(command === "libs" || command === "libraries" || command === "librarylist") {
    const libEmbed = new Discord.RichEmbed()
    .setColor(0xFFFFFF)
    .setTitle('Current Libraries')
    .setDescription("Below is a list of all libraries publicised on this server sorted by language.")
    .addField('Python', 'Pyblox - https://github.com/Sanjay-B/Pyblox \nRobloxlib - https://github.com/NoahCristino/robloxlib')
    .addField('Node.js', 'bloxy - https://github.com/MartinRBX/bloxy \nnoblox.js - https://github.com/suufi/noblox.js \nroblox-js - https://github.com/sentanos/roblox-js')
    .addField('Lua', 'RobloxCommunication - https://github.com/CrescentCode/RobloxCommunication')
    .addField('C#', 'RobloxAPI - https://github.com/gamenew09/RobloxAPI')
    .addField('PHP', 'Roblophp - https://github.com/WebDevTrop/roblophp')
    .addField('Java', 'Javablox - https://github.com/Pythonic-Rainbow/Javablox \nRoblox4j - https://github.com/PizzaCrust/Roblox4j')
    .addField('Kotlin', 'KotlinRoblox - https://github.com/PizzaCrust/KotlinRoblox \nRoblox.kt - https://github.com/FreeLineTM/roblox.kt')
    message.channel.send(libEmbed);
  }

  if(command === "resources") {
    const codeBlock = new Discord.RichEmbed()
    .setColor(0xFFFFFF)
    .setTitle('Useful Resources')
    .setDescription("Below is a list of useful resources for multiple programming languages.")
    .addField('Lua', 'Learning Lua - http://www.lua.org/pil/contents.html \nRoblox Developer Hub - https://www.robloxdev.com/resources \nRoblox API Reference - https://www.robloxdev.com/api-reference')
    .addField('JavaScript', 'Learning Javascript - https://www.codecademy.com/learn/learn-javascript \nJavascript Intro - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Introduction')
    .addField('Python', 'Learning Python - https://www.codecademy.com/learn/learn-python \nPython Intro - https://wiki.python.org/moin/BeginnersGuide')
    .addField('Java', 'Learning Java - https://docs.oracle.com/javase/tutorial/ \nJava Intro - https://www.ibm.com/developerworks/java/tutorials/j-introtojava1/index.html')
    message.channel.send(codeBlock);
  }
  
});
bot.login(config.token);
