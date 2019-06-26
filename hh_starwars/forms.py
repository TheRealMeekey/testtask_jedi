from django import forms
from django.core.exceptions import PermissionDenied
from hh_starwars.models import *
from django.db import IntegrityError


class AspirantForms(forms.ModelForm):
    class Meta:
        model = Aspirants
        exclude = ('jedi',)


class TestTaskForms(forms.Form):
    # Cоздание полей, в зависимости о количества вопросов
    def __init__(self, *args, **kwargs):
        aspirant = kwargs.pop('aspirant', None)
        questions = kwargs.pop('questions', None)
        super(TestTaskForms, self).__init__(*args, **kwargs)
        self.aspirant = aspirant
        # Cоздание полей, где id вопроса является названием поля, а text вопроса - лейблом поля
        for q in questions:
            self.fields[str(q[0])] = forms.BooleanField(label=q[1], required=False)

    def save(self):
        # try/except нужен для того, чтобы избежать попытки несколько
        # раз ответить на один вопрос одним кандидатом; если такое событие произошло отдаю 403
        try:
            for k, v in self.cleaned_data.items():
                Answers.objects.create(question_id=k, aspirant=self.aspirant, answer=v)
        except IntegrityError:
            raise PermissionDenied


class JediSelectForm(forms.Form):
    jedi = forms.ModelChoiceField(label='Джедай', queryset=Jedis.with_padawans.can_teach())


class AddPadawan(forms.Form):
    take = forms.BooleanField(label='Возьмете в падаваны?', required=False)

    def save(self):
        if self.cleaned_data['take']:
            jedi = self.initial['jedi']
            aspirant = self.initial['aspirant']
            aspirant.jedi = jedi
            aspirant.save()
