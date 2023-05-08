from django.urls import path
from myparser import views
 
urlpatterns = [
    path('', views.form_view, name='form_view'),
]
