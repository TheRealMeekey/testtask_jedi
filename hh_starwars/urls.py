from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='hh_starwars/index.html'), name='home'),
    path('aspirant/', views.NewAspirantView.as_view(), name='new_aspirant'),
    path('aspirant/<int:aspirants_id>/order/<int:order_id>/', views.TestView.as_view(), name="test"),
    path('aspirant/passed/', TemplateView.as_view(template_name='hh_starwars/passed_aspirant.html'), name='passed'),
    path('jedi/', views.JediSelectView.as_view(), name='select_jedi'),
    path('jedi/<int:jedi_id>/aspirants/list/', views.JediView.as_view(), name='jedi'),
    path('jedi/<int:jedi_id>/aspirants/<int:aspirants_id>/', views.AspirantToPadawanView.as_view(), name='aspirant'),
    path('jedi/list/', views.JediListView.as_view(), name='jedi_list'),
    path('jedi/list/gt1/', views.JediListMoreThanOneView.as_view(), name='jedi_list_gt1')
]
