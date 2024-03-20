import telebot
import requests
import json
from config import TOKEN, API
bot = telebot.TeleBot(token=TOKEN) #создаем экземпляр бота


@bot.message_handler(commands=['start'])
def start(message):
    music = open('music.mp3', 'rb')
    bot.send_voice(message.chat.id, music)
    bot.send_message(message.chat.id, 'Напиши город!')


@bot.message_handler(content_types=['text'])
def get_wether(message):
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={message.text.strip()}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        cur_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]  # влажность
        pressure = data["main"]["pressure"]
        wind_speed = data["wind"]["speed"]
        info = (f"Погода в городе {message.text.title()}\nТемпература: {cur_weather} °C\nВлажность: {humidity}%\n"
                f"Давление: {pressure} мм.рт.ст\nВетер: {wind_speed} м/с")
        bot.reply_to(message, info)
    else:
        bot.reply_to(message, 'Город указан неверно')


if __name__ == "__main__":
    bot.polling(none_stop=True)
