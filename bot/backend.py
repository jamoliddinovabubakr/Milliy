import json
import requests

# Base URL for your API
base_url = 'http://localhost:8000/'


def get_faculties():
    url = base_url + 'question/faculty-list/'
    response = requests.get(url)
    if response.status_code == 200:
        faculties = response.json()['faculties']
        values_only = [d['name'] for d in faculties]
        return values_only
    else:
        return 0


def get_kafedra(faculty):
    url = base_url + f'question/kafedra/{faculty}/'
    response = requests.get(url)
    if response.status_code == 200:
        kafedra = response.json()['kafedra']
        values_only = [d['name'] for d in kafedra]
        return values_only
    else:
        return 0
    

def get_questions():
    url = base_url + 'question/question-list/'
    response = requests.get(url)
    if response.status_code == 200:
        questions = response.json()['questions']
        return questions
    else:
        return 0


def get_answers(question_name):
    url = base_url + f'question/answer-list/{question_name}'
    response = requests.get(url)
    if response.status_code == 200:
        answers = response.json()['answers']
        values_only = [d['name'] for d in answers]
        return values_only
    else:
        return 0


def get_teachers(faculty_name):
    url = base_url + f'question/teacher-list/{faculty_name}/'
    response = requests.get(url)
    if response.status_code == 200:
        teachers = response.json()['teachers']
        values_only = [d['name'] for d in teachers]

        return values_only
    else:
        return 0


def result(data):
    desired_data = {
        "kafedra": data['kafedra'],
        "teacher": data['teacher'],
        "question_answer": data['question_answer'],
        "general_score": data['general_score'],
        "comment": data['comment']
    }
    url = base_url + f'student/result/'

    response = requests.post(url, json=desired_data)
    if response.status_code == 201:
        return 0
    else:
        return 1


def report_result():
    url = base_url + f'student/report-result/'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return 0


def report_result_by_facults(kafedra):
    url = base_url + f"student/report-result-kafedra/{kafedra}/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return 0


def get_count_result():
    url = base_url + "student/count-result/"
    response = requests.get(url=url)
    if response.status_code == 200:
        count = response.json()
        return count['count']
    else:
        return 0


def delete_result():
    url = base_url + 'student/delete-result/'
    response = requests.delete(url=url)
    if response.status_code == 204:
        return 0
    else:
        return 1


