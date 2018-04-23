from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main_page, name='main_page'),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
]