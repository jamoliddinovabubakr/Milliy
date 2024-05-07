from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.redis import RedisStorage2
import logging

logging.basicConfig(level=logging.INFO)
API_TOKEN = "6675833746:AAHGIwdOxGQwvuM3EsGZG4Zjz1EMVJphre8"
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
storage = RedisStorage2(host='localhost', port=6379)  # Adjust host and port according to your Redis setup
dp = Dispatcher(bot, storage=storage)

from aiogram.dispatcher.storage import FSMContext

from states import *
from utils import *
from admin_page import *
import backend
from kb import *

ADMINS = [880448541]
STATUS_SERVER = False


@dp.message_handler(commands=['start'], state="*")
async def start_command(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id

    if telegram_id in ADMINS:
        await message.answer("Anonim haqida ma'lumot olish 📋🔍", reply_markup=admin_kb)

    else:
        if STATUS_SERVER:
            await state.finish()
            print(message.from_user.id)

            faculties = backend.get_faculties()

            await state.update_data(faculty_list_check=faculties)

            faculties_buttons = get_keyboard(faculties)

            await message.answer(
                "🎓 O'zMU So'rov Tizimiga hush kelibsiz.\nBu tizim orqali o'qituvchilar haqida fikr va baholaringizni anonim ravishda ifodalash imkoniyati mavjud. 📚🔒")
            await message.answer("Fakultetni tanlang ✨", reply_markup=faculties_buttons)

            await StudentAnswer.faculty.set()

        else:
            await message.answer("Bot faollashtirilmagan!")
            await state.finish()


@dp.message_handler(state=StudentAnswer.faculty)
async def faculty_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    faculty = message.text

    if faculty in data['faculty_list_check']:
        await state.update_data(faculty=faculty)

        departments = backend.get_kafedra(faculty)

        await state.update_data(department_list_check=departments)

        departments_buttons = get_keyboard(departments)

        await message.answer("Kafedrani tanlang ✨", reply_markup=departments_buttons)
        await StudentAnswer.department.set()

    else:
        await message.answer("To'g'ri fakultetni tanlang ❌")
        await StudentAnswer.faculty.set()


@dp.message_handler(state=StudentAnswer.department)
async def faculty_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    department = message.text
    if department in data['kafeda_list_check']:

        await state.update_data(kafedra=department)
        teachers = backend.get_teachers(department)
        await state.update_data(teacher_list_check=teachers)

        teachers_buttons = get_keyboard(teachers)

        await message.answer("O'qituvchini tanlang 👩‍🏫👨‍🏫", reply_markup=teachers_buttons)

        await StudentAnswer.teacher.set()
    else:
        await message.answer("To'g'ri kafedrani tanlang ❌")
        await StudentAnswer.department.set()


@dp.message_handler(state=StudentAnswer.teacher)
async def teacher_handler(message: types.Message, state: FSMContext):
    teacher = message.text
    data = await state.get_data()
    if teacher in data['teacher_list_check']:

        await state.update_data(teacher=teacher)
        questions = backend.get_questions()
        await state.update_data(questions=questions)

        question_answer = {}
        for i in questions:
            question_answer[i['name']] = ''
        await state.update_data(question_answer=question_answer)

        t_name = questions[0]['name']
        await state.update_data(iter=t_name)

        answers = backend.get_answers(t_name)

        await state.update_data(answers_list_check=answers)

        answers_buttons = get_keyboard(answers)
        await message.answer(f"{t_name} ?", reply_markup=answers_buttons)

        await StudentAnswer.questions.set()
    else:
        await message.answer("To'g'ri o'qituvchini tanlang ❌")
        await StudentAnswer.teacher.set()


@dp.message_handler(state=StudentAnswer.questions)
async def question_handler(message: types.Message, state: FSMContext):
    answer = message.text
    data = await state.get_data()
    if answer in data['answers_list_check']:

        questions = data['questions']
        t_item = data['iter']
        new_questions = delete_dict_by_value(questions, t_item)
        question_answer = data['question_answer']
        question_answer[t_item] = answer

        await state.update_data(question_answer=question_answer)
        await state.update_data(questions=new_questions)

        try:
            t_item = new_questions[0]['name']
            answers = backend.get_answers(t_item)

            await state.update_data(iter=t_item)
            await state.update_data(answers_list_check=answers)
            answers = backend.get_answers(t_item)
            if answers:

                answers_buttons = get_keyboard(answers)

                await message.answer(f"{t_item} ?", reply_markup=answers_buttons)
            else:
                await message.answer(f"{t_item} ?", reply_markup=types.ReplyKeyboardRemove())
            await StudentAnswer.questions.set()
        except IndexError:
            await message.answer("0 dan 100 gacha baholang ✨", reply_markup=types.ReplyKeyboardRemove())

            await StudentAnswer.general_score.set()

    else:
        await message.answer("To'g'ri javobni kiriting ❌")
        await StudentAnswer.questions.set()


@dp.message_handler(state=StudentAnswer.general_score)
async def answer_handler(message: types.Message, state: FSMContext):
    try:
        general_score = int(message.text)
        if 100 >= general_score >= 0:
            await state.update_data(general_score=general_score)
            keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard_markup.add(types.KeyboardButton('Tasdiqlash ✅'))
            await message.answer(f"Izohlar yozing 💬", reply_markup=keyboard_markup)

            await StudentAnswer.comment.set()

        else:
            await message.answer("0 dan 100 gacha baholang ✨", reply_markup=types.ReplyKeyboardRemove())
            await StudentAnswer.general_score.set()
    except ValueError:
        await message.answer("Raqam yozing ✨")
        await StudentAnswer.general_score.set()


@dp.message_handler(state=StudentAnswer.comment)
async def answer_handler(message: types.Message, state: FSMContext):
    if message.text == 'Tasdiqlash ✅':
        await state.update_data(comment=None)

    else:
        comment = message.text
        await state.update_data(comment=comment)
        await message.answer('✨ Fikringiz uchun rahmat! 😊')

    data = await state.get_data()

    desired_data = {
        "kafedra": data['kafedra'],
        "teacher": data['teacher'],
        "question_answer": data['question_answer'],
        "general_score": data['general_score'],
        "comment": data['comment']
    }
    status = backend.result(desired_data)
    await state.finish()

    faculties = backend.get_faculties()

    await state.update_data(faculty_list_check=faculties)

    faculties_buttons = get_keyboard(faculties)

    await message.answer(
        "🎓 O'zMU So'rov Tizimiga hush kelibsiz.\nBu tizim orqali o'qituvchilar haqida fikr va baholaringizni anonim ravishda ifodalash imkoniyati mavjud. 📚🔒")
    await message.answer("Kafedrani tanlang ✨", reply_markup=faculties_buttons)

    await StudentAnswer.faculty.set()


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin,
                                      "🤖 Bot qayta ishga tushdi! 🎉\n🔗 <a href='http://127.0.0.1:8000/OzMUtizimi/'>Bot Admin Saxifasi</a> 🛠️",
                                      parse_mode="HTML", reply_markup=keyboard_back)
        except Exception as err:
            logging.exception(err)


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Restart"),
        ]
    )


async def on_startup(dispatcher):
    logging.info('Bot working')
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
