import random
import openai
import requests
import json
import sqlite3
openai.api_key=() # OpenAI API key
def handle_responses(message,username_nick,username,nick_change) -> str:
    p_message=message.lower()
    if p_message=="help":
        cmd_list_full=["roll","github","nick","chat","draw","colour","medal"]
        cmd_list_description=["rolls a dice","sends github link","changes nickname","chat with GPT-3","draws a picture using dall-e","changes your colour","adds medal username to database"]
        for i in range(len(cmd_list_full)):
            cmd_list_full[i]=cmd_list_full[i]+" - "+cmd_list_description[i]
        cmd_list_full=str(cmd_list_full)
        cmd_list_full=cmd_list_full.replace(",","; ").replace("'","").replace("[","").replace("]","")
        return "Commands: "+cmd_list_full
    if p_message=="hi":
        return "Hello"
    if p_message=="roll":
        return str(random.randint(1,6))
    if "zabba" in username_nick:
        return "IM THE REAL ZACK"
    if "zabba" in p_message or "zack" in p_message or "zacharius" in p_message:
        response=["ZABBABY YUH","slay the heretic","you called?","if you say zabba one more time...","ZABBA ZABBA ZABBA","ZA","Zabba is a rare word that is likely derived from the Dutch word for 'barrel'"]
        return response[random.randint(0,len(response)-1)]
    if "yas" in p_message:
        return "SLAYYYYY"
    if p_message.startswith("github") or p_message.startswith("git"):
        return "https://github.com/karankantaria"
    if p_message.startswith("chat"):
        p_message=p_message.replace("chat","")
        response = openai.Completion.create(model="text-davinci-003", prompt = p_message, max_tokens=300,temperature = 0)
        return response["choices"][0]["text"]
    if p_message.startswith("draw"):
        p_message=p_message.replace("draw","")
        response = openai.Image.create(prompt = p_message, size="1024x1024")
        return response["data"][0]["url"]
    if p_message.startswith("medal"):
        conn = sqlite3.connect('medal_users.db')
        cursor = conn.cursor()
        modified_string = p_message.replace("medal", "").strip()
        cursor.execute("INSERT INTO medal_users (user_name) VALUES (?)", (modified_string,))
        conn.commit()
        print("New entry added successfully!")
        conn.close()
