from django.conf.urls import url
from parserapp import views

urlpatterns = [
	#url(r'^index', views.render_page),
	url(r'^$', views.render_page_points),
	url(r'^update/$', views.update_list_points)
]
