from django.urls import path
from . import views

urlpatterns = [
    path('result/', views.StudentResult.as_view()),
    path('report-result/', views.ReportResult.as_view()),

    path('count-result/', views.CountResultAnswer.as_view()),

    path('delete-result/', views.DeleteResultAnswer.as_view()),

    path('report-result-kafedra/<str:kafedra>/', views.ReportResultByFaculty.as_view())

]
