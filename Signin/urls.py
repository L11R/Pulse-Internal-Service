from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.checked, name='main_page'),
    url(r'', views.checked),
    url(r'^cameras/', views.cameras_page),
    url(r'^cameras_more/', views.cameras_more),
    url(r'^menu/', views.menu_page),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    url(r'^technical/', views.techn_page),
    url(r'^leroy/', views.leroy_page),
    url(r'^terminals/', views.terminal_page),
    url(r'^parcels/', views.parcels_page),
    url(r'^rental', views.lease_page),
    url(r'^menu_rental', views.menu_lease),
    url(r'^add_users', views.new_users),
    url(r'^views_point', views.template_views),
]