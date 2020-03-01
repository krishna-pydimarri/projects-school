from django.urls import path
#from django.contrib.auth import views as auth_views
from . import views

app_name = 'timekeeping'
urlpatterns = [
    #path('', views.index, name='index'),
    path('timesheet', views.timesheet, name='timesheet'),
    path('multibarhorizontalchart/', views.multibarhorizontalchart, name='multibarhorizontalchart'),
    #path('week_display', views.week_display, name='week_display'),
    path('', views.home, name='home'),
    path('thanks-page/', views.sub_func, name='sub_func'),
    path('timekeeping/templates/login', views.Login, name='login'),
    path('test', views.test, name='test'),
    path('<int:dimemployees_id>/detail/', views.detail, name='detail'),
    

]

