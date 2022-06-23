import telebot
from telebot import types
import configure
import time
import random
from question_base import question_dict, answer_dict, num, asked_questions, game_score, final_game_score

bot = telebot.TeleBot(configure.config['token'])

num_list = [i for i in range(1, len(question_dict) + 1)]


@bot.message_handler(commands=['start', 'new_game'])
def start_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Летс гоу')
    markup.add(item1)
    asked_questions = []
    bot.send_message(message.chat.id,
                     "Привет! Давай поиграем.", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ['Летс гоу', 'Следующий вопрос'])
def message_ques(message):
    global num
    global asked_questions
    markup_ques = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Показать ответ')
    markup_ques.add(item1)
    if game_score[1] < 7:
        num = random.choice(list(set(num_list) - set(asked_questions)))
        asked_questions.append(num)
        bot.send_message(message.chat.id, 'Вопрос:\n\n' + question_dict[num].upper())
        bot.send_message(message.chat.id, 'Минута пошла! ')
        time.sleep(30)
        bot.send_message(message.chat.id, 'Осталось 30 сек.')
        time.sleep(20)
        bot.send_message(message.chat.id, 'Осталось 10 сек.')
        time.sleep(10)
        bot.send_message(message.chat.id, 'Время вышло!', reply_markup=markup_ques)
    elif len(asked_questions) == len(num_list):
        markup_finish = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item2 = types.KeyboardButton('Летс гоу')
        markup_finish.add(item2)
        bot.send_message(message.chat.id, 'Вопросы закончились. Спасибо за игру!', reply_markup=markup_finish)


@bot.message_handler(func=lambda message: message.text in ['Показать ответ'])
def message_ans(message):
    markup_ans = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item3 = types.KeyboardButton('Ответили правильно')
    item4 = types.KeyboardButton('Ответили НЕправильно')
    markup_ans.add(item3, item4)
    bot.send_message(message.chat.id, 'Правильный ответ:\n\n' + answer_dict[num].upper(), reply_markup=markup_ans)


@bot.message_handler(func=lambda message: message.text in ['Ответили правильно', 'Ответили НЕправильно'])
def message_scores(message):
    global game_score
    markup_score_base = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item5 = types.KeyboardButton('Следующий вопрос')
    markup_score_base.add(item5)
    markup_score_final = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item6 = types.KeyboardButton('К Суперигре')
    markup_score_final.add(item6)
    if message.text == 'Ответили правильно':
        game_score[0] += 1
        game_score[1] += 1
    elif message.text == 'Ответили НЕправильно':
        game_score[1] += 1
    if game_score[1] < 7:
        bot.send_message(message.chat.id, 'Общий счет:\n\n' + str(game_score[0]) + ' из ' + str(game_score[1]),
                    reply_markup=markup_score_base)
    elif game_score[1] == 7:
        bot.send_message(message.chat.id, 'Итоговый счет:\n\n' + str(game_score[0]) + ' из ' + str(game_score[1]) +
                         '\n\n' + 'На суперигру у Вас будет ' +
                         str(game_score[0]) + ' минут(ы).' + '\n\n' +
                         'В суперигре Ваш вариант ответа нужно отправить боту текстом. ' +
                         '\n\n' +
                         'Чтобы выиграть в суперигре, ответьте правильно на 4 вопроса.',
                         reply_markup=markup_score_final)


@bot.message_handler(func=lambda message: message.text in ['К Суперигре', 'Следующий'])
def message_ques_final(message):
    global num
    global asked_questions
    global final_game_score
    markup_final_que = types.ForceReply(selective=False)
    num = random.choice(list(set(num_list) - set(asked_questions)))
    asked_questions.append(num)
    bot.send_message(message.chat.id, str(final_game_score) + '`й вопрос суперигры:')
    bot.send_message(message.chat.id, question_dict[num].upper(),
                     reply_markup=markup_final_que)
    final_game_score += 1


@bot.message_handler(func=lambda message: message.text not in ['Летс гоу',
                                                               'Следующий вопрос',
                                                               'Показать ответ',
                                                               'Ответили правильно',
                                                               'Ответили НЕправильно',
                                                               'К Суперигре',
                                                               'Следующий'
                                                               ]
                     )
def message_scores(message):
    global final_game_score
    markup_final_ans = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item7 = types.KeyboardButton('Следующий')
    markup_final_ans.add(item7)
    markup_final = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item8 = types.KeyboardButton('/new_game')
    markup_final.add(item8)
    if message.text.lower() == answer_dict[num].lower() and final_game_score < 5:
        bot.send_message(message.chat.id, 'Верно!', reply_markup=markup_final_ans)
    elif message.text.lower() == answer_dict[num].lower() and final_game_score == 5:
        bot.send_message(message.chat.id, 'Поздравляю! Вы выиграли супер игру!', reply_markup=markup_final)
    else:
        bot.send_message(message.chat.id, 'Неверно!')



bot.infinity_polling()

