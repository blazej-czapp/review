from django.urls import path

from . import views

app_name = 'web'
urlpatterns = [
    path('', views.index, name='index'),
    path('add_new_resource', views.add_new_resource, name='add_new_resource'),
    path('edit_existing_resource', views.edit_existing_resource, name='edit_existing_resource'),
    path('reviewed', views.reviewed, name='reviewed'),
    path('review_list', views.review_list, name='review_list'),
    path('get_raw_resource_data', views.get_raw_resource_data, name='get_raw_resource_data'),
]
