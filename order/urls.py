from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('pay/<int:pk>', views.Pay.as_view(), name='pay'),
    path('finish/', views.Finish.as_view(), name='finish'),
    path('details/<int:pk>', views.Details.as_view(), name='details'),
    path('list/', views.List.as_view(), name='list'),
]
