from question_app.models import Kafedra
from django.shortcuts import render
from .models import Student, Result
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from question_app.models import Faculty, Question, Answer, Teacher


class StudentAnswer(APIView):
    def post(self, request):
        teacher = request.data['teacher']
        teacher_id = Teacher.objects.get(name=teacher)

        question = request.data['question']
        question_id = Question.objects.get(name=question)

        choice = request.data['choice']
        choice_id = Answer.objects.get(name=choice)

        Student.objects.create(
            teacher=teacher_id, question=question_id, choice=choice_id)

        return Response({'error': 0, 'error_note': "success"}, status=status.HTTP_200_OK)


class StudentResult(APIView):
    def post(self, request):
        faculty_name = request.data.get('kafedra')
        teacher_name = request.data.get('teacher')
        question_answer = request.data.get('question_answer')
        general_score = request.data.get('general_score')
        comment = request.data.get('comment')

        faculty = Kafedra.objects.get(name=faculty_name)

        # Retrieve or create Teacher object
        teacher = Teacher.objects.get(
            name=teacher_name, kafedra=faculty)

        # Create Result object
        result = Result.objects.create(
            teacher=teacher, general_score=general_score, comment=comment)
        result.save()
        # Handle question-answer pairs
        for question_name, answer_name in question_answer.items():
            question = Question.objects.get(name=question_name)
            answer = Answer.objects.get(question=question, name=answer_name)
            result.answers.add(answer)

        return Response({"Result created successfully."}, status=status.HTTP_201_CREATED)


class CountResultAnswer(APIView):
    def get(self, request):
        result = Result.objects.all().count()
        return Response({"count": result}, status=status.HTTP_200_OK)


class DeleteResultAnswer(APIView):
    def delete(self, request):
        # Get all objects of Result and Answer models
        results_to_delete = Result.objects.all()
        student_to_delete = Student.objects.all()

        # Delete all objects
        results_to_delete.delete()
        student_to_delete.delete()

        # Return success response
        return Response({'status': "Success"}, status=status.HTTP_204_NO_CONTENT)


class ReportResult(APIView):
    def get(self, request):
        answers = Result.objects.all()
        main_data = []
        for answer in answers:
            data = {}
            data['FIO teacher'] = answer.teacher.name
            data['general_score'] = answer.general_score
            data['comment'] = answer.comment
            for i in answer.answers.all():
                data[i.question.name] = int(i.mark.name)
            main_data.append(data)
        return Response(main_data)


class ReportResultByFaculty(APIView):
    def get(self, request, kafedra):
        if kafedra == "Barchasi":
            answers = Result.objects.all()
        else:
            answers = Result.objects.filter(teacher__kafedra__name=kafedra)
        main_data = []
        for answer in answers:
            data = {}
            data['FIO teacher'] = answer.teacher.name
            data['general_score'] = answer.general_score
            data['comment'] = answer.comment
            for i in answer.answers.all():
                data[i.question.name] = int(i.mark.name)
            main_data.append(data)
        return Response(main_data)
