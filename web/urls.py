from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register, name='register'),
    path('register/done/', views.register_done, name='register_done'),
    path('profiles/', views.profiles, name='profiles'),
    path('profiles-update/', views.profiles_update, name='profiles_update'),
    path('profiles/<int:uid>/delete', views.profiles_delete, name='profiles_delete'),
    path('keywords/', views.keywords, name='keywords'),
    path('keywords/<str:keyword>/delete', views.keywords_delete, name='keywords_delete'),
    path('reports/', views.reports, name='reports'),
    path('comment/<int:comment_id>/read', views.comment_read, name="comment_read"),
]
