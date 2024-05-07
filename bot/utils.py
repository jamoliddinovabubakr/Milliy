import os
from aiogram import types


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
