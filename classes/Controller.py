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
        conn.commit()
        cursor.close()
        while(True):
            row = cursor.fetchone()
            if row == None:
                break
            streamData = twitch.getStream(row[0])
            onlineInDB = row[1]
            if streamData['data'] != [] and onlineInDB == False:
                #print(streamData['data'][0])
                await discord.broadcastStreamerWentOnline(row[0], streamData['data'][0])
                database.setStreamerOnline(row[0], 1)
                conn.close()
            elif streamData['data'] == [] and onlineInDB == True:
                database.setStreamerOnline(row[0], 0)
                conn.close()