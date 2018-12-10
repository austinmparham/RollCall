from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^login$',views.login),
	url(r'^home$',views.home),
	url(r'^new_roster$',views.new_roster),
	url(r'^check_in/(?P<id>\d+)$',views.check_in),
	url(r'^remove_child/(?P<id>\d+)$',views.remove),
	url(r'^back$',views.back),
	url(r'^submit_roster$',views.submit_roster),
	url(r'^roster_list$',views.roster_list),
	url(r'^view_roster/(?P<id>\d+)$',views.view_roster),
	url(r'^logout$',views.logout),
	url(r'^view_kids$',views.view_kids),
	url(r'^register_child$',views.register_child),
	url(r'^submit_child$', views.submit_child),
	url(r'^new_day$', views.new_day),
	url(r'^photo_check$', views.photo_check),
	url(r'^live_check$',views.live_check),
	url(r'^face_code$',views.face_code)
]