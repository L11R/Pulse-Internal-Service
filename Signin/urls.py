from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.checked, name='main_page'),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    url(r'^technical/', views.techn_page),
    url(r'^leroy/', views.leroy_page),
]