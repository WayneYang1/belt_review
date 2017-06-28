from django.conf.urls import url
#from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^books$', views.books, name='books'),
    url(r'^books/(?P<book_id>\d+)$', views.book_id, name='book_id'),
    url(r'^books/add$', views.add, name='add'),
    url(r'^post_book$', views.post_book, name='post_book'),
    url(r'^delete/(?P<review_id>\d+)$', views.delete, name='delete'),
    url(r'^update/(?P<book_id>\d+)$', views.update, name='update'),
    url(r'^users/(?P<user_id>\d+)?$', views.users, name='users'),
    url(r'^logout$', views.logout, name='logout')
]
