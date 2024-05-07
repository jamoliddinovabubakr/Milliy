from aiogram.dispatcher.filters.state import StatesGroup, State


class StudentAnswer(StatesGroup):
    faculty_list_check = State()
    teacher_list_check = State()
    answers_list_check = State()
    department_list_check = State()

    faculty = State()
    teacher = State()
    department = State()
    general_score = State()
    comment = State()

    iter = State()
    questions = State()
    question_answer = State()

    finish = State()


class AdminState(StatesGroup):
    faculty = State()
    department = State()
