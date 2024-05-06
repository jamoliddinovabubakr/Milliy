from django.urls import path
from . import views

urlpatterns = [
    path('faculty-list/', views.FacultyList.as_view()),
    path('question-list/', views.QuestionList.as_view()),

    path('answer-list/<str:question_name>/', views.AnswerList.as_view()),
    path('teacher-list/<str:faculty_name>/', views.TeacherList.as_view()),

    path('kafedra/<str:faculty>/', views.KafedraList.as_view())

]
