from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^books$', views.books),
    url(r'^logout$', views.logout),
    url(r'^books/add$', views.addbook),
    url(r'^books/add/submit$', views.submitbook),
    url(r'^books/(?P<book_id>\d+)$', views.bookpage),
    url(r'^books/(?P<book_id>\d+)/addreview$', views.addreview),
    url(r'^books/(?P<book_id>\d+)/deletereview/(?P<review_id>\d+)$', views.deletereview),
    url(r'^users/(?P<user_id>\d+)$', views.userpage),
]