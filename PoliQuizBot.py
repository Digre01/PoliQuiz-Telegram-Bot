import os
import telebot
import requests
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types
from random import randint

API_KEY = "5623910350:AAGjVfSC9EoDdW0rIgxKd6lQK7CqLh7Mn_M"
bot = telebot.TeleBot(API_KEY)
URL = 'https://api.poliquiz.it'

request = requests.get(URL + '/courses')
f = request.json()

print(f)
print("Bot is starting...")

courses = []
for course in f['data']:
  print(course['name'])
  courses.append(course['name'])


def check_course(msg):
  return msg in courses


# variabile globale che decide il numero di quiz
numberOfQuiz = 0
TOT_quiz = 0
quizzes = []


# ---------------------------- Comandi ----------------------------


# messaggio di inizio
@bot.message_handler(commands=['start'])
def start(message):
  bot.send_message(
    message.chat.id,
    "Hi!\nThis is bot is a telegram version of PoliQuiz made by Digre\n\nI quiz sono soggetti a licenza Creative Commons: CC-BY-NC 4.0 Poliquiz.it."
  )

  # selezione corso
  markup = types.ReplyKeyboardMarkup(row_width=2)
  itembtn1 = types.KeyboardButton(courses[0])
  itembtn2 = types.KeyboardButton(courses[1])
  itembtn3 = types.KeyboardButton(courses[2])
  itembtn4 = types.KeyboardButton(courses[3])
  itembtn5 = types.KeyboardButton(courses[4])
  itembtn6 = types.KeyboardButton(courses[5])
  itembtn7 = types.KeyboardButton(courses[6])
  itembtn8 = types.KeyboardButton(courses[7])
  itembtn9 = types.KeyboardButton(courses[8])
  itembtn10 = types.KeyboardButton(courses[9])
  markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6,
             itembtn7, itembtn8, itembtn9, itembtn10)
  
  bot.send_message(message.chat.id, "Choose one course:", reply_markup=markup)






      


# scelta numero di quiz
@bot.message_handler(func=lambda msg: check_course(msg.text))
def setQuiz(message):
  

    #troviamo l'id associato al nome del corso
    for course in f['data']: 
        if message.text == course["name"]:
           id = course['id']

    URL = 'https://api.poliquiz.it'
    URL += '/course/' + str(id) #prende il JSON del corso specifico
    request = requests.get(URL)
    r = request.json()
    TOT_quiz = r['data']['total_quizzes'] #estrae il numero totale di quiz
    
    URL += '/quizzes' #rifa la lettura del JSON
    request = requests.get(URL)
    r = request.json()
    quizzes = r['data'] #estrea i quiz in una lista


    options = ['5', '15', '30']

    inline_markup = types.InlineKeyboardMarkup()
    itembtn11 = types.InlineKeyboardButton(text=options[0],
                                            callback_data="option0")
    itembtn12 = types.InlineKeyboardButton(text=options[1],
                                            callback_data="option1")
    itembtn13 = types.InlineKeyboardButton(text=options[2],
                                            callback_data="option2")
    inline_markup.add(itembtn11, itembtn12, itembtn13)
    bot.send_message(message.chat.id,
                    "How many quiz do you want to do?",
                    reply_markup=inline_markup)


# setta il numero di quiz
@bot.callback_query_handler(func=lambda call: True)
def qui(call):

  if call.data == "option0":
    numberOfQuiz = 5
  if call.data == "option1":
    numberOfQuiz = 15
  if call.data == "option2":
    numberOfQuiz = 30

  bot.answer_callback_query(call.id, f"Selected: {numberOfQuiz} quiz")
  bot.send_message(call.id, "adasd")
  


# algoritmo quiz
max_n = len(quizzes)
points = 0

for i in range(numberOfQuiz):  
  
  id_question = randint(0, TOT_quiz)
  quiz = quizzes[id_question]

  if quiz['verified']:
    print(quiz['question'])
    answers = quiz['answers']

    for j in range(len(answers)):
      print(str(j + 1) + ")   " + str(answers[j]))

    risposta = int(input("numero risposta: "))

    if risposta - 1 == quiz['right_answer_index']:
      points += 3

    else:
      points -= 1

    print("\n")

  else:
    i -= 1

















bot.infinity_polling()
