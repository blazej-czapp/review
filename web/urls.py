from django.urls import path

from . import views

app_name = 'web'
urlpatterns = [
    path('', views.index, name='index'),
    path('add_new_resource', views.add_new_resource, name='add_new_resource'),
    path('reviewed', views.reviewed, name='reviewed'),
    path('review_list', views.review_list, name='review_list'),
]
