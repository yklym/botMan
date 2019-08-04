Bot uses last version of Python Bot Api through pyTelegramBotApi community library

##Project directory:
1. ####Source code files:
    * *bot_classes.py* -- created classes, doesnt i,port other files
    * *bot.py* -- event and querries listenners, main file which includes all others
    * *config.py* -- important settings and variables
    * *logmode.py* -- functions to work with JSON or txt files, create and maintain logfile imports config.py
    * *parse_shop.py* -- functions to make HTTP-request and parse different HTML-documents, includes requests.py and config.py
    * *print_functions.py* - functions which controll responce to user, uses print_functions.py, parse_shop.py and others
2. ####Other files:
    * *prodPictures dir* -- temporary saves images, which are included to .gitignore
    * *log.txt* -- text log of incoming messages, isn't used anywhere
    * *users.json* -- saves users information and personal settings

##How to setup bot and start polling(windows/linux):
1. Install [pip](https://pypi.org/project/pip/)
2. Get Python packages(telebot/requests):
    2.1. [pyTelegramBotApi(telebot) - install and guide](https://github.com/eternnoir/pyTelegramBotAPI#callback-query-handler)
    2.2. [Requests lib guide](https://pythonru.com/biblioteki/kratkoe-rukovodstvo-po-biblioteke-python-requests)
3. Check settings in **config.py** file:
    3.1. *bot token* variable is obligatory
    3.2. *users_file* variable is obligatory and must be initialized at least with emty JSON object({})
    3.3. if *log file* not None, script will try to open or create new file and it can cause errors
4. Start **bot.py** file
