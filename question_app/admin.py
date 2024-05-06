from django.contrib import admin
from .models import Faculty, Teacher, Question, Answer, Mark

class AnswerAdmin(admin.ModelAdmin):
    list_display = ['name', 'question', 'mark']


admin.site.register(Answer, AnswerAdmin)


class TearcherAdmin(admin.ModelAdmin):
    list_display = ['name', 'kafedra']


admin.site.register(Teacher, TearcherAdmin)


class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Faculty, FacultyAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Question, QuestionAdmin)


admin.site.register(Mark)
from .models import Kafedra
admin.site.register(Kafedra)