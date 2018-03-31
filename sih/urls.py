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
    url(r'^dept_admin/$', views.dept_admin, name='dept_admin'),
    url(r'^dashboard/$',views.dashboard, name='dashboard'),
    url(r'^apply/(?P<job1>[-\w]+)/$',views.apply, name='apply')
    url(r'^change_status/(?P<jobID>\d+)/$', views.change_status, name='change_status'),
]
