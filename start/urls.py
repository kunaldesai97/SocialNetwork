from django.conf.urls import url, include
from . import views

urlpatterns = [
				url(r'^$', views.LoginFormView.as_view(), name ='login'),
				url(r'^signup/', views.UserFormView.as_view(), name = 'signup')]