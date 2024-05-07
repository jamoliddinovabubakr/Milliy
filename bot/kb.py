from aiogram import types

admin_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
admin_kb.add(types.KeyboardButton("So'rovlar soni 📈"))
admin_kb.add(types.KeyboardButton('Excel fayllar 📊'))
admin_kb.add(types.KeyboardButton("Ma'lumotlarni tozalash 🗑"))
admin_kb.add(types.KeyboardButton("Botning xolati 🤖"))

kb_back = [
    [types.KeyboardButton('Orqaga ⬅️')]
]
keyboard_back = types.ReplyKeyboardMarkup(
    keyboard=kb_back, resize_keyboard=True)
