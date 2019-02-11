from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.checked, name='main_page'),
    url(r'^cameras/', views.cameras_page),
    url(r'^cameras_more/', views.cameras_more),
    url(r'^menu/', views.menu_page),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    url(r'^technical/', views.techn_page),
    url(r'^leroy/', views.leroy_page),
    url(r'^terminals/', views.terminal_page),
    url(r'^parcels/', views.parcels_page),
    url(r'^add_users', views.new_users),
    url(r'^views_point', views.template_views),
    url(r'^add_camera', views.add_camera),
    url(r'^request_leroy', views.request_orders_file),
    url(r'^statistic_cells', views.statistic_cells),
    url(r'^get_leroy_parcels', views.get_leroy_parcels),
    url(r'^add_apps', views.add_apps),
    url(r'^sms_statics', views.sms_static_page)
]