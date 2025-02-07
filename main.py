from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio


api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
kb.add(button)
button_1 = KeyboardButton(text='Информация')
kb.insert(button_1)

@dp.message_handler(text= 'Информация')
async def bot_inform(message):
    await message.answer('Данный бот создан учеником Urban University для практики в создании ТГ-ботов.')


"""
Задача "Цепочка вопросов":
Необходимо сделать цепочку обработки состояний для нахождения нормы калорий для человека.
"""

class UserState(StatesGroup):
    """
    Группа состояний:
    Импортируйте классы State и StatesGroup из aiogram.dispatcher.filters.state.
    Создайте класс UserState наследованный от StatesGroup.
    Внутри этого класса опишите 3 объекта класса State: age, growth, weight
    (возраст, рост, вес).
    Эта группа(класс) будет использоваться в цепочке вызовов message_handler'ов.
    """
    age = State()
    growth = State()
    weight = State()
"""
Задача "Меньше текста, больше кликов":
Необходимо дополнить код предыдущей задачи, чтобы вопросы о параметрах тела для расчёта калорий выдавались
по нажатию кнопки.
Измените massage_handler для функции set_age. Теперь этот хэндлер будет реагировать на текст 'Рассчитать', а
не на 'Calories'.
Создайте клавиатуру ReplyKeyboardMarkup и 2 кнопки KeyboardButton на ней со следующим текстом: 'Рассчитать' и 
'Информация'. Сделайте так, чтобы клавиатура подстраивалась под размеры интерфейса устройства 
при помощи параметра resize_keyboard.
Используйте ранее созданную клавиатуру в ответе функции start, используя параметр reply_markup.

В итоге при команде /start у вас должна присылаться клавиатура с двумя кнопками. 
При нажатии на кнопку с надписью 'Рассчитать' срабатывает функция set_age с которой начинается
работа машины состояний для age, growth и weight.
"""

@dp.message_handler(text= 'Рассчитать')
async def set_age(message):
    print(f'Запущен алгоритм подсчета калорий. \nОжидаем "Возраст"')
    """
    Функция set_age(message):
        Оберните её в message_handler, который реагирует на текстовое сообщение 'Calories'.
        Эта функция должна выводить в Telegram-бот сообщение 'Введите свой возраст:'.
        После ожидать ввода возраста в атрибут UserState.age при помощи метода set.
    """
    await message.answer(f'Введите свой возраст, пожалуйста:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    print(f'Возраст установлен: \n{message.text} \nОжидаем "Рост"')
    """
    Функция set_growth(message, state):
        Оберните её в message_handler, который реагирует на переданное состояние UserState.age.
        Эта функция должна обновлять данные в состоянии age на message.text
        (написанное пользователем сообщение). Используйте метод update_data.
        Далее должна выводить в Telegram-бот сообщение 'Введите свой рост:'.
        После ожидать ввода роста в атрибут UserState.growth при помощи метода set.
    """
    await state.update_data(age= message.text)
    await message.answer(f'Введите свой рост, пожалуйста:')
    await UserState.growth.set()



@dp.message_handler(state= UserState.growth)
async def set_weight(message, state):
    print(f'Установлен рост: \n{message.text} \nОжидаем "Вес"')
    """
    Функция set_weight(message, state):
        Оберните её в message_handler, который реагирует на переданное состояние UserState.growth.
        Эта функция должна обновлять данные в состоянии growth на message.text (написанное пользователем сообщение).
        Используйте метод update_data.
        Далее должна выводить в Telegram-бот сообщение 'Введите свой вес:'.
        После ожидать ввода роста в атрибут UserState.weight при помощи метода set.
    """
    await state.update_data(growth= message.text)
    await message.answer(f'Введите свой вес, пожалуйста:')
    await UserState.weight.set()


@dp.message_handler(state= UserState.weight)
async def send_calories(message, state):
    print(f'Вес установлен:\n{message.text}')
    """
    Функция send_calories(message, state):
        Оберните её в message_handler, который реагирует на переданное состояние UserState.weight.
        Эта функция должна обновлять данные в состоянии weight на message.text (написанное пользователем сообщение).
        Используйте метод update_data.
        Далее в функции запомните в переменную data все ранее введённые состояния при помощи state.get_data().
        Используйте упрощённую формулу Миффлина - Сан Жеора для подсчёта нормы калорий
        (для женщин или мужчин - на ваше усмотрение).
        Данные для формулы берите из ранее объявленной переменной data по ключам age, growth и weight соответственно.
        Результат вычисления по формуле отправьте ответом пользователю в Telegram-бот.
        Финишируйте машину состояний методом finish().
    """
    await state.update_data(weight=message.text)
    data = await state.get_data()
    """
    Формула Миффлина-Сан Жеора – это одна из самых последних формул расчета калорий для оптимального похудения или
    сохранения нормального веса. Она была выведена в 2005 году и все чаще стала заменять
    классическую формулу Харриса-Бенедикта.
    Формула Миффлина-Сан Жеора, разработанная группой американских врачей-диетологов под руководством докторов Миффлина
    и Сан Жеора, существует в двух вариантах – упрощенном и доработанном и выдает необходимое количество килокалорий 
    в сутки для каждого конкретного человека.
    Упрощенный вариант формулы Миффлина-Сан Жеора:
    для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;
    """
    result_calories = (10 * int(data["weight"])) + (6.25 * int(data["growth"])) - (5 * int(data["age"])) + 5
    await message.answer(f'Ваша норма калорий: \n{result_calories}')
    print(f'Вычисления закончены: \n{result_calories}')
    await state.finish()


@dp.message_handler(text = ['Urban'])
async def rinat_message(message):
     print('Urban')
     await message.answer('Служебное сообщение')

@dp.message_handler(commands=['start'])
async def start(message):
      print('Начало работы бота. Всё ок.')
      await message.answer('Привет! Я бот помогающий твоему здоровью. '
                           '\nНажмите на кнопку "Рассчитать", чтобы посчитать '
                           'необходимое количество калорий', reply_markup=kb)

@dp.message_handler()
async def all_message(message):
    print('Введено случайное сообщение')
    await message.answer('Введите команду /start, чтобы начать общение.')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
