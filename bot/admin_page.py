from main import bot, dp
from aiogram import types
from aiogram.dispatcher.storage import FSMContext

import backend
from kb import *
from utils import *
from states import *

from main import ADMINS
from main import STATUS_SERVER


@dp.message_handler(lambda message: message.text == "So'rovlar soni 📈")
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

        await message.answer("🔍 Kerakli kafedrani topib, Excel formatdagi asonim javoblarni fayllarni yuklab oling! 📊",
                             reply_markup=faculties)
        await AdminState.faculty.set()
    else:
        await message.answer("Siz admin emassiz 🚫👨‍💼")


@dp.message_handler(lambda message: message.text == "Botning xolati 🤖")
async def back_page(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        status_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        status_kb.add(types.KeyboardButton("Faollashtirish ✅"))
        status_kb.add(types.KeyboardButton("Tugatish 🚫"))
        status_kb.add(types.KeyboardButton("Orqaga ⬅️"))
        import main
        if main.STATUS_SERVER:
            await message.answer(f"Botning xolati: Faol ✅", reply_markup=status_kb)
        else:
            await message.answer(f"Botning xolati: O'chiq 🚫", reply_markup=status_kb)
        await state.finish()
    else:
        await message.answer("Siz admin emassiz 🚫👨‍💼")


@dp.message_handler(lambda message: message.text == "Faollashtirish ✅")
async def back_page(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        import main
        main.STATUS_SERVER = True

        await message.answer("So'rovni boshlandi", reply_markup=keyboard_back)
    else:
        await message.answer("Siz admin emassiz 🚫👨‍💼")


@dp.message_handler(lambda message: message.text == "Tugatish 🚫")
async def back_page(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        import main
        main.STATUS_SERVER = False
        await message.answer("So'rovni tugatildi", reply_markup=keyboard_back)
        await state.finish()
    else:
        await message.answer("Siz admin emassiz 🚫👨‍💼")


@dp.message_handler(state=AdminState.faculty)
async def faculty_handler(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        faculty = message.text

        if faculty == "Barchasi":
            results = backend.report_result_by_facults(faculty)

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
            department = backend.get_kafedra(faculty)
            department_kb = get_keyboard(department)
            await message.answer("Kafedra tanlang ✨", reply_markup=department_kb)
            await AdminState.department.set()

    else:
        await message.answer("Siz admin emassiz 🚫👨‍💼")


@dp.message_handler(state=AdminState.department)
async def department_handler(message: types.Message, state: FSMContext):
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
