from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, FormView
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from hh_starwars.forms import AspirantForms, TestTaskForms, JediSelectForm, AddPadawan
from hh_starwars.models import TestTasks, Aspirants, Jedis, Answers


class NewAspirantView(CreateView):
    form_class = AspirantForms
    template_name = 'hh_starwars/new_aspirant.html'

    def get_success_url(self):
        return reverse('test', kwargs={'aspirants_id': self.object.pk,
                                       'order_id': self.object.planet_id})


class TestView(FormView):
    form_class = TestTaskForms
    template_name = 'hh_starwars/test.html'
    success_url = reverse_lazy('passed')

    # передаем в класс формы именованные аргументы
    # для динамического создания полей и сохранения формы
    def get_form_kwargs(self):
        aspirants_id = self.kwargs.get('aspirants_id', None)
        aspirant = get_object_or_404(Aspirants, id=aspirants_id)
        order_id = self.kwargs.get('order_id', None)
        # получаем список вопросов из определенного испытания
        questions = get_object_or_404(TestTasks, order_id=order_id).question.all()
        form_kwargs = super(TestView, self).get_form_kwargs()
        form_kwargs['aspirant'] = aspirant
        form_kwargs['questions'] = [(q.id, q.text) for q in questions]
        return form_kwargs

    def form_valid(self, form):
        form.save()
        return super(TestView, self).form_valid(form)


class JediSelectView(FormView):
    form_class = JediSelectForm
    template_name = 'hh_starwars/select_jedi.html'

    def form_valid(self, form):
        return redirect(reverse('jedi', kwargs={'jedi_id': form.cleaned_data['jedi'].id}))


class JediView(ListView):
    template_name = 'hh_starwars/jedis_aspirantes.html'
    context_object_name = 'aspirant'

    # возвращаем список кандидатов с планеты джедая
    def get_queryset(self):
        jedi_id = self.kwargs.get('jedi_id', None)
        jedi = get_object_or_404(Jedis, id=jedi_id)
        return Aspirants.objects.filter(planet=jedi.planet)

    # добавляем в контекст id джедая для формирования урла
    def get_context_data(self, **kwargs):
        context = super(JediView, self).get_context_data(**kwargs)
        context['jedi_id'] = self.kwargs['jedi_id']
        return context


# использую FormMixin для отображения формы внутри DetailView
class AspirantToPadawanView(DetailView, FormMixin):
    model = Aspirants
    template_name = 'hh_starwars/aspirant_detail.html'
    pk_url_kwarg = 'aspirants_id'
    form_class = AddPadawan
    success_url = '/'

    # передаем в форму кандидата и джедая для последующей связи
    def get_initial(self):
        aspirants_id = self.kwargs.get('aspirants_id', None)
        aspirant = get_object_or_404(Aspirants, id=aspirants_id)
        jedi_id = self.kwargs.get('jedi_id', None)
        jedi = get_object_or_404(Jedis, id=jedi_id)
        return {'aspirant': aspirant,
                'jedi': jedi}

    def form_valid(self, form):
        form.save()
        return super(AspirantToPadawanView, self).form_valid(form)

    def send_message(self):
        mail_subject = 'Ты принят'
        init_dict = self.get_initial()
        aspirant = init_dict.get('aspirant')
        jedi = init_dict.get('jedi')
        message = render_to_string('hh_starwars/email.html', {
            'aspirant': aspirant,
            'jedi': jedi
        })
        to_email = aspirant.email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()

    # DetailView по-дефолту не принимает POST запрос, сделаем так, чтобы принимал
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            self.send_message()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class JediListView(ListView):
    queryset = Jedis.with_padawans.all()
    template_name = 'hh_starwars/list_jedi.html'
    context_object_name = 'jedis'


class JediListMoreThanOneView(JediListView):
    queryset = Jedis.with_padawans.more_than_one()
