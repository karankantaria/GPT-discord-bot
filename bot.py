import discord
import responses
import nextcord
from discord.ext import tasks, commands
import requests
import json
from medal_api import MedalAPI
import sqlite3

intents = discord.Intents.default()
intents.typing = True
intents.messages = True
intents.message_content = True
intents.members = True

async def send_message(message,user_message,is_private):
    try:
        response=responses.handle_responses(user_message,str(message.author.nick),str(message.author),message.author.nick)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN='' # Replace with your bot token
    client=discord.Client(intents=intents)
    @client.event
    async def on_ready():
        my_task.start()
        print(f'{client.user} has connected to Discord!')

    @client.event
    async def on_message(message):
        if message.author==client.user:
            return
        username=str(message.author)
        user_message=str(message.content)
        channel=str(message.channel)
        print(f'{username} sent {user_message} in {channel}')
        if user_message[0]=='!':
            user_message=user_message[1:]
            await send_message(message,user_message,is_private=True)
        else:
            if user_message.startswith("nick"):
                member = message.guild.get_member(message.author.id)
                if member is not None:
                    try:
                        await member.edit(nick=user_message[4:])
                    except discord.Forbidden:
                        print("I don't have permission to change the nickname.")
                else:
                    print("Member not found in the guild.")
            if message.content.lower().startswith('colour'):
                color_list=["Red","Blue","Silver","Spring_green","Aqua","Chocolate","Yellow","Magenta","Hot_pink","Crimson"]
                if "list" in message.content.lower():
                    await message.channel.send(f"Available colors: {color_list}")
                    return
                role_name = message.content[6:].strip()
                new_role = nextcord.utils.get(message.guild.roles, name=role_name)
                if new_role is not None:
                    for role in message.author.roles:
                        for i in range(len(color_list)):
                            if role.name == color_list[i]:
                                await message.author.remove_roles(role)
                    await message.author.add_roles(new_role)
                else:
                    await message.channel.send(f"Sorry, the role `{role_name}` does not exist.")
            if message.author.name == "swift" and message.author.discriminator == "0666" and message.content == "PURGE":
                # Get the channel object
                channel = client.get_channel() # Replace with your desired channel ID
                await channel.purge()
                await message.channel.send("All messages have been deleted!")
            else:
                await send_message(message,user_message,is_private=False)
        user_message=user_message.replace("nick","").strip()

    @client.event
    async def on_member_update(before, after):
        if before.nick != after.nick and "zabba" in after.nick.lower():
            new_nick = "ZABABY YUH"
            try:
                await after.edit(nick=new_nick)
                print(f"Changed {after.display_name}'s nickname to {new_nick}")
            except discord.Forbidden:
                print(f"Could not change {after.display_name}'s nickname due to insufficient permissions.")

    @tasks.loop(seconds=300)
    async def my_task():
        channel = client.get_channel() # Replace with your desired channel ID
        api=MedalAPI()
        conn = sqlite3.connect('medal_users.db')
        c = conn.cursor()
        c.execute('SELECT user_name FROM medal_users')
        users = []
        for row in c.fetchall():
            users.append(row[0])
        print(users)
        conn.close()
        user_ID_list=[]
        for user in users:
            users_ID=api.get_user(user)
            user_ID_list.append(users_ID[0]['userId'])
        for i in range(len(user_ID_list)):
            url = "https://developers.medal.tv/v1/latest"
            headers = {
                "Authorization": "pub_lC6L2dum838FGlsYmPr2mIqeOuqORwbj" # You can use this API key, rate limits are done off IP basis
            }

            params = {
                "userId": user_ID_list[i],
                "limit": "1"
            }
            print(params,headers)
            response = requests.get(url, headers=headers, params=params)
            response=response.json()
            id_count=0
            # Made by Karan Kantaria 
            conn = sqlite3.connect('medal_users.db')
            c = conn.cursor()
            c.execute('SELECT content_id FROM medal_users')
            content_ids = []
            for row in c.fetchall():
                content_ids.append(row[0])
            for content_iteration in range(len(content_ids)):
                if response['contentObjects'][0]['contentId'] == content_ids[content_iteration]:
                    id_count+=1
            if id_count==0:
                print(users[i])
                c.execute("UPDATE medal_users SET content_id = ? WHERE user_name = ?", (response['contentObjects'][0]['contentId'], users[i]))
                await channel.send(response['contentObjects'][0]['directClipUrl'])
                conn.commit()
                conn.close()
            


    client.run(TOKEN)
