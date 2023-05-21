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
       
  А этот кусок отвечает за работу Dell E

    await bot.send_message(message.chat.id, "Ожидайте изображение...")
            prompt = str(message.text)
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="512x512",
            )
            await bot.send_message(message.chat.id, response["data"][0]["url"])
            
  Но хочу подчеркнуть, то что в web версии telegram изображение приходит ссылкой и никак иначе.
  
  Весь остальной код это просто придуманные мной алгоритмы счета символов, функции определения подписан ли пользователь на группу в Tg и БД хронящая в себе все данные о пользователе, не мого сказать, что все эти алгоритмы доведены до ума, но они не плохо, хотя и требуют доработки.
  
## Запуск бота ℹ️

  1. Получить токин у BotFather
  2. Получить токен в OpenAI
  3. Вставить в файл config.py
  4. Зайти в IDE/cmd/notepad++
  5. И запустить программу стандартным способом для вашей среды
 
 Больше проблем возникнуть у вас не должно, а если возникли создайте дисскусию или задайте вопрос на stackoverflow
 
 
 Бот по ссылке в телеграм пока не работает.
  

Hope this code helps you
