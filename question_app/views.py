from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Faculty, Question, Answer, Teacher
from .serialisers import *


class FacultyList(APIView):
    def get(self, request):
        faculties = Faculty.objects.all().order_by('name')
        serializer = FacultySerializer(faculties, many=True)
        return Response({'error': 0, 'faculties': serializer.data}, status=status.HTTP_200_OK)


class QuestionList(APIView):
    def get(self, request):
        questions = Question.objects.filter(status=True)
        serializer = QuestionSerializer(questions, many=True)
        return Response({'error': 0, 'questions': serializer.data}, status=status.HTTP_200_OK)


class AnswerList(APIView):
    def get(self, request,  question_name):
        question = Question.objects.get(name=question_name)
        answers = Answer.objects.filter(question=question)
        serializer = AnswerSerializer(answers, many=True)
        return Response({'error': 0, 'answers': serializer.data}, status=status.HTTP_200_OK)


class TeacherList(APIView):
    def get(self, request, faculty_name):
        kafedra = Kafedra.objects.get(name=faculty_name)
        teachers = Teacher.objects.filter(kafedra=kafedra).order_by('name')
        serializer = TeacherSerializer(teachers, many=True)
        return Response({'error': 0, 'teachers': serializer.data}, status=status.HTTP_200_OK)

from .models import Kafedra

class KafedraListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kafedra
        fields = ['name']

class KafedraList(APIView):
    def get(self, requst, faculty):
        kafedra = Kafedra.objects.filter(faculty__name=faculty).order_by('name')
        serializer = KafedraListSerializer(kafedra, many=True)
        return Response({'error': 0, 'kafedra': serializer.data}, status=status.HTTP_200_OK)

    