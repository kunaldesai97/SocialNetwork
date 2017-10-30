from django.conf.urls import url, include
from . import views

urlpatterns = [
				url(r'^$', views.LoginFormView.as_view(), name ='login'),
				url(r'^signup/', views.UserFormView.as_view(), name = 'signupform'),
				url(r'^user/(?P<username>[%&+ \w]+)', views.userhome, name = 'userhome'),
				url(r'^accept/(?P<seid>[%&+ \w]+)/(?P<reid>[%&+ \w]+)',views.AcceptView.as_view(), name = 'accept'),
				url(r'^reject/(?P<seid>[%&+ \w]+)/(?P<reid>[%&+ \w]+)',views.RejectView.as_view(), name = 'reject'),
				url(r'^sendreq/(?P<reqid>[%&+ \w])+/(?P<seid>[%&+ \w]+)',views.sendreq, name = 'sendrequest'),
				]
				# url(r'^accept/', views.accept, name = 'accept')]
				# url(r'^user/', views.userhome, name = 'userhome')]