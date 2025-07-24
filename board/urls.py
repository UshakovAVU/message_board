# from django.conf import settings
# from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('', views.advertisement_list, name='advertisement_list'),
    path('stat/', views.user_stat_list, name='user_stat_list'),
    path('settings/', views.user_settings, name='user_settings'),
    path('<int:pk>/', views.advertisement_list, name='advertisement_list'),
    path('advertisement/<int:pk>/', views.advertisement_detail, name='advertisement_detail'),
    path('edit/<int:pk>/', views.edit_advertisement, name='edit_advertisement'),
    path('edit_comment/<int:pk>/', views.edit_comment, name='edit_comment'),
    path('delete_comment/<int:pk>/', views.delete_comment, name='delete_comment'),
    path('image_generation/<int:pk>/', views.image_generation, name='image_generation'),
    path('del/<int:pk>/', views.del_advertisement, name='del_advertisement'),
    path('add/', views.add_advertisement, name='add_advertisement'),
    path('add_comment/<int:pk>/', views.add_comment, name='add_comment'),
    path('add_image/<int:pk>/', views.add_image, name='add_image'),
    path('like/<int:pk>/<int:tp>/', views.like_dislike, name='like_dislike'),
]

