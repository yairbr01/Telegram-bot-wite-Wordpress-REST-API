# Telegram-bot-wite-Wordpress-REST-API
Using this repository you can create a telegram bot that interfaces with the wordpress rest API and lets you publish posts consisting of text / image / video.

## This repository consists of 2 parts:
1. Python file that activates the telegram bot.
2. PHP function that handles REST API c on the site.

## In order to use this bot, the following must be defined:
1. Token definition of the bot in its executable file.
2. Setting up an authentication token in the REST API and inserting it into the bot code.
3. Setting the ID of the users allowed to use the bot in the bot's executable file (you can use this bot to get the ID: https://t.me/getmyid_bot).
4. Setting up the Webhooks URLs.
5. Setting up a new user application on the site and setting up its login information in the bot code.
6. In order to upload a video or image, you must define a custom field on the website and change its slug in the rest api.
