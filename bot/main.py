from aiogram import types
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
import logging
import asyncio

import backend

from aiogram.dispatcher.filters.state import StatesGroup, State



STATUS_SERVER = False

# =========== STATE ============= #
class StudentAnswer(StatesGroup):
    faculty_list_check = State()
    teacher_list_check = State()
    answers_list_check = State()
    kafeda_list_check = State()

    faculty = State()
    teacher = State()
    kafedra = State()
    general_score = State()
    comment = State()


    iter = State()
    questions = State()
    question_answer = State()

    finish = State()


class AdminState(StatesGroup):
    faculty = State()
    kafedra = State()
# ============================== #


from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.redis import RedisStorage2









# ============ SETTINGS ============ #
logging.basicConfig(level=logging.INFO)
API_TOKEN = "6675833746:AAHGIwdOxGQwvuM3EsGZG4Zjz1EMVJphre8"
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
storage = RedisStorage2(host='localhost', port=6379)  # Adjust host and port according to your Redis setup
dp = Dispatcher(bot, storage=storage)
# ============================== #




# ============ ADMIN SETTINGS ============ #
ADMINS = [880448541]
# ============================== #



# ======== KEYBOARDS =========== #
admin_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
admin_kb.add(types.KeyboardButton("So'rovlar soni 📈"))
admin_kb.add(types.KeyboardButton('Excel fayllar 📊'))
admin_kb.add(types.KeyboardButton("Ma'lumotlarni tozalash 🗑"))
admin_kb.add(types.KeyboardButton("Botning xolati"))

kb_back = [
    [types.KeyboardButton('Orqaga ⬅️')]
]
keyboard_back = types.ReplyKeyboardMarkup(
    keyboard=kb_back, resize_keyboard=True)
# ============================== #



# ======== UTILS =========== #
def delete_files_in_folder(folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            pass
    

def get_keyboard(objects):
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for obj in objects:
        try:
            keyboard_markup.add(types.KeyboardButton(obj['name']))
        except:
            keyboard_markup.add(types.KeyboardButton(obj))

    return keyboard_markup


def delete_dict_by_value(list_of_dicts, value_to_delete):
    """
    Delete dictionaries from the list based on a specific value of a key.

    Parameters:
        list_of_dicts (list): List of dictionaries.
        value_to_delete (str): The value to delete.

    Returns:
        list: Updated list of dictionaries.
    """
    # Create a new list to store dictionaries without the specified value
    updated_list = []

    # Iterate through the list and add dictionaries to the updated list if they don't have the specified value
    for item in list_of_dicts:
        if item.get('name') != value_to_delete:
            updated_list.append(item)

    return updated_list
# ============================== #

        
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

            await message.answer("🎓 O'zMU So'rov Tizimiga hush kelibsiz.\nBu tizim orqali o'qituvchilar haqida fikr va baholaringizni anonim ravishda ifodalash imkoniyati mavjud. 📚🔒")
            await message.answer("Fakultetni tanlang ✨", reply_markup=faculties_buttons)

            await StudentAnswer.faculty.set()

        else:
            await message.answer("Bot faollashtirilmagan!")
            await state.finish()
    
   


@dp.message_handler(state=StudentAnswer.faculty)
async def facult_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    faculty = message.text

    if faculty in data['faculty_list_check']:
        await state.update_data(faculty=faculty)

        kafedralar = backend.get_kafedra(faculty)

        await state.update_data(kafeda_list_check=kafedralar)

        kefedralar_buttons = get_keyboard(kafedralar)

        await message.answer("Kafedrani tanlang ✨", reply_markup=kefedralar_buttons)
        await StudentAnswer.kafedra.set()

    else:
        await message.answer("To'g'ri fakultetni tanlang ❌")
        await StudentAnswer.faculty.set()



@dp.message_handler(state=StudentAnswer.kafedra)
async def facult_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    kafedra = message.text
    if kafedra in data['kafeda_list_check']:

        await state.update_data(kafedra=kafedra)
        teachers = backend.get_teachers(kafedra)
        await state.update_data(teacher_list_check=teachers)

        teachers_buttons = get_keyboard(teachers)

        await message.answer("O'qituvchini tanlang 👩‍🏫👨‍🏫", reply_markup=teachers_buttons)

        await StudentAnswer.teacher.set()
    else:
        await message.answer("To'g'ri kafedrani tanlang ❌")
        await StudentAnswer.kafedra.set()


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
        if general_score <= 100 and 0 <= general_score:
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

    await message.answer("🎓 O'zMU So'rov Tizimiga hush kelibsiz.\nBu tizim orqali o'qituvchilar haqida fikr va baholaringizni anonim ravishda ifodalash imkoniyati mavjud. 📚🔒")
    await message.answer("Kafedrani tanlang ✨", reply_markup=faculties_buttons)

    await StudentAnswer.faculty.set()


# ====================== ADMIN ================== #
@ dp.message_handler(lambda message: message.text == "So'rovlar soni 📈")
async def back_page(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        count = backend.get_count_result()
        await message.answer(f"{count}", reply_markup=keyboard_back)
    else:
        await message.answer("Siz admin emassiz 🚫👨‍💼")


@dp.message_handler(lambda message: message.text == "Excel fayllar 📊")
async def back_page(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        faculties = backend.get_faculties()

        faculties = get_keyboard(faculties)
        faculties.add(types.KeyboardButton("Barchasi"))

        await message.answer("🔍 Tanlovni kerakli kafedrani topib, va Excel formatdagi fayllarni yuklab oling! 📊", reply_markup=faculties)
        await AdminState.faculty.set()
    else:
        await message.answer("Siz admin emassiz 🚫👨‍💼")

@dp.message_handler(lambda message: message.text == "Botning xolati")
async def back_page(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        global STATUS_SERVER
        status_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        status_kb.add(types.KeyboardButton("Boshlash"))
        status_kb.add(types.KeyboardButton("Tugatish"))

        await message.answer(f"Botning xolati: {STATUS_SERVER}", reply_markup=status_kb)
        await state.finish()
    else:
        await message.answer("Siz admin emassiz 🚫👨‍💼")



@dp.message_handler(lambda message: message.text == "Boshlash")
async def back_page(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        global STATUS_SERVER
        STATUS_SERVER = True

        await message.answer("So'rovni boshlandi", reply_markup=kb_back)
        await state.finish()
    else:
        await message.answer("Siz admin emassiz 🚫👨‍💼")



@dp.message_handler(lambda message: message.text == "Tugatish")
async def back_page(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        global STATUS_SERVER
        STATUS_SERVER = False
        await message.answer("So'rovni tugatildi", reply_markup=kb_back)
        await state.finish()
    else:
        await message.answer("Siz admin emassiz 🚫👨‍💼")



@dp.message_handler(state=AdminState.faculty)
async def facult_handler(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        fakeltet = message.text

        if fakeltet == "Barchasi":
            results = backend.report_result_by_facults(fakeltet)

            if not results:
                await message.answer("Ma'lumot yo'q 🚫", reply_markup=keyboard_back)
                await state.finish()
            else:
                import time
                time.sleep(2)
                await message.answer("Taxlil natijalari 📝 ", reply_markup=keyboard_back)

                import ananylize_survey
                ananylize_survey.generate_excel(results)

                folder_path = "./bot/files/"
                for file_name in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, file_name)
                    if os.path.isfile(file_path):
                        with open(file_path, 'rb') as file:
                            await bot.send_document(message.from_user.id, file)

                delete_files_in_folder(folder_path)

                await state.finish()

        else:
            kafedralar = backend.get_kafedra(fakeltet)
            kafedralar_kb = get_keyboard(kafedralar)
            await message.answer("Kafedra tanlang ✨", reply_markup=kafedralar_kb)
            await AdminState.kafedra.set()
        
    else:
        await message.answer("Siz admin emassiz 🚫👨‍💼")

@dp.message_handler(state=AdminState.kafedra)
async def facult_handler(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        await message.answer_chat_action("typing")

        kafedra = message.text

        results = backend.report_result_by_facults(kafedra)
        if not results:
            await message.answer("Ma'lumot yo'q 🚫", reply_markup=keyboard_back)
            await state.finish()
        else:
            import ananylize_survey
            ananylize_survey.generate_excel(results)

            import time
            time.sleep(2)
            await message.answer("Taxlil natijalari 📝 ", reply_markup=keyboard_back)


            folder_path = "./bot/files/"
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path):
                    with open(file_path, 'rb') as file:
                        await bot.send_document(message.from_user.id, file)

            delete_files_in_folder(folder_path)

            await state.finish()
    else:
        await message.answer("Siz admin emassiz 🚫👨‍💼")





@dp.message_handler(lambda message: message.text == "Orqaga ⬅️")
async def back_page(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        await message.answer("Asosiy saxifa 🏘", reply_markup=admin_kb)
    else:
        await message.answer("Siz admin emassiz 🚫👨‍💼")


@dp.message_handler(lambda message: message.text == "Ma'lumotlarni tozalash 🗑")
async def back_page(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:

        response_status = backend.delete_result()

        if response_status:
            await message.answer("Ma'lumotlarni o'chirishda xatolik yuz berdi", reply_markup=keyboard_back)

        await message.answer("Ma'lumotlar o'chirildi ✅", reply_markup=keyboard_back)
    else:
        await message.answer("Siz admin emassiz 🚫👨‍💼")
# ======================================= #





# ============== BOT SETTINGS ========== #
async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "🤖 Bot qayta ishga tushdi! 🎉\n🔗 <a href='http://127.0.0.1:8000/OzMUtizimi/'>Bot Admin Saxifasi</a> 🛠️", parse_mode="HTML")
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
# ===========================================#


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
