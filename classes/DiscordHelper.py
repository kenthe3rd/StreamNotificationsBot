import discord
import os
from dotenv import load_dotenv
import classes.DatabaseManager as db

class DiscordHelper:    
    database = db.DatabaseManager()
    def isValidCommand(self, command):
        commands = [
            "!SNB-add-user",
            "!SNB-set-notifications-channel"
        ]
        if command in commands:
            return True
        return False
        
    async def executeCommand(self, command, message, author, channel):
        if command == "!SNB-add-user":
            self.database.addUser(message, author)
            await channel.send("Successfully added user to SNB")
        elif command == "!SNB-set-notifications-channel":
            self.database.setNotificationsChannel(message, author)
            await channel.send("Successfully set notifications channel to " + message)

    
    def isAuthorized(self, author):
        if author.guild_permissions.administrator == True:
            return True
        return False
    
    async def broadcastStreamerWentOnline(self, user_login):
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
                    await channel.send("@everyone " + user_login + " went online!\nhttp://www.twitch.tv/" + user_login)
                    break
            break
        await client.close()
        conn.close()
            