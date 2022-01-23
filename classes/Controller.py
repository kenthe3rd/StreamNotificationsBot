import classes.DatabaseManager as db
import time
import classes.TwitchHelper as th
import classes.DiscordHelper as dh

class Controller:
    async def run(self):
        database = db.DatabaseManager()
        twitch = th.TwitchHelper()
        discord = dh.DiscordHelper()
        while(True):
            conn = database.getConnection()
            cursor = conn.cursor()
            query = "SELECT user_login, online FROM streamers;"
            params = []
            cursor.execute(query, params)
            row = cursor.fetchone()
            if row == None:
                cursor.close()
                conn.close()
                break
            streamData = twitch.getStream(row[0])
            onlineInDB = row[1]
            if streamData['data'] != [] and onlineInDB == False:
                #print(streamData['data'][0])
                await discord.broadcastStreamerWentOnline(row[0], streamData['data'][0])
                database.setStreamerOnline(row[0], 1)
            elif streamData['data'] == [] and onlineInDB == True:
                database.setStreamerOnline(row[0], 0)
