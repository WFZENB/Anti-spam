import pymorphy2
import re
import math
import serializer


# Словарь уникальных слов
unique_words = {}

# Количество слов в классах
spam_words_count  = 0
other_words_count = 0

# Количество слов в классах
spam_texts_count  = 0
other_texts_count = 0

# Начальные тексты для обучения
spam_text  = ['''САЙТУ ИСПОЛНЯЕТСЯ 10 ЛЕТ ОТПРАВЬ ЭТО СООБЩЕНИЕ 10 ДРУЗЬЯМ И У ТЕБЯ ПОЯВИТСЯ ЗОЛОТАЯ РАМОЧКА И
                РАЗНОЦВЕТНЫЕ СМАЙЛИКИ И ТАКЖЕ ТЫ БУДЕШЬ ЗНАТЬ КТО ЗАХОДИТ К ТЕБЕ НА СТРАНИЦУ''']
other_text = ['''Письма в русском языке обычно включают в себя стандартные фразы и формулировки. Часть вашего курса
                русского языка будет посвящена написанию писем всех жанров. Здесь мы приведём несколько примеров
                стандартных письменных формулировок и два примера писем.''']


# Нормализатор текста
def normal_sep_text(text):
    # Отделение слов
    text = re.findall(r'\w+-\w+|[а-яА-ЯёЁ]\w+', text)

    # Экземпляр класса морфологического анализатора
    morph = pymorphy2.MorphAnalyzer()

    # Постановка в инфинитив
    normal_text = []
    for word in text:
        normal_text.append(morph.parse(word)[0].normal_form)

    return normal_text


# Добавление сообщения в массив исходных данных
def add_study(text, is_spam):
    global spam_words_count
    global other_words_count
    global spam_texts_count
    global other_texts_count
    global unique_words

    normal_text = normal_sep_text(text)

    if is_spam:
        spam_texts_count += 1
        for word in normal_text:
            spam_words_count += 1
            if unique_words.get(word) is None:
                unique_words[word] = [1, 0]
            elif unique_words.get(word)[0] == 0:
                unique_words[word][0] = 1
            else:
                unique_words[word][0] += 1
    else:
        other_texts_count += 1
        for word in normal_text:
            other_words_count += 1
            if unique_words.get(word) is None:
                unique_words[word] = [0, 1]
            elif unique_words.get(word)[1]  == 0:
                unique_words[word][1] = 1
            else:
                unique_words[word][1] += 1

    serializer.write()


# Исходное обучение
def init_study():
    for text in spam_text:
        add_study(text, True)
    for text in other_text:
        add_study(text, False)


# Коэффициент спама
def spam_probability(normal_text):
    result = math.log(spam_texts_count/(spam_texts_count+other_texts_count))
    for word in normal_text:
        result += math.log((unique_words.get(word, [0, 0])[0] + 1)/(len(unique_words)+spam_words_count))
    return result


# Коэффициент не спама
def other_probability(normal_text):
    result = math.log(other_texts_count/(other_texts_count+spam_texts_count))
    for word in normal_text:
        result += math.log((unique_words.get(word, [0, 0])[1] + 1)/(len(unique_words)+other_words_count))
    return result


# Вероятность принадлежности сообщения к спаму
def nba_spam_predict(text):
    normal_text = normal_sep_text(text)
    spam = spam_probability(normal_text)
    other = other_probability(normal_text)
    return 1/(1+(math.exp(other-spam)))


def init():
    #init_study()
    serializer.read()
