from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^profile/edit/$', views.profile_edit, name='profile_edit'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^vacancies/$', views.vacancies, name='vacancies'),
    url(r'^vacancy/(?P<pk>\d+)/$', views.vacancy_detail, name='vacancy_detail'),
    url(r'^activate/$', views.activate, name='activate'),
]