from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('pay/', views.Pay.as_view(), name='pay'),
    path('finish/', views.Finish.as_view(), name='finish'),
    path('details/', views.Details.as_view(), name='details'),
]
