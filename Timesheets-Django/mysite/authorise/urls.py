from django.urls import path
from . import views
# from django.contrib.auth.views import logout_then_login


app_name = 'authorise'
urlpatterns = [
    path('', views.landing, name='landing'),
    path('logoutUser/', views.logoutUser, name='logout'),
]