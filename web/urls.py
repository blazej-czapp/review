from django.urls import path

from . import views

app_name = 'web'
urlpatterns = [
    path('', views.index, name='index'),
    path('add_new_review_item', views.add_new_review_item, name='add_new_review_item'),
    path('edit_existing_review_item', views.edit_existing_review_item, name='edit_existing_review_item'),
    path('reviewed', views.reviewed, name='reviewed'),
    path('review_list', views.review_list, name='review_list'),
    path('get_raw_review_item_data', views.get_raw_review_item_data, name='get_raw_review_item_data'),
    path('render_markdown', views.render_markdown, name='render_markdown'),
]
