from django.conf.urls import url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import login

urlpatterns = [
 				url(r'^$', views.LoginFormView.as_view(), name ='login'),
				url(r'^signup/', views.UserFormView.as_view(), name = 'signupform'),
				url(r'^user/friends/(?P<username>[%&+ \w]+)',views.friends, name = 'friends'),
				url(r'^user/profile/(?P<username>[%&+ \w]+)',views.ProfileFormView.as_view(),name = 'profile'),
				url(r'^user/imagepost/(?P<username>[%&+ \w]+)', views.ImagePostFormView.as_view(),name = 'postimage'),
				url(r'^user/displayprofile/(?P<username>[%&+ \w]+)',views.displayProfile,name='disppro'),
				url(r'^user/(?P<username>[%&+ \w]+)', views.homepage, name = 'userhome'),
				url(r'^accept/(?P<seid>[%&+ \w]+)/(?P<reid>[%&+ \w]+)',views.AcceptView.as_view(), name = 'accept'),
				url(r'^reject/(?P<seid>[%&+ \w]+)/(?P<reid>[%&+ \w]+)',views.RejectView.as_view(), name = 'reject'),
				url(r'^sendreq/(?P<reqid>[%&+ \w]+)/(?P<seid>[%&+ \w]+)',views.sendreq, name = 'sendrequest'),
				url(r'^like/(?P<image_id>[%&+ \w]+)/(?P<user_id>[%&+ \w]+)',views.like,name = 'like'),
				
				url(r'^logout/', views.logout, name = 'logout'),
				]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
# 	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
# 	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
# 				] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
				# url(r'^accept/', views.accept, name = 'accept')]
				# url(r'^user/', views.userhome, name = 'userhome')]