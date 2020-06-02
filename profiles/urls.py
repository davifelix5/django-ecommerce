from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('signin/', views.SignIn.as_view(), name='signin'),  # CHECK
    path('update/', views.Update.as_view(), name='update'),  # CHECK
]
