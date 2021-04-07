from bs4 import BeautifulSoup
import requests
import telebot

API = '1687153363:AAEkBG9scz7z9TOien-4RIV3Cw7Kh58Ct2Q'
bot = telebot.TeleBot(API)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Welcome! The bot returns GitHub repositories by username")
    bot.send_message(message.chat.id, "Enter github username: ")

@bot.message_handler(content_types=['text'])
def get_username(message):
    user_name = message.text
    repos = get_repos(user_name)
    print(repos)
    for i in repos:
        bot.send_message(message.chat.id, i)

def get_repos(user_name):
    url =f'https://github.com/{user_name}?tab=repositories'
    r = requests.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        l = []
        for i in soup.find_all("h3", {"class": "wb-break-all"}):
            l.append(i.a.string[9:])
        l2 = []
        for i in l:
            i = f'github.com/{user_name}/{i}'
            l2.append(i)
        return l2
    else:
        print("Incorrect username")


bot.polling()