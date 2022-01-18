import discord
import os
from dotenv import load_dotenv
import classes.DatabaseManager as db

class DiscordHelper:    
    database = db.DatabaseManager()
    def isValidCommand(self, command):
        commands = [
            "!TM-add-user",
            "!TM-set-notifications-channel",
            "!TM-help"
        ]
        if command in commands:
            return True
        return False
        
    async def executeCommand(self, command, message, author, channel):
        if command == "!TM-add-user":
            self.database.addUser(message, author)
            await channel.send("Successfully added user to TM")
        elif command == "!TM-set-notifications-channel":
            self.database.setNotificationsChannel(message, author)
            await channel.send("Successfully set notifications channel to " + message)
        elif command == "!TM-help":
            await channel.send("!TM-add-user [TWITCH_USERNAME]\n!TM-set-notifications-channel [CHANNEL_FOR_NOTIFICATIONS]")

    
    def isAuthorized(self, author):
        if author.guild_permissions.administrator == True:
            return True
        return False
    
    async def broadcastStreamerWentOnline(self, user_login, data):
        load_dotenv('../.env')
        intents=discord.Intents.default()
        client=discord.Client(intents=intents)
        await client.login(os.getenv('DISCORD_TOKEN'))
        guilds = await client.fetch_guilds(limit=150).flatten()
        conn = self.database.getConnection()
        query = "SELECT discord_id, notifications_channel FROM servers WHERE id IN(SELECT server FROM servers_streamers WHERE streamer = (SELECT id FROM streamers WHERE user_login = ?)); "
        params = [user_login]
        cursor = conn.cursor()
        cursor.execute(query, params)
        while(True):
            row = cursor.fetchone()
            if row == None:
                break
            channelID = row[1]
            guildData = await client.fetch_guild(row[0])
            channels = await guildData.fetch_channels()
            for channel in channels:
                if channel.id == channelID:
                    messageString = "@everyone\n"
                    messageString += user_login + " is playing " + data['game_name'] +"\n"
                    messageString += "Stream title: " + data['title'] + "\n"
                    messageString += "Come watch at http://www.twitch.tv/" + user_login 
                    await channel.send(messageString)
                    break
            break
        await client.close()
        conn.close()
            