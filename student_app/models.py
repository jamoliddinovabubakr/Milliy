from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Student(models.Model):
    answer = models.ForeignKey("question_app.Answer", on_delete=models.CASCADE)
    question = models.ForeignKey('question_app.Question', models.CASCADE)

    def __str__(self):
        return f"{self.answer} - {self.question}"

    class Meta:
        verbose_name = "Talaba Ovozi"
        verbose_name_plural = "Talaba Ovozlari"


class Result(models.Model):
    teacher = models.ForeignKey(
        'question_app.Teacher', on_delete=models.CASCADE)
    answers = models.ManyToManyField('question_app.Answer')
    general_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.teacher} - {self.general_score}"

    class Meta:
        verbose_name = 'Talaba Javobi'
        verbose_name_plural = 'Talaba Javoblari'


"""

{
["FIO teacher": "Karim",
"Question_1": 1,
"Question_2": 0,
...

"genral_score": int,
"comment": "str",



"FIO teacher": "Karim",
"Question_1": 1,
"Question_2": 0,
...

"genral_score": int,
"comment": "str"




"FIO teacher": "Karim",
"Question_1": 1,
"Question_2": 0,
...

"genral_score": int,
"comment": "str"
]
}
"""
