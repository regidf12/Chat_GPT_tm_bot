# Welcome to Regidf

# Chat_GPT_tm_bot :robot:

The bot is based on ChatGPT and Dell-E neural networks.

Consider the code and steps to run the bot.

## Основное ⚙️

  This is the code required for GPT and Dell to work
      
       openai.api_key = config.API - токин с сайта OpenAI хранится в config.py
       model_engine = "text-davinci-003" - модель на которой работает GPT
       
 This part of the code is copied from the OpenAI documentation
       
       async def chat_gpt(message: types.Message):
       prompt = str(message.text)
       completion = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=2048,
            temperature=0.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        await bot.send_message(message.chat.id, completion.choices[0].text)
       
And this piece is responsible for the work of Dell E

    await bot.send_message(message.chat.id, "Ожидайте изображение...")
            prompt = str(message.text)
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="512x512",
            )
            await bot.send_message(message.chat.id, response["data"][0]["url"])
            
  But I want to emphasize that in the web version of telegram, the image comes as a link and nothing else.
  
   The rest of the code is just the character counting algorithms I came up with, the functions for determining whether the user is subscribed to a group in Tg and the database storing all the data about the user, I can’t say that all these algorithms have been brought to mind, but they are not bad, although they require improvements.
  
## Bot launch ℹ️

  1. Get a token from BotFather
  2. Get a token in OpenAI
  3. Paste in config.py file
  4. Go to IDE/cmd/notepad++
  5. And run the program in the standard way for your environment
 
  You should not have any more problems, but if you have, create a discussion or ask a question on stackoverflow
 
 
  The bot on the telegram link is not working yet.
  

Hope this code helps you
