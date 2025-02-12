from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('upload/', views.upload, name='upload'),
    path('upload/', views.upload_image, name='upload'),
    path('predict/', views.predict_blood_group, name='predict_blood_group'),
    path('result/', views.result, name='result'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
