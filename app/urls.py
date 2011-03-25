from django.conf.urls.defaults import *
from django.views.generic import DetailView
from django.views.generic import ListView
from app.model import Session

import views

urlpatterns = patterns('app',
    url(r'^$', views.home, name="home"),
    url(r'^sessions/$',
        ListView.as_view(
            model=Session,
            context_object_name="session_list")),
    url(r'^sessions/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Session)),
    url(r'^logout/$',
        views.logout_view,
        name="logout"),
    url(r'^login_form/$',
        views.login_form,
        name="login_form"),
)
