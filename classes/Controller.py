import classes.DatabaseManager as db
import time
import classes.TwitchHelper as th
import classes.DiscordHelper as dh

class Controller:
    async def run(self):
        database = db.DatabaseManager()
        twitch = th.TwitchHelper()
        discord = dh.DiscordHelper()
        conn = database.getConnection()
        cursor = conn.cursor()
        query = "SELECT user_login, online FROM streamers;"
        params = []
        cursor.execute(query, params)
        while(True):
            row = cursor.fetchone()
            if row == None:
                break
            currentlyOnline = twitch.userOnline(row[0])
            onlineInDB = row[1]
            if currentlyOnline == True and onlineInDB == False:
                await discord.broadcastStreamerWentOnline(row[0])
                database.setStreamerOnline(row[0], 1)
            elif currentlyOnline == False and onlineInDB == True:
                database.setStreamerOnline(row[0], 0)