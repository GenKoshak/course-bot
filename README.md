# course-bot
## outlook
A basic Telegram chatbot that helps users by suggesting a certain English language training course 

The bot is built upon pyTelegramBotAPI and its functionality is based on asking a user certain questions, providing them with possible answers via ReplyKeyboardMarkup.
<img width="837" alt="Снимок экрана 2020-12-12 в 12 06 06" src="https://user-images.githubusercontent.com/24829708/101980080-d9ec9c00-3c73-11eb-8dba-7824a74ecb5c.png">

The repo is uploaded in order to be deployed on Heroku later on.
As of currently 10 scenarious out 90 have been completed.

### code
The current repo contains following files:
course_bot.py
The main executable file which contains the bot token and all the message handlers that govern the conversation.

markups.py
A list of all the keyboard markups used in course_bot.py

bot_phrases.py
A dictionary containing all the button names for the keyboard markups.
