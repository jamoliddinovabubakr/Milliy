from rest_framework import serializers
from .models import Faculty, Question, Answer, Teacher


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['name']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields =  ['name']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

from .models import Kafedra
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kafedra
        fields = ['name']
