import telebot  # type: ignore
from telebot import types  # type: ignore
from Droplet_Detector.draw import draw_contours_of_drops  # type: ignore
from Droplet_Detector.do_xslx import get_num  # type: ignore
from Droplet_Detector.calculate import get_sum  # type: ignore

# Создаем экземпляр бота
bot = telebot.TeleBot('6050349643:AAHh6MT-s12_9niKl_GwiYRt79NLXDvUk7A')
global_src = ' '


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Меню 🗃')
    btn2 = types.KeyboardButton('Help❓')

    markup.row(btn1, btn2)
    bot.send_message(message.chat.id,
                     "Привет, {0.first_name}!".format(message.from_user),
                     reply_markup=markup)
    bot.send_message(message.chat.id,
                     "🔸Я бот🤖, который может:\n"
                     "🔸Отрисовать контур капель на фотографии💦\n"
                     "🔸Вычислить площадь каждой капли🧮\n"
                     "🔸Сохранить данные в xlsx файл и отправить его вам📝\n"
                     "Перед тем как начать работу нажмите Help❓ ",
                     reply_markup=markup)


@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    try:

        file_down = bot.get_file(message.document.file_id)
        down_file = bot.download_file(file_down.file_path)

        src = 'save_docs/' + message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(down_file)
        file = open(src, 'rb')
        # path = gray_img(src)
        # file_out = open(path, 'rb')

        global global_src
        global_src = src
        # print(global_src)

        bot.send_photo(message.chat.id, file)
        # os.remove(path)
        bot.reply_to(message, "Пожалуй, я это сохраню")

    except Exception as e:
        print(e)
        bot.reply_to(message, "Не получилось")


@bot.message_handler(content_types=['text'])
def one_click(message):
    if message.text == 'Меню 🗃':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Отрисовать контура капель')
        item2 = types.KeyboardButton('Рассчитать площадь капель')
        item3 = types.KeyboardButton('Сохранить в xlsx')
        item4 = types.KeyboardButton('⬅️ Назад')
        markup.add(item1, item2, item3, item4)
        bot.send_message(message.chat.id, "Меню 🗃", reply_markup=markup)
    elif message.text == '⬅️ Назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Меню 🗃')
        btn2 = types.KeyboardButton('Help❓')
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, "🤔", reply_markup=markup)
    elif message.text == 'Рассчитать площадь капель':
        try:
            file_s = f'exel/new{get_num() - 1}.xlsx'
            file = open(file_s, 'rb')
            print(file)
            bot.send_message(message.chat.id,
                             f"Суммарная площадь капель: {get_sum()}\n"
                             f"Площадь каждой капли будет "
                             f"записана в табличку😉")

        except Exception as e:
            print(e)
            bot.send_message(message.chat.id,
                             "Извините, вы наверно не правильно поняли Help❓\n"
                             "Сперва вам нужно отрисовать контура капель!")
    elif message.text == 'Отрисовать контура капель':
        try:
            filename = draw_contours_of_drops(global_src)
            file = open(filename, 'rb')
            bot.send_photo(message.chat.id, file)
            bot.send_message(message.chat.id, "Отрисовал🎨")

        except Exception as e:
            print(e)
            bot.send_message(message.chat.id,
                             "Извините, но вы не можете продолжить работу.😔\n"
                             "Отправьте мне файл с фото и мы сможем начать!😉")

    elif message.text == 'Сохранить в xlsx':
        try:
            file_s = f'exel/new{get_num() - 1}.xlsx'
            file = open(file_s, 'rb')
            bot.send_document(message.chat.id, file)
            bot.send_message(message.chat.id, "Держи😇")

        except Exception as e:
            print(e)
            bot.send_message(message.chat.id,
                             "Извините, вы наверно не правильно поняли Help❓\n"
                             "Сперва вам нужно рассчитать площадь капель!")

    elif message.text == 'Help❓':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item = types.KeyboardButton('⬅️ Назад')
        markup.add(item)
        bot.send_message(message.chat.id,
                         "📌Для успешной работы бота отправьте"
                         " фотографию капель в виде файла\n"
                         "Далее нажмите <<Меню 🗃>>\n"
                         "📌Если вы хотите отрисовать контуры капель, нажмите"
                         " <<Отрисовать контура капель>> \n"
                         "📌Если вы хотите рассчитать площади капель, нажмите"
                         " <<Рассчитать площадь капель>>\n"
                         "📌Если вы хотите получить данные о "
                         "площадях в виде таблицы, нажмите"
                         " <<Сохранить в xlsx>>", reply_markup=markup)
        bot.send_message(message.chat.id,
                         "⁉Важно⁉\n"
                         "Соблюдайте последовательность:\n"
                         "<<Отрисовать контура капель>> ➡"
                         " <<Рассчитать площадь капель>> ➡ "
                         "<<Сохранить в xlsx>>", reply_markup=markup)
    else:
        bot.send_message(message.chat.id,
                         "Извините,мы не можем с вами "
                         "общаться на отдалённые темы, "
                         "прочтите пожалуйста Help❓ и узнайте"
                         " как со мной работать😉")


# Запускаем бота
bot.polling(none_stop=True, interval=0)
