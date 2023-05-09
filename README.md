# GPT-discord-bot
Discord bot that has Chat GPT, dall-e and medal integrated

Key Features
-------------

- Has OpenAI's ChatPGT integrated.
- Has OpenAI's dall-e integrated.
- Automatically sends any newly uploaded medal clip of medal users in database.

Installing
----------

**Python 3.8 or higher is required**

To install the all used libraries, you can just run the following command:

```terminal
    # Windows
    pip install -r requirements.txt
```
    



Command List
--------------
Replace all value with a comment next to it. This will include your discord bot token and OpenAPI Api key.
This uses Medal's public API key so u can still use it as rate limits are done per IP address.

```python
    help # sends list of commands
    chat (prompt) # sends prompt to OpenAI to get a response
    draw (prompt) # sends prompt to dall-e
    medal (username) # stores medal username in database. From here all new user uploads will be sent to discord
    nick (nickname) # changes nickname of user who sent message
    colour (colour) # changes colour of user who sent message
    roll # rolls random number between 1 and 6
    git # sends my github
```
yuhyuh
