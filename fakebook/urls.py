from django.conf.urls import patterns, url

from fakebook import views



urlpatterns = patterns('',

	# ex: /fakebook/
	url(r'^$', views.index, name='index'),

	url(r'^users/(?P<username>.*)/', views.user, name='user'),

	url(r'^comments/(?P<username>.*)/', views.comments, name='comments'),
	
	url(r'^photos/(?P<photo>.*)/$', views.photo, name='photo'),
	
	url(r'^comment/(?P<photo>.*)/$', views.comment, name='comment'),

	url(r'^like/(?P<photo>.*)/$', views.vote, {'like': True}, name='like'),
	
	url(r'^dislike/(?P<photo>.*)/$', views.vote, {'like': False}, name='dislike'),
	
	url(r'^upload/$', views.upload, name='upload'),
	
#	url(r'^commentPhoto/(?P<photo>.*)/$', views.commentPhoto, name='commentPhoto'),
	
	url(r'^login/$', views.log_in, name='log_in'),
	
	url(r'^logout/$', views.log_out, name='log_out'),
	
)
	
