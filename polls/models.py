from django.conf import settings
from django.db import models
from django.urls import reverse

MC = 'MC'
CN = 'CN'
TX = 'TX'

CATEGORY = (
    (MC, 'Multichoice'),
    (CN, 'Choose N'),
    (TX, 'Text'),
)


class Poll(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_start = models.TimeField(null=True, blank=True)
    time_end = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Опросник'
        verbose_name_plural = 'Опросники'
        ordering = ['title']

    def get_absilute_urls(self):
        return reverse('poll', kwargs={'polls_id': self.pk})


class Question(models.Model):
    title = models.CharField(max_length=255)
    polls = models.ManyToManyField(Poll)

    question_category = models.CharField(max_length=2, choices=CATEGORY)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['title']


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=256)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Варианты'
        verbose_name_plural = 'Вариант'
        ordering = ['title']


class Answer(models.Model):
    user = models.SmallIntegerField()
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    choices = models.ForeignKey(Choice, on_delete=models.DO_NOTHING,null=True)
    choices_text = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.choices_text.title

    class Meta:
        verbose_name = 'Ответы'
        verbose_name_plural = 'Ответ'
