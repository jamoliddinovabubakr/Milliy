from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=255)
    kafedra = models.ForeignKey('Kafedra', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "O'qituvchi"
        verbose_name_plural = "O'qituvchilar"


# - matem facult 
#       - kafedra

class Faculty(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Fakultet"
        verbose_name_plural = "Fakultetlar"



class Kafedra(models.Model):
    name = models.CharField(max_length=255)
    faculty = models.ForeignKey('Faculty', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kafedra"
        verbose_name_plural = "Kafedralar"


class Question(models.Model):
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"


class Answer(models.Model):
    name = models.CharField(max_length=255)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    mark = models.ForeignKey('Mark', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Javob'
        verbose_name_plural = "Javoblar"


class Mark(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Savolni baxolash'
        verbose_name_plural = "Savollarni baxolash"
