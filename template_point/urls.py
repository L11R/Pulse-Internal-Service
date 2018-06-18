from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^auth_client/', views.auth_client, name='main_page'),
    url(r'^auth_sender/', views.auth_sender),
    url(r'^next/', views.next),
    url(r'^reminder_cell_is_open/', views.reminder_cell_is_open),
    #url(r'^auth_client/', views.auth_client, name='main_page'),
]