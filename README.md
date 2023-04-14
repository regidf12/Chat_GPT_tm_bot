# Welcome to Dive-into-dev  :floppy_disk:

[![Dive-into-dev](https://github.com/Dive-dev/Dive-dev/blob/main/assets/dive-into-dev.png?raw=true)]()

You can follow me on my social networks:

  [![Linktree](https://img.shields.io/badge/-Linktree-131313?style=for-the-badge&logo=Linktree)](https://linktr.ee/dive_into_dev)
  
  [![Telegram](https://img.shields.io/badge/-Telegram-131313?style=for-the-badge&logo=Telegram)](https://t.me/Dark_Hub_info)
  
  [![Vk](https://img.shields.io/badge/-Vk-131313?style=for-the-badge&logo=Vk)](https://vk.com/dive_into_dev)
  
  [![Gmail](https://img.shields.io/badge/-Gmail-131313?style=for-the-badge&logo=Gmail&logoColor=white)](https://mail.google.com/mail/u/0/?fs=1&tf=cm&source=mailto&to=tiltedfear@gmail.com)

# Chat_GPT_tm_bot :robot:

Бот основан на нейросетях ChatGPT и Dell-E.

Рассмотрим код и шаги для запуска бота.

## Основное ⚙️

  Это код требуемый для работы GPT и Dell
      
       openai.api_key = config.API - токин с сайта OpenAI хранится в config.py
       model_engine = "text-davinci-003" - модель на которой работает GPT
       
  Эта часть кода скопированна с документации OpenAI
       
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
  

Hope this code helps you 💾
