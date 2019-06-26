from django.contrib import admin
from hh_starwars.models import *


class PlanetsAdmin(admin.ModelAdmin):
    list_display = ('name',)


class AspirantsAdmin(admin.ModelAdmin):
    list_display = ('name', 'planet', 'age')


class JedisAdmin(admin.ModelAdmin):
    list_display = ('name', 'planet')


class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('text', 'right_answer')


admin.site.site_header = 'Академия Джедаев'
admin.site.site_title = 'Сайт Администратора'
admin.site.index_title = 'Администратор Академии Джедаев'

admin.site.register(Planets, PlanetsAdmin)
admin.site.register(Aspirants, AspirantsAdmin)
admin.site.register(Jedis, JedisAdmin)
admin.site.register(TestTasks)
admin.site.register(Questions, QuestionsAdmin)
