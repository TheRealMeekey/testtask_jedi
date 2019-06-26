from django.db import models
from django.core.validators import MinValueValidator


class Planets(models.Model):
    class Meta:
        verbose_name = 'Планета'
        verbose_name_plural = 'Планеты'

    name = models.CharField(max_length=64, verbose_name='Наименование')

    def __str__(self):
        return self.name


# Менеджер для модели Jedis
class JediManager(models.Manager):
    # Добавляет поле количество падаванов к джедаю
    def get_queryset(self):
        return super(JediManager, self).get_queryset().annotate(padawans_cnt=models.Count('aspirants'))

    # Меньше трех падаванов
    def can_teach(self):
        return self.get_queryset().filter(padawans_cnt__lte=3)

    # Больше одного падавана
    def more_than_one(self):
        return self.get_queryset().filter(padawans_cnt__gt=1)


class Jedis(models.Model):
    class Meta:
        verbose_name = 'Джедай'
        verbose_name_plural = 'Джедаи'

    name = models.CharField(max_length=64, verbose_name='Имя')
    planet = models.ForeignKey(Planets, on_delete=models.CASCADE, verbose_name='Планета на которой он обучает')
    objects = models.Manager()  # для удобства оставим дефолтный менеджер
    with_padawans = JediManager()

    def __str__(self):
        return self.name


# Менеджер для модели Aspirants,
# нужен для того, чтобы отделять кандидатов, которые еще не стали джедаями
class AspirantManager(models.Manager):
    def get_queryset(self):
        return super(AspirantManager, self).get_queryset().filter(jedi=None)


class Aspirants(models.Model):
    class Meta:
        verbose_name = 'Кандидат'
        verbose_name_plural = 'Кандидаты'

    name = models.CharField(max_length=64, verbose_name='Имя')
    planet = models.ForeignKey(Planets, on_delete=models.CASCADE, verbose_name='Планета обитания')
    age = models.PositiveIntegerField(validators=[MinValueValidator(0)], verbose_name='Возраст')
    email = models.EmailField(verbose_name='Email')
    jedi = models.ForeignKey(Jedis, on_delete=models.CASCADE, null=True, verbose_name='Джедай')
    objects = AspirantManager()

    def __str__(self):
        return "{} c {}".format(self.name, self.planet)


class Questions(models.Model):
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    text = models.TextField(verbose_name='Вопрос')
    right_answer = models.BooleanField(verbose_name='Ответ')

    def __str__(self):
        return self.text[:20] + "..."


class Answers(models.Model):
    class Meta:
        unique_together = (('aspirant', 'question'),)

    aspirant = models.ForeignKey(Aspirants, on_delete=models.CASCADE, verbose_name='Кандидат', related_name='aspirant')
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, verbose_name='Вопрос')
    answer = models.BooleanField(verbose_name='Ответ')


class TestTasks(models.Model):
    class Meta:
        verbose_name = 'Тестовое испытание'
        verbose_name_plural = 'Тестовые испытания'

    # На каждой планете имеется только один орден
    # Вопрос можно было бы добавлять с помощью inline, но я не стал вводить еще одну модель
    order = models.OneToOneField(Planets, on_delete=models.CASCADE, verbose_name='Орден')
    question = models.ManyToManyField(Questions, verbose_name='Вопросы')

    def __str__(self):
        return "{} тест".format(self.order)
