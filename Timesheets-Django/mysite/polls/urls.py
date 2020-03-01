# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 10:39:16 2019

@author: Krishna
"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]